import unittest

from app.services.dashboard_service import build_dashboard_summary


class DashboardServiceTests(unittest.TestCase):
    def test_build_dashboard_summary_aggregates_documents(self):
        documents = [
            {"trust_score": 95, "status": "Verified", "uploaded_at": "2026-07-30 10:00:00"},
            {"trust_score": 82, "status": "Needs Manual Review", "uploaded_at": "2026-07-30 11:00:00"},
            {"trust_score": 60, "status": "Rejected", "uploaded_at": "2026-07-29 09:00:00"},
        ]

        summary = build_dashboard_summary(documents)

        self.assertEqual(summary["total_documents"], 3)
        self.assertEqual(summary["average_trust_score"], 79)
        self.assertEqual(summary["suspicious_documents"], 2)
        self.assertEqual(summary["today_uploads"], 2)


if __name__ == "__main__":
    unittest.main()
