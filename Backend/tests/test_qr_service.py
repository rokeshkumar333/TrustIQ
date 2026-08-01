import os
import tempfile
import unittest
from unittest.mock import patch

from app.services.qr_service import verify_qr


class QRServiceTests(unittest.TestCase):
    def test_detects_qr_markers(self):
        result = verify_qr("This document includes a QR verification token", "report.pdf")
        self.assertTrue(result["verified"])
        self.assertIn("qr", result["markers"])

    def test_returns_false_when_no_markers(self):
        result = verify_qr("A simple invoice without any identifiers", "invoice.pdf")
        self.assertFalse(result["verified"])

    def test_returns_first_qr_code_for_pdf_documents(self):
        with tempfile.NamedTemporaryFile(suffix=".pdf", delete=False) as handle:
            temp_path = handle.name

        try:
            with patch("app.services.qr_service.convert_pdf_to_images", return_value=["page1.png", "page2.png"]), \
                 patch("app.services.qr_service._decode_qr_from_image", side_effect=[["first-code"], ["second-code"]]):
                result = verify_qr("", temp_path)
        finally:
            os.remove(temp_path)

        self.assertTrue(result["qr_found"])
        self.assertEqual(result["qr_content"], ["first-code"])
        self.assertEqual(result["validation_result"], "Valid")
        self.assertEqual(result["method"], "opencv")


if __name__ == "__main__":
    unittest.main()
