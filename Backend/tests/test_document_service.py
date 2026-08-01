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

    def test_serialize_document_row_preserves_qr_verification_metadata(self):
        row = (
            2,
            "qr.pdf",
            "stored-qr.pdf",
            "uploads/stored-qr.pdf",
            "pdf",
            "QR content",
            "2026-07-30 10:00:00",
            88,
            "Processed",
            '{"document_type": "Invoice", "qr_verification": {"qr_found": true, "qr_content": ["abc123"], "validation_result": "Valid", "confidence": 0.95, "method": "opencv"}}',
        )

        payload = serialize_document_row(row)

        self.assertTrue(payload["qr_verification"]["qr_found"])
        self.assertEqual(payload["qr_verification"]["qr_content"], ["abc123"])
        self.assertEqual(payload["qr_verification"]["validation_result"], "Valid")
        self.assertEqual(payload["qr_verification"]["confidence"], 0.95)
        self.assertEqual(payload["fields"]["document_type"], "Invoice")

    def test_serialize_document_row_handles_missing_metadata(self):
        row = (
            3,
            "plain.pdf",
            "stored-plain.pdf",
            "uploads/stored-plain.pdf",
            "pdf",
            "Plain text",
            "2026-07-30 10:00:00",
            50,
            "Processed",
            None,
        )

        payload = serialize_document_row(row)

        self.assertEqual(payload["fields"], {})
        self.assertEqual(payload["qr_verification"], {})
        self.assertEqual(payload["status"], "Processed")


if __name__ == "__main__":
    unittest.main()
