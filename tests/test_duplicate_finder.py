import tempfile
import unittest
from pathlib import Path
import main

class DuplicateFinderTests(unittest.TestCase):
    def test_finds_identical_content_and_skips_unique_files(self):
        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder)
            (root / "one.txt").write_text("same")
            (root / "two.txt").write_text("same")
            (root / "three.txt").write_text("different")
            groups = main.find_duplicates(root)
            self.assertEqual(len(groups), 1)
            self.assertEqual(len(groups[0]), 2)

    def test_rejects_missing_directory(self):
        with self.assertRaises(ValueError):
            main.find_duplicates(Path("/definitely/not/a/real/folder"))

if __name__ == "__main__":
    unittest.main()
