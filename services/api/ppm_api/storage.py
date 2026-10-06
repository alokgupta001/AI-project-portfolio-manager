"""Local byte-object interface. No upload endpoint until authorized domain work."""

import os
import tempfile
from pathlib import Path, PurePosixPath
from typing import Protocol


class ObjectStore(Protocol):
    def put(self, key: str, content: bytes) -> None: ...
    def get(self, key: str) -> bytes: ...
    def delete(self, key: str) -> None: ...


class LocalObjectStore:
    def __init__(self, root: Path):
        self.root = root.resolve()

    def _path(self, key: str) -> Path:
        parts = PurePosixPath(key).parts
        if (
            not parts
            or key.startswith("/")
            or "\\" in key
            or ":" in key
            or any(p in {".", ".."} for p in parts)
        ):
            raise ValueError("Invalid object key")
        path = self.root.joinpath(*parts).resolve()
        if not path.is_relative_to(self.root) or path == self.root:
            raise ValueError("Object key outside storage root")
        return path

    def put(self, key: str, content: bytes) -> None:
        path = self._path(key)
        path.parent.mkdir(parents=True, exist_ok=True)
        descriptor, temporary = tempfile.mkstemp(dir=path.parent, prefix=".upload-")
        try:
            with os.fdopen(descriptor, "wb") as stream:
                stream.write(content)
            os.replace(temporary, path)
        finally:
            if os.path.exists(temporary):
                os.unlink(temporary)

    def get(self, key: str) -> bytes:
        return self._path(key).read_bytes()

    def delete(self, key: str) -> None:
        self._path(key).unlink(missing_ok=True)

    def ready(self) -> bool:
        self.root.mkdir(parents=True, exist_ok=True)
        with tempfile.TemporaryFile(dir=self.root) as stream:
            stream.write(b"probe")
            stream.seek(0)
            return stream.read() == b"probe"
