# Duplicate File Detector

Find byte-identical files in a directory tree using file size and SHA-256 hashing. The tool is deliberately read-only: it reports duplicates and exports a CSV; it never deletes or moves files.

## Requirements
- Python 3.10+
- No third-party packages

## Run
```bash
python main.py ~/Downloads
python main.py ~/Downloads --csv duplicates.csv
```

Use the report to review files manually before deleting anything. Symlinks are skipped by default. Large directories can take time because file contents are hashed.

## Tests
```bash
python -m unittest discover -s tests -v
```
