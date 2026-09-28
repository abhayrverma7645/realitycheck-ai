"""
Unit tests for SerpApi search service.
"""

import unittest
from services.serpapi_service import SerpApiService

class TestSerpApiService(unittest.TestCase):
    def setUp(self):
        self.service = SerpApiService()

    def test_missing_api_key_handling(self):
        """Verify service returns clean error dictionary when API key is missing."""
        service = SerpApiService(api_key="")
        result = service.search_google("test query")
        self.assertFalse(result["success"])
        self.assertIn("missing", result["error"].lower())

    def test_domain_extraction(self):
        """Test URL domain extraction helper."""
        self.assertEqual(self.service._extract_domain("https://www.reuters.com/article/123"), "reuters.com")
        self.assertEqual(self.service._extract_domain("http://bbc.co.uk/news"), "bbc.co.uk")
        self.assertEqual(self.service._extract_domain(""), "Unknown Source")

    def test_parse_serp_response(self):
        """Test parsing raw SerpApi JSON response into structured evidence items."""
        mock_response = {
            "organic_results": [
                {
                    "title": "Test Title",
                    "link": "https://example.com/test",
                    "snippet": "This is a test snippet",
                    "date": "Jan 1, 2026",
                    "source": "Example News"
                }
            ]
        }
        parsed = self.service._parse_serp_response(mock_response)
        self.assertEqual(len(parsed), 1)
        self.assertEqual(parsed[0]["title"], "Test Title")
        self.assertEqual(parsed[0]["domain"], "example.com")
        self.assertEqual(parsed[0]["result_type"], "Organic Search")

if __name__ == "__main__":
    unittest.main()
