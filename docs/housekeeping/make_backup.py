"""Verified two-destination backup; Python 3.10 standard library only.

Run from a scratch copy outside the source. The source is read-only.
Never overwrites an existing backup, and never stops/restarts the app.
"""
import argparse
import calendar
import csv
import hashlib
import json
import os
from pathlib import Path
import shutil
import sqlite3
import sys
import time
from datetime import datetime, timedelta, timezone

DEFAULT_SOURCE = Path(r"C:\Users\brian\Documents\Codex\2026-10-17\Assembly Workshop")
DEFAULT_LOCAL = Path(r"D:\Backups\Assembly Workshop")
DEFAULT_CLOUD = Path(r"C:\Users\brian\OneDrive\Backups\Assembly Workshop")
CHUNK = 1024 * 1024


def digest(path):
    h = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(CHUNK), b""):
            h.update(block)
    return h.hexdigest()


def pacific_now():
    # US Pacific DST rules since 2007; no external timezone database required.
    now = datetime.now(timezone.utc)
    year = now.year
    march_sunday = 1 + (6 - calendar.weekday(year, 3, 1)) % 7 + 7
    november_sunday = 1 + (6 - calendar.weekday(year, 11, 1)) % 7
    start = datetime(year, 3, march_sunday, 10, tzinfo=timezone.utc)
    end = datetime(year, 11, november_sunday, 9, tzinfo=timezone.utc)
    return now.astimezone(timezone(timedelta(hours=-7 if start <= now < end else -8)))


def inventory(root):
    files, directories = [], []
    for current, dirs, names in os.walk(root, followlinks=False):
        dirs[:] = sorted(d for d in dirs if d != "__pycache__")
        for name in dirs + names:
            path = Path(current) / name
            if path.is_symlink() or path.stat().st_file_attributes & 0x400:
                raise RuntimeError(f"Reparse point needs explicit handling: {path}")
        directories.extend((Path(current) / d).relative_to(root) for d in dirs)
        files.extend((Path(current) / n).relative_to(root) for n in sorted(names))
    return sorted(files), directories


def is_database(path):
    with path.open("rb") as stream:
        header = stream.read(16)
    return header == b"SQLite format 3\x00" or path.name == "library.sqlite3"


def integrity(path):
    # Immutable prevents copied sidecars from being replayed or changed.
    with sqlite3.connect(path.resolve().as_uri() + "?mode=ro&immutable=1", uri=True) as db:
        result = db.execute("PRAGMA integrity_check").fetchall()
    if result != [("ok",)]:
        raise RuntimeError(f"SQLite integrity failure: {path}: {result}")


def copy_regular(source, target):
    for attempt in range(3):
        before = source.stat()
        shutil.copy2(source, target)
        source_hash = digest(source)
        copy_hash = digest(target)
        after = source.stat()
        if (before.st_size, before.st_mtime_ns) == (after.st_size, after.st_mtime_ns) and source_hash == copy_hash:
            return source_hash, copy_hash
        time.sleep(0.1)
    raise RuntimeError(f"Source changed repeatedly or hash mismatch: {source}")


def verify(root, rows, metadata):
    total = 0
    for index, row in enumerate(rows, 1):
        path = root / row["relative_path"]
        if path.stat().st_size != int(row["bytes"]) or digest(path) != row["copy_sha256"]:
            raise RuntimeError(f"Verification mismatch: {path}")
        if row["verification"] == "sqlite_backup_integrity_ok":
            integrity(path)
        total += path.stat().st_size
        if index % 500 == 0:
            print(f"Verified {index}/{len(rows)}: {root}", flush=True)
    for name, expected in metadata.items():
        if digest(root / name) != expected:
            raise RuntimeError(f"Metadata mismatch: {root / name}")
    actual, _ = inventory(root)
    expected = {row["relative_path"] for row in rows} | set(metadata)
    if {p.as_posix() for p in actual} != expected:
        raise RuntimeError(f"Unexpected/missing files in {root}")
    return total


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source", type=Path, default=DEFAULT_SOURCE)
    parser.add_argument("--local", type=Path, default=DEFAULT_LOCAL)
    parser.add_argument("--onedrive", type=Path, default=DEFAULT_CLOUD)
    args = parser.parse_args()
    source = args.source.resolve(strict=True)
    if Path(__file__).resolve().is_relative_to(source):
        parser.error("Copy this script to a scratch folder outside the project before running it.")
    stamp = pacific_now()
    name = "AssemblyWorkshop_" + stamp.strftime("%Y%m%d-%H%M")
    local, cloud = args.local.resolve() / name, args.onedrive.resolve() / name
    for destination in (local, cloud):
        if destination.is_relative_to(source) or source.is_relative_to(destination):
            raise RuntimeError("Source and destinations must not overlap")
        if destination.exists():
            raise FileExistsError(f"Never overwrite: {destination}")
    if local == cloud or local.is_relative_to(cloud) or cloud.is_relative_to(local):
        raise RuntimeError("Destinations must be separate")
    files, directories = inventory(source)
    for reserved in ("manifest.csv", "BACKUP_README.md"):
        if Path(reserved) in files:
            raise RuntimeError(f"Backup metadata would overwrite source file: {reserved}")
    size = sum((source / rel).stat().st_size for rel in files)
    print(f"Inventory: {len(files)} files, {size} source bytes; skipping only __pycache__ directories", flush=True)
    for parent in (local.parent, cloud.parent):
        parent.mkdir(parents=True, exist_ok=True)
        if shutil.disk_usage(parent).free < size + 64 * CHUNK:
            raise RuntimeError(f"Insufficient free space: {parent}")
    local.mkdir(exist_ok=False)
    for rel in directories:
        (local / rel).mkdir(parents=True, exist_ok=True)
    rows, databases, sidecars = [], [], []
    for index, rel in enumerate(files, 1):
        original, target = source / rel, local / rel
        target.parent.mkdir(parents=True, exist_ok=True)
        if is_database(original):
            # Source explicitly read-only; backup() includes committed live WAL data.
            src = sqlite3.connect(original.resolve().as_uri() + "?mode=ro", uri=True, timeout=30)
            try:
                dst = sqlite3.connect(str(target))
                try:
                    src.backup(dst, pages=256, sleep=0.05)
                finally:
                    dst.close()
            finally:
                src.close()
            integrity(target)
            source_hash, copy_hash = "SQLITE_BACKUP_API_INTEGRITY_OK", digest(target)
            method = "sqlite_backup_integrity_ok"
            databases.append(rel.as_posix())
        else:
            source_hash, copy_hash = copy_regular(original, target)
            method = "sha256_match"
        if rel.name.endswith(("-wal", "-shm", "-journal")):
            sidecars.append(rel.as_posix())
        rows.append(dict(relative_path=rel.as_posix(), bytes=target.stat().st_size,
                         source_sha256=source_hash, copy_sha256=copy_hash, verification=method))
        if index % 250 == 0:
            print(f"Copied {index}/{len(files)}", flush=True)
    current_files, current_dirs = inventory(source)
    if current_files != files or set(current_dirs) != set(directories):
        raise RuntimeError("Source inventory changed during backup; incomplete backup retained, no cloud copy made")
    manifest = local / "manifest.csv"
    with manifest.open("w", encoding="utf-8", newline="") as stream:
        writer = csv.DictWriter(stream, fieldnames=list(rows[0]) if rows else ["relative_path", "bytes", "source_sha256", "copy_sha256", "verification"])
        writer.writeheader()
        writer.writerows(rows)
    payload_bytes = sum(row["bytes"] for row in rows)
    readme = f"""# Assembly Workshop verified backup

Timestamp: {stamp.isoformat()} (America/Los_Angeles)
Source: {source}
Local destination: {local}
Private OneDrive destination: {cloud}
Project payload file count: {len(rows)}
Project payload bytes: {payload_bytes}
Additional backup metadata files: manifest.csv and BACKUP_README.md
Mismatches: 0 (a run fails instead of accepting a mismatch).
Skipped: only directories named __pycache__.

Every regular file was compared with its source using SHA-256. SQLite files
were copied using Python sqlite3.backup from URI mode=ro connections and
verified with PRAGMA integrity_check = ok, instead of source-byte comparison.
The SQLite source_sha256 marker is explicitly not a hash. The copy SHA-256
and size describe the resulting self-contained snapshot. Both destinations
are verified against the manifest; metadata hashes are compared separately
because a manifest cannot contain its own hash. Empty directories are preserved.
Completion of the command confirms both copies; an interrupted run is incomplete.

The app was left running. These are sequential file copies and per-database
transactionally consistent snapshots, not a single project-wide atomic snapshot.
Unsaved browser drafts are not disk files and are not captured. OneDrive's local
copy is verified; this does not prove remote synchronization has completed.
Sharing settings were not changed and no share link was created.

## Restore

1. Preserve the existing project separately. Close the app before restoration.
2. Copy this backup folder's project contents to the intended project directory.
   Keep both data locations, .git, outputs, work, revisions, history and artwork.
3. The listed SQLite sidecars are retained as raw historical evidence. Before
   opening a restored SQLite snapshot, MOVE its adjacent -wal/-shm/-journal
   files outside the restored project into a separate preservation folder.
   Never replay historical sidecars over a self-contained API snapshot.
4. Launch outputs/Mechanical_Design_App/start.bat, never bare python app.py.
   The launcher must select the restored data/normal-use directory.

SQLite snapshots ({len(databases)}):
""" + "".join(f"- {name}\n" for name in databases) + f"\nCopied sidecars ({len(sidecars)}):\n" + ("".join(f"- {name}\n" for name in sidecars) or "- None present in the source inventory.\n")
    (local / "BACKUP_README.md").write_text(readme, encoding="utf-8")
    metadata = {name: digest(local / name) for name in ("manifest.csv", "BACKUP_README.md")}
    print("Verifying local backup", flush=True)
    verify(local, rows, metadata)
    print("Local backup verified; copying finished folder to OneDrive", flush=True)
    shutil.copytree(local, cloud, copy_function=shutil.copy2)
    with (cloud / "manifest.csv").open(encoding="utf-8", newline="") as stream:
        cloud_rows = list(csv.DictReader(stream))
    print("Verifying OneDrive backup", flush=True)
    verify(cloud, cloud_rows, metadata)
    for rel in directories:
        if not (local / rel).is_dir() or not (cloud / rel).is_dir():
            raise RuntimeError(f"Missing directory: {rel}")
    metadata_bytes = sum((local / name).stat().st_size for name in metadata)
    print(json.dumps(dict(status="VERIFIED", local=str(local), onedrive=str(cloud),
                          project_file_count=len(rows), total_file_count=len(rows) + len(metadata),
                          project_bytes=payload_bytes, total_bytes=payload_bytes + metadata_bytes,
                          sqlite_snapshots=len(databases), sidecars=len(sidecars), mismatches=0), indent=2), flush=True)


if __name__ == "__main__":
    main()
