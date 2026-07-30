import unittest

from app.services.classification_service import classify_document


class ClassificationServiceTests(unittest.TestCase):
    def test_classify_document_assigns_financial_category(self):
        result = classify_document(
            {"document_title": "Invoice", "document_type": "Invoice", "purpose": "Billing"},
            "invoice.pdf",
        )

        self.assertEqual(result["category"], "Financial")
        self.assertGreaterEqual(result["confidence"], 0.8)


if __name__ == "__main__":
    unittest.main()
