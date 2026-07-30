import unittest

from app.services.document_service import serialize_document_row


class DocumentServiceTests(unittest.TestCase):
    def test_serialize_document_row_includes_report_fields(self):
        row = (
            1,
            "invoice.pdf",
            "stored.pdf",
            "uploads/stored.pdf",
            "pdf",
            "Invoice details",
            "2026-07-30 10:00:00",
            92,
            "Verified",
            '{"document_type": "Invoice", "document_title": "Invoice"}',
        )

        payload = serialize_document_row(row)

        self.assertEqual(payload["id"], 1)
        self.assertEqual(payload["trust_score"], 92)
        self.assertEqual(payload["status"], "Verified")
        self.assertEqual(payload["fields"]["document_type"], "Invoice")


if __name__ == "__main__":
    unittest.main()
