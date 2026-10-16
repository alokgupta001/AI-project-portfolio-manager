"""Checkpoint failures are simulated; these tests never invoke Docker or read real data."""

import json
import subprocess
import sys

import pytest

from scripts import sprint11_preserve as S


@pytest.mark.parametrize("failure", ["sql", "json"])
def test_failed_validation_leaves_backup_capture_retryable(tmp_path, monkeypatch, failure):
    monkeypatch.setattr(S, "FOLDER", tmp_path)
    monkeypatch.setattr(sys, "argv", ["preserve", "database", "before"])
    target = tmp_path / "database-before.json"
    failed = True
    commands = []

    def query(args, **_kwargs):
        sql = args[-1]
        if "pg_tables" in sql:
            return "ppm_projects"
        if "alembic_version" in sql:
            return "0012_ai_runtime"
        if failed and failure == "sql":
            raise subprocess.CalledProcessError(1, args)
        return '{"count":1,"hash":"synthetic-hash"}'

    write = type(target).write_text

    def checkpoint(path, *args, **kwargs):
        if failed and failure == "json" and path == target:
            raise OSError("Synthetic checkpoint failure")
        return write(path, *args, **kwargs)

    def backup(args, stdout, **_kwargs):
        assert json.loads(target.read_text())["tables"]["ppm_projects"]["count"] == 1
        commands.append(args)
        stdout.write(b"synthetic backup only")

    monkeypatch.setattr(S.subprocess, "check_output", query)
    monkeypatch.setattr(S.subprocess, "run", backup)
    monkeypatch.setattr(type(target), "write_text", checkpoint)
    with pytest.raises((subprocess.CalledProcessError, OSError)):
        S.database()
    assert list(tmp_path.iterdir()) == [] and commands == []
    failed = False
    S.database()
    assert len(commands) == 2
    assert (tmp_path / "database-before.dump").read_bytes() == b"synthetic backup only"
    assert (tmp_path / "objects-before.tar").read_bytes() == b"synthetic backup only"
    with pytest.raises(SystemExit, match="overwrite"):
        S.database()
    assert len(commands) == 2
