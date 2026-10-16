"""Bounded, text-only extraction in a disposable worker subprocess. Never execute content."""

import csv
import io
import json
import os
import re
import shutil
import socket
import struct
import subprocess
import sys
import tempfile
import zipfile
from pathlib import Path
from typing import Any
from xml.etree import ElementTree as ET

PARSER_VERSION = "source-parser-v1"
MAX_BYTES = 8 * 1024 * 1024
MAX_TEXT = 500_000


class IntakeError(ValueError):
    pass


def validate(data: bytes, filename: str) -> str:
    if not 0 < len(data) <= MAX_BYTES:
        raise IntakeError("SIZE_LIMIT")
    ext = filename.rsplit(".", 1)[-1].lower()
    if b"EICAR-STANDARD-ANTIVIRUS-TEST-FILE" in data or b"<script" in data.lower():
        raise IntakeError("UNSAFE_CONTENT")
    if ext in {"txt", "csv"}:
        try:
            value = data.decode("utf-8-sig")
        except UnicodeError:
            raise IntakeError("INVALID_UTF8") from None
        if any(ord(c) < 32 and c not in "\n\r\t" for c in value):
            raise IntakeError("CONTROL_CHARACTER")
    elif ext in {"docx", "xlsx"}:
        try:
            with zipfile.ZipFile(io.BytesIO(data)) as z:
                entries = z.infolist()
                if len(entries) > 500 or sum(x.file_size for x in entries) > 16 * 1024 * 1024:
                    raise IntakeError("ARCHIVE_LIMIT")
                if len({x.filename for x in entries}) != len(entries):
                    raise IntakeError("INVALID_ARCHIVE")
                required = "word/document.xml" if ext == "docx" else "xl/workbook.xml"
                if required not in z.namelist():
                    raise IntakeError("FORMAT_MISMATCH")
                for item in entries:
                    if (
                        item.flag_bits & 1
                        or item.filename.startswith("/")
                        or ".." in Path(item.filename).parts
                    ):
                        raise IntakeError("INVALID_ARCHIVE")
                    if re.search(r"vbaProject|embeddings/|externalLinks/", item.filename, re.I):
                        raise IntakeError("ACTIVE_CONTENT")
                    if item.filename.endswith((".xml", ".rels")):
                        xml_bytes = z.read(item)
                        if b"<!DOCTYPE" in xml_bytes.upper() or b"<!ENTITY" in xml_bytes.upper():
                            raise IntakeError("ACTIVE_XML")
                        if item.filename.endswith(".rels") and re.search(
                            rb"TargetMode\s*=\s*[\'\"]External", xml_bytes, re.I
                        ):
                            raise IntakeError("EXTERNAL_REFERENCE")
        except (zipfile.BadZipFile, KeyError, RuntimeError):
            raise IntakeError("CORRUPT_ARCHIVE") from None
    elif ext == "pdf":
        if not data.startswith(b"%PDF-") or b"%%EOF" not in data[-2048:]:
            raise IntakeError("FORMAT_MISMATCH")
        normalized = re.sub(rb"#([0-9A-Fa-f]{2})", lambda m: bytes([int(m[1], 16)]), data)
        if re.search(rb"/(JavaScript|JS|Launch|EmbeddedFile|OpenAction|AA)\b", normalized):
            raise IntakeError("ACTIVE_PDF")
    elif ext in {"png", "jpg", "jpeg"}:
        signature = b"\x89PNG\r\n\x1a\n" if ext == "png" else b"\xff\xd8\xff"
        if not data.startswith(signature):
            raise IntakeError("FORMAT_MISMATCH")
    else:
        raise IntakeError("UNSUPPORTED_FORMAT")
    return ext


def scan(data: bytes, host: str, port: int = 3310) -> str:
    if not host:
        raise IntakeError("SCANNER_UNAVAILABLE")
    try:
        with socket.create_connection((host, port), timeout=15) as sock:
            sock.sendall(b"zINSTREAM\x00")
            for start in range(0, len(data), 65536):
                chunk = data[start : start + 65536]
                sock.sendall(struct.pack("!I", len(chunk)) + chunk)
            sock.sendall(struct.pack("!I", 0))
            response = bytearray()
            while b"\x00" not in response and len(response) < 4096:
                part = sock.recv(4096)
                if not part:
                    break
                response.extend(part)
        if bytes(response).strip(b"\x00\r\n") != b"stream: OK":
            raise IntakeError("SCAN_REJECTED")
        return "clamd-instream"
    except (OSError, TimeoutError):
        raise IntakeError("SCANNER_UNAVAILABLE") from None


def ocr(path: Path) -> tuple[str, float | None]:
    if not shutil.which("tesseract"):
        raise IntakeError("OCR_UNAVAILABLE")
    result = subprocess.run(
        ["tesseract", str(path), "stdout", "-l", "eng", "--psm", "6", "tsv"],
        capture_output=True,
        timeout=12,
        check=True,
    )
    rows = list(csv.DictReader(io.StringIO(result.stdout.decode("utf-8")), delimiter="\t"))
    words = [r for r in rows if r.get("text", "").strip() and float(r["conf"]) >= 0]
    text = " ".join(r["text"] for r in words)
    confidence = sum(float(r["conf"]) for r in words) / len(words) / 100 if words else None
    return text, confidence


def validate_pdf_objects(reader: Any) -> None:
    """Inspect resolved containers, including compressed objects, without following cycles."""
    from pypdf.generic import ArrayObject, DictionaryObject, IndirectObject, NameObject

    active_names = {
        "/JavaScript",
        "/JS",
        "/Launch",
        "/EmbeddedFile",
        "/EmbeddedFiles",
        "/OpenAction",
        "/AA",
    }
    pending = [reader.trailer]
    references: set[tuple[int, int]] = set()
    containers: set[int] = set()
    examined = 0
    while pending:
        examined += 1
        if examined > 50_000:
            raise IntakeError("PDF_OBJECT_LIMIT")
        obj = pending.pop()
        if isinstance(obj, IndirectObject):
            reference = (obj.idnum, obj.generation)
            if reference in references:
                continue
            references.add(reference)
            obj = obj.get_object()
        if isinstance(obj, NameObject) and str(obj) in active_names:
            raise IntakeError("ACTIVE_PDF")
        if isinstance(obj, (DictionaryObject, ArrayObject)):
            if id(obj) in containers:
                continue
            containers.add(id(obj))
            if isinstance(obj, DictionaryObject):
                if any(str(key) in active_names for key in obj):
                    raise IntakeError("ACTIVE_PDF")
                pending.extend(obj.values())
            else:
                pending.extend(obj)


def extract(data: bytes, filename: str) -> list[dict]:
    ext = validate(data, filename)
    locations: list[tuple[str, str, str, float | None]] = []
    if ext == "txt":
        locations = [
            (f"paragraph {i}", t, "text", None)
            for i, t in enumerate(data.decode("utf-8-sig").split("\n\n"), 1)
        ]
    elif ext == "csv":
        rows = list(csv.reader(io.StringIO(data.decode("utf-8-sig"))))
        if (
            not rows
            or len(rows) > 5000
            or len(rows[0]) > 100
            or any(len(r) != len(rows[0]) for r in rows)
        ):
            raise IntakeError("TABLE_LIMIT_OR_SHAPE")
        locations = [
            (f"sheet CSV row {i}", " | ".join(row), "table", None) for i, row in enumerate(rows, 1)
        ]
    elif ext == "docx":
        with zipfile.ZipFile(io.BytesIO(data)) as z:
            root = ET.fromstring(z.read("word/document.xml"))
            ns = {"w": "http://schemas.openxmlformats.org/wordprocessingml/2006/main"}
            locations = [
                (
                    f"paragraph {i}",
                    "".join(t.text or "" for t in p.findall(".//w:t", ns)),
                    "text",
                    None,
                )
                for i, p in enumerate(root.findall(".//w:p", ns), 1)
            ]
    elif ext == "xlsx":
        with zipfile.ZipFile(io.BytesIO(data)) as z:
            ns = {"s": "http://schemas.openxmlformats.org/spreadsheetml/2006/main"}
            shared = []
            if "xl/sharedStrings.xml" in z.namelist():
                shared = [
                    "".join(s.itertext()) for s in ET.fromstring(z.read("xl/sharedStrings.xml"))
                ]
            workbook = ET.fromstring(z.read("xl/workbook.xml"))
            relns = "{http://schemas.openxmlformats.org/package/2006/relationships}"
            rels = {
                r.attrib["Id"]: r.attrib["Target"]
                for r in ET.fromstring(z.read("xl/_rels/workbook.xml.rels")).findall(
                    relns + "Relationship"
                )
            }
            for sheet in workbook.findall("s:sheets/s:sheet", ns):
                rid = sheet.attrib[
                    "{http://schemas.openxmlformats.org/officeDocument/2006/relationships}id"
                ]
                target = rels[rid]
                name = target.lstrip("/") if target.startswith("/") else "xl/" + target
                tree = ET.fromstring(z.read(name))
                for row in tree.findall(".//s:sheetData/s:row", ns):
                    cells = []
                    for cell in row:
                        # Formula results can be stale: never evaluate or report cached values.
                        if cell.find("s:f", ns) is not None:
                            value = "[formula omitted]"
                        elif cell.attrib.get("t") == "s":
                            value = shared[int(cell.findtext("s:v", "0", ns))]
                        elif cell.attrib.get("t") == "inlineStr":
                            value = "".join(t.text or "" for t in cell.findall(".//s:t", ns))
                        else:
                            value = cell.findtext("s:v", "", ns)
                        cells.append(cell.attrib.get("r", "?") + ": " + value)
                    locations.append(
                        (
                            f"sheet {sheet.attrib['name']} row {row.attrib.get('r', '?')}",
                            " | ".join(cells),
                            "table",
                            None,
                        )
                    )
    else:
        with tempfile.TemporaryDirectory(prefix="ppm-source-") as tmp:
            path = Path(tmp) / ("source." + ext)
            path.write_bytes(data)
            if ext == "pdf":
                from pypdf import PdfReader

                reader = PdfReader(io.BytesIO(data), strict=True)
                if reader.is_encrypted or not 0 < len(reader.pages) <= 50:
                    raise IntakeError("PDF_LIMIT_OR_ENCRYPTED")
                validate_pdf_objects(reader)
                for i, page in enumerate(reader.pages, 1):
                    text = page.extract_text() or ""
                    confidence = None
                    method = "text"
                    if not text.strip():
                        if not shutil.which("pdftoppm"):
                            raise IntakeError("OCR_UNAVAILABLE")
                        prefix = Path(tmp) / "page"
                        subprocess.run(
                            [
                                "pdftoppm",
                                "-f",
                                str(i),
                                "-l",
                                str(i),
                                "-singlefile",
                                "-scale-to",
                                "2000",
                                "-png",
                                str(path),
                                str(prefix),
                            ],
                            capture_output=True,
                            timeout=12,
                            check=True,
                        )
                        text, confidence = ocr(prefix.with_suffix(".png"))
                        method = "ocr"
                    locations.append((f"page {i}", text, method, confidence))
            else:
                # Tesseract/Leptonica rejects malformed images. Bound dimensions before decoding.
                if ext == "png":
                    width, height = struct.unpack("!II", data[16:24])
                    if not 0 < width * height <= 16_000_000:
                        raise IntakeError("IMAGE_LIMIT")
                text, confidence = ocr(path)
                locations.append(("image 1", text, "ocr", confidence))
    if len(locations) > 5000 or sum(len(x[1]) for x in locations) > MAX_TEXT:
        raise IntakeError("EXTRACTION_LIMIT")
    result: list[dict[str, Any]] = []
    for location, text, method, confidence in locations:
        text = text.strip()
        for start in range(0, len(text), 1200):
            result.append(
                dict(
                    ordinal=len(result),
                    location=location + f" chars {start + 1}-{min(start + 1200, len(text))}",
                    text=text[start : start + 1200],
                    method=method,
                    confidence=confidence,
                )
            )
    if len(result) > 5000:
        raise IntakeError("EXTRACTION_LIMIT")
    if not result:
        raise IntakeError("NO_EXTRACTABLE_TEXT")
    return result


def isolated_extract(data: bytes, filename: str) -> list[dict]:
    with tempfile.TemporaryDirectory(prefix="ppm-parse-") as tmp:
        source = Path(tmp) / "source"
        output = Path(tmp) / "output.json"
        source.write_bytes(data)
        process = subprocess.run(
            [sys.executable, "-m", "ppm_api.document_parser", str(source), filename, str(output)],
            capture_output=True,
            timeout=60,
            check=False,
            env=os.environ | {"PYTHONPATH": str(Path(__file__).resolve().parents[1])},
        )
        if process.returncode != 0:
            code = output.read_text() if output.exists() else "PARSER_FAILED"
            raise IntakeError(code if re.fullmatch("[A-Z_]{1,48}", code) else "PARSER_FAILED")
        if output.stat().st_size > 4_000_000:
            raise IntakeError("EXTRACTION_LIMIT")
        return json.loads(output.read_text())


if __name__ == "__main__":
    try:
        if sys.platform != "win32":
            import resource

            resource.setrlimit(resource.RLIMIT_AS, (768 * 1024 * 1024, 768 * 1024 * 1024))
            resource.setrlimit(resource.RLIMIT_CPU, (45, 45))
            resource.setrlimit(resource.RLIMIT_FSIZE, (8 * 1024 * 1024, 8 * 1024 * 1024))
        value = extract(Path(sys.argv[1]).read_bytes(), sys.argv[2])
        Path(sys.argv[3]).write_text(json.dumps(value))
    except Exception as exc:
        Path(sys.argv[3]).write_text(str(exc) if isinstance(exc, IntakeError) else "PARSER_FAILED")
        sys.exit(1)
