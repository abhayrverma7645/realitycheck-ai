"""
Unit tests for evidence analyzer and confidence math.
"""

import unittest
from services.evidence_analyzer import EvidenceAnalyzer

class TestEvidenceAnalyzer(unittest.TestCase):
    def setUp(self):
        self.analyzer = EvidenceAnalyzer()

    def test_classify_source(self):
        """Test source category classification rules."""
        self.assertEqual(self.analyzer.classify_source("cdc.gov"), "Official")
        self.assertEqual(self.analyzer.classify_source("arxiv.org"), "Research")
        self.assertEqual(self.analyzer.classify_source("reuters.com"), "News")
        self.assertEqual(self.analyzer.classify_source("rtings.com"), "Review")
        self.assertEqual(self.analyzer.classify_source("reddit.com"), "Community")
        self.assertEqual(self.analyzer.classify_source("randomblog.xyz"), "Other")

    def test_heuristic_extract_claims(self):
        """Test fallback claim extraction and conflict detection logic."""
        question = "Are electric vehicles cheaper to maintain?"
        mock_evidence = [
            {
                "id": 1,
                "title": "EVs Save Money",
                "link": "https://example.com/ev",
                "snippet": "EVs have fewer moving parts and save 40% on maintenance.",
                "source": "AutoNews",
                "domain": "autonews.com",
                "category": "Industry",
                "date": "2026"
            },
            {
                "id": 2,
                "title": "EV Battery Replacement Costs",
                "link": "https://example.com/battery",
                "snippet": "However, battery replacement is expensive and a major problem.",
                "source": "CarReview",
                "domain": "carreview.com",
                "category": "Review",
                "date": "2026"
            }
        ]

        result = self.analyzer.analyze_investigation(question, mock_evidence)
        self.assertIn("claims", result)
        self.assertGreaterEqual(len(result["claims"]), 1)
        
        main_claim = result["claims"][0]
        # Should detect conflict keyword "however / expensive / problem"
        self.assertEqual(main_claim["status"], "CONFLICTING")
        self.assertIn(1, main_claim["supporting_evidence_ids"])
        self.assertIn(2, main_claim["conflicting_evidence_ids"])

    def test_confidence_math(self):
        """Test confidence score bounds and calculation."""
        score, explanation = self.analyzer._calculate_confidence(
            question="Test question",
            claims=[{"status": "SUPPORTED"}],
            total_sources=5,
            supported_count=1,
            conflicting_count=0,
            insufficient_count=0,
            enriched_evidence=[{"category": "Official", "date": "2026"}]
        )
        self.assertGreater(score, 50)
        self.assertLessEqual(score, 98)
        self.assertIn("Source Volume", explanation)

    def test_confidence_explanation_distinction(self):
        """Verify that confidence explanation clearly distinguishes claims, sources, and multi-factor rating."""
        score, explanation = self.analyzer._calculate_confidence(
            question="Is electric vehicle ownership cheaper to maintain?",
            claims=[{"status": "SUPPORTED"}, {"status": "CONFLICTING"}],
            total_sources=16,
            supported_count=1,
            conflicting_count=1,
            insufficient_count=0,
            enriched_evidence=[{"category": "Official", "date": "2026"}],
            supporting_sources=13,
            conflicting_sources=3
        )
        self.assertEqual(score, 67)
        self.assertIn("Multi-Factor Rating (67%)", explanation)
        self.assertIn("13 supporting, 3 conflicting", explanation)
        self.assertIn("rather than a raw source count ratio", explanation)

if __name__ == "__main__":
    unittest.main()
