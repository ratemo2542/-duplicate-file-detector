import tempfile
import unittest
from pathlib import Path
from duplicate_finder import find_duplicates

class DuplicateFinderTests(unittest.TestCase):
    def test_finds_same_content_with_different_names(self):
        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder)
            (root / "a.txt").write_text("same")
            (root / "b.txt").write_text("same")
            (root / "c.txt").write_text("different")
            groups = find_duplicates(root)
            self.assertEqual(len(groups), 1)
            self.assertEqual(len(next(iter(groups.values()))), 2)

if __name__ == "__main__":
    unittest.main()
