from pathlib import Path
import unittest


SKILL_ROOT = Path(__file__).resolve().parents[1]


class CompactEngineeringNoteTests(unittest.TestCase):
    def test_compact_note_profile_is_routed_from_skill(self):
        skill = (SKILL_ROOT / "SKILL.md").read_text(encoding="utf-8")
        self.assertIn("Compact Engineering Note / 简洁证据型工程说明", skill)
        self.assertIn("Light + PDF", skill)
        self.assertIn("references/compact-engineering-note.md", skill)
        self.assertIn("Mandatory outline approval applies", skill)

    def test_compact_note_reference_preserves_evidence_and_readability_rules(self):
        profile = (
            SKILL_ROOT / "references" / "compact-engineering-note.md"
        ).read_text(encoding="utf-8")
        for required in (
            "【来源确认】",
            "【交叉印证】",
            "【工程推断】",
            "【尚未确认】",
            "Evidence figure / 证据图",
            "Analytical redraw / 分析重绘",
            "Conceptual illustration / 概念示意",
            "at least 9.5 pt",
            "at least 8 pt",
            "mandatory outline",
        ):
            self.assertIn(required, profile)

    def test_qa_contains_compact_note_gate(self):
        qa = (SKILL_ROOT / "references" / "qa-checklist.md").read_text(
            encoding="utf-8"
        )
        self.assertIn("Gate D: Compact Engineering Note", qa)
        self.assertIn("approximately 30 seconds", qa)
        self.assertIn("without relying on colour alone", qa)


if __name__ == "__main__":
    unittest.main()

