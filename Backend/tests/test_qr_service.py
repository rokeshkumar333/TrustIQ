import unittest

from app.services.qr_service import verify_qr


class QRServiceTests(unittest.TestCase):
    def test_detects_qr_markers(self):
        result = verify_qr("This document includes a QR verification token", "report.pdf")
        self.assertTrue(result["verified"])
        self.assertIn("qr", result["markers"])

    def test_returns_false_when_no_markers(self):
        result = verify_qr("A simple invoice without any identifiers", "invoice.pdf")
        self.assertFalse(result["verified"])


if __name__ == "__main__":
    unittest.main()
