import unittest

from app.services.analytics_service import build_analytics_summary


class AnalyticsServiceTests(unittest.TestCase):
    def test_build_analytics_summary_counts_statuses(self):
        documents = [
            {"trust_score": 95, "status": "Verified"},
            {"trust_score": 82, "status": "Needs Manual Review"},
            {"trust_score": 60, "status": "Rejected"},
        ]

        summary = build_analytics_summary(documents)

        self.assertEqual(summary["total_documents"], 3)
        self.assertEqual(summary["average_score"], 79)
        self.assertEqual(summary["max_score"], 95)
        self.assertEqual(summary["min_score"], 60)
        self.assertEqual(summary["status_breakdown"]["Verified"], 1)


if __name__ == "__main__":
    unittest.main()
