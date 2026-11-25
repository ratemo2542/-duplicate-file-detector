import tempfile, unittest, sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from main import find_duplicates

class DuplicateTests(unittest.TestCase):
    def test_finds_identical_content(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root/"a.txt").write_text("same")
            (root/"b.txt").write_text("same")
            (root/"c.txt").write_text("different")
            groups = find_duplicates(root)
            self.assertEqual(len(groups), 1)
            self.assertEqual({p.name for p in groups[0]}, {"a.txt", "b.txt"})
if __name__ == "__main__":
    unittest.main()
