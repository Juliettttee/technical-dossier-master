import importlib.util
import json
import tempfile
import unittest
from pathlib import Path

SCRIPT = Path(__file__).resolve().parents[1] / "scripts" / "resource_index.py"
SPEC = importlib.util.spec_from_file_location("resource_index", SCRIPT)
MODULE = importlib.util.module_from_spec(SPEC)
assert SPEC.loader
SPEC.loader.exec_module(MODULE)


class ResourceIndexTests(unittest.TestCase):
    def test_incremental_lifecycle_optional_manifest_and_selection(self):
        with tempfile.TemporaryDirectory(dir=Path(__file__).parent) as temporary:
            root = Path(temporary) / "resource-packs"
            eee = root / "eee"
            water = root / "water-features" / "sources"
            eee.mkdir(parents=True)
            water.mkdir(parents=True)
            relevant = eee / "结构材料 notes.txt"
            unrelated = water / "fountain-catalogue.pdf"
            unknown = eee / "mystery.xyz"
            relevant.write_text("v1", encoding="utf-8")
            unrelated.write_bytes(b"not parsed")
            unknown.write_bytes(b"unknown")
            (root / "water-features" / "pack.json").write_text(
                json.dumps({"id": "water-features", "domains": ["fountain engineering"]}),
                encoding="utf-8",
            )
            index_path = root / ".resource-index.json"

            first_index, first = MODULE.scan(root, index_path, "结构 材料", 1, False)
            MODULE.atomic_write(index_path, first_index)
            self.assertIn("eee/结构材料 notes.txt", first["summary"]["new"])
            self.assertIn("eee/mystery.xyz", first["summary"]["unsupported"])
            self.assertTrue(any(item["folder"] == "eee" and item["manifest"] == "absent" for item in first_index["packs"]))
            self.assertTrue(any(item["folder"] == "water-features" for item in first_index["packs"]))
            self.assertFalse(any("fountain-catalogue.pdf" in item["relative_path"] for item in first["candidates"]))
            self.assertTrue(any("结构材料" in item["relative_path"] for item in first["candidates"]))

            _, english_query = MODULE.scan(root, index_path, "structural materials", 1, False)
            self.assertTrue(any("结构材料" in item["relative_path"] for item in english_query["candidates"]))

            relevant.write_text("version two", encoding="utf-8")
            second_index, second = MODULE.scan(root, index_path, "结构 材料", 1, False)
            MODULE.atomic_write(index_path, second_index)
            self.assertIn("eee/结构材料 notes.txt", second["summary"]["modified"])

            relevant.unlink()
            third_index, third = MODULE.scan(root, index_path, "结构 材料", 1, False)
            self.assertIn("eee/结构材料 notes.txt", third["summary"]["deleted"])
            self.assertFalse(any(item.get("relative_path") == "eee/结构材料 notes.txt" for item in third_index["files"]))

    def test_bad_manifest_is_reported(self):
        with tempfile.TemporaryDirectory(dir=Path(__file__).parent) as temporary:
            root = Path(temporary) / "resource-packs"
            pack = root / "eee"
            pack.mkdir(parents=True)
            (pack / "pack.json").write_text("{bad", encoding="utf-8")
            _, report = MODULE.scan(root, root / ".resource-index.json", "test", 1, False)
            self.assertTrue(any(item["path"] == "eee/pack.json" for item in report["summary"]["errors"]))


if __name__ == "__main__":
    unittest.main()
