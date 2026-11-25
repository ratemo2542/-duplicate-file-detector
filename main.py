"""Read-only duplicate file finder using SHA-256."""
import argparse, csv, hashlib
from collections import defaultdict
from pathlib import Path

def sha256(path, chunk_size=1024 * 1024):
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(chunk_size), b""):
            digest.update(chunk)
    return digest.hexdigest()

def find_duplicates(root):
    root = Path(root).expanduser().resolve()
    if not root.is_dir():
        raise ValueError(f"Not a directory: {root}")
    by_size = defaultdict(list)
    for path in root.rglob("*"):
        try:
            if path.is_file() and not path.is_symlink():
                by_size[path.stat().st_size].append(path)
        except (OSError, PermissionError):
            continue
    by_hash = defaultdict(list)
    for paths in by_size.values():
        if len(paths) < 2:
            continue
        for path in paths:
            try:
                by_hash[sha256(path)].append(path)
            except (OSError, PermissionError):
                continue
    return [paths for paths in by_hash.values() if len(paths) > 1]

def main():
    parser = argparse.ArgumentParser(description="Find duplicate files without deleting anything.")
    parser.add_argument("directory")
    parser.add_argument("--csv", dest="csv_path")
    args = parser.parse_args()
    try:
        groups = find_duplicates(args.directory)
    except ValueError as exc:
        parser.error(str(exc))
    if not groups:
        print("No duplicates found.")
        return
    rows = []
    for number, group in enumerate(groups, 1):
        print(f"\nDuplicate group {number}:")
        for path in group:
            print(f"  {path}")
            rows.append((number, str(path), path.stat().st_size))
    if args.csv_path:
        with open(args.csv_path, "w", newline="", encoding="utf-8") as handle:
            writer = csv.writer(handle)
            writer.writerow(["group", "path", "size_bytes"])
            writer.writerows(rows)
        print(f"\nReport written to {args.csv_path}")

if __name__ == "__main__":
    main()
