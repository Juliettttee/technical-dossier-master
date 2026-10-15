from pathlib import Path
import unittest


SKILL_ROOT = Path(__file__).resolve().parents[1]


class ResearchDepthModeTests(unittest.TestCase):
    def test_skill_routes_before_resource_scan(self):
        text = (SKILL_ROOT / "SKILL.md").read_text(encoding="utf-8")
        gate = text.index("## Research depth gate")
        resource_scan = text.index("## Resource Packs")
        self.assertLess(gate, resource_scan)
        self.assertIn("Never silently upgrade", text)
        self.assertIn("Light is the default", text)

    def test_mode_reference_has_all_three_modes_and_upgrade_rule(self):
        text = (SKILL_ROOT / "references" / "research-depth-modes.md").read_text(encoding="utf-8")
        self.assertIn("Mode 1 - Light", text)
        self.assertIn("Mode 2 - Standard", text)
        self.assertIn("Mode 3 - Professional", text)
        self.assertIn("Never upgrade silently", text)
        self.assertIn("A format request is not a depth upgrade", text)

    def test_online_sources_require_clickable_claim_adjacent_links(self):
        skill = (SKILL_ROOT / "SKILL.md").read_text(encoding="utf-8")
        checklist = (SKILL_ROOT / "references" / "qa-checklist.md").read_text(encoding="utf-8")
        self.assertIn("Clickable online-source links - mandatory", skill)
        self.assertIn("source register does not replace claim-adjacent links", skill)
        self.assertIn("verify that PDF link annotations exist", skill)
        self.assertIn("visible descriptive link near that claim", checklist)
        self.assertIn("PDF hyperlink annotations exist", checklist)


if __name__ == "__main__":
    unittest.main()

