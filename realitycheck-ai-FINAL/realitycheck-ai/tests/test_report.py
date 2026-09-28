"""
Unit tests for ReportLab PDF report generation.
"""

import unittest
from services.report_generator import PDFReportGenerator

class TestReportGenerator(unittest.TestCase):
    def setUp(self):
        self.generator = PDFReportGenerator()

    def test_pdf_generation(self):
        """Test PDF bytes generation from investigation data."""
        mock_data = {
            "question": "Is electric car ownership cheaper?",
            "executive_summary": "Test executive summary explanation.",
            "metrics": {
                "total_sources": 4,
                "confidence_score": 82,
                "confidence_explanation": "High source agreement."
            },
            "claims": [
                {
                    "claim": "EVs have lower fuel costs",
                    "status": "SUPPORTED",
                    "confidence": "High",
                    "explanation": "Electricity costs less per mile.",
                    "supporting_evidence_ids": [1],
                    "conflicting_evidence_ids": []
                }
            ],
            "evidence": [
                {
                    "id": 1,
                    "title": "EV Study",
                    "link": "https://example.com/study",
                    "snippet": "EVs save $1000 per year on gas.",
                    "source": "EnergyGov",
                    "category": "Official"
                }
            ]
        }

        pdf_bytes = self.generator.generate_pdf(mock_data)
        self.assertIsInstance(pdf_bytes, bytes)
        self.assertTrue(len(pdf_bytes) > 500)
        # Check PDF header bytes %PDF
        self.assertTrue(pdf_bytes.startswith(b"%PDF"))

if __name__ == "__main__":
    unittest.main()
