"""Find duplicate files safely using SHA-256."""
import argparse
import hashlib
import json
from collections import defaultdict
from pathlib import Path

def file_hash(path: Path, chunk_size: int = 1024 * 1024) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(chunk_size), b""):
            digest.update(chunk)
    return digest.hexdigest()

def find_duplicates(root: Path) -> dict[str, list[Path]]:
    if not root.exists() or not root.is_dir():
        raise ValueError(f"Not a directory: {root}")
    by_size: dict[int, list[Path]] = defaultdict(list)
    for path in root.rglob("*"):
        try:
            if path.is_file() and not path.is_symlink():
                by_size[path.stat().st_size].append(path)
        except OSError:
            continue
    groups: dict[str, list[Path]] = defaultdict(list)
    for paths in by_size.values():
        if len(paths) < 2:
            continue
        for path in paths:
            try:
                groups[file_hash(path)].append(path)
            except OSError:
                continue
    return {digest: paths for digest, paths in groups.items() if len(paths) > 1}

def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("directory", type=Path)
    parser.add_argument("--json", dest="json_path", type=Path, help="Write report as JSON")
    args = parser.parse_args()
    try:
        groups = find_duplicates(args.directory)
    except ValueError as exc:
        parser.error(str(exc))
    report = []
    for digest, paths in groups.items():
        size = paths[0].stat().st_size
        report.append({"sha256": digest, "size_bytes": size, "files": [str(p) for p in paths]})
        print(f"\n{size:,} bytes | SHA-256 {digest}")
        for path in paths:
            print(f"  {path}")
    print(f"\nFound {len(groups)} duplicate group(s).")
    if args.json_path:
        args.json_path.write_text(json.dumps(report, indent=2), encoding="utf-8")
        print(f"Report saved to {args.json_path}")

if __name__ == "__main__":
    main()
