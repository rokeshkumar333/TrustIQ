import importlib.util
import unittest
from pathlib import Path


class DocumentRouteTests(unittest.TestCase):
    def setUp(self):
        backend_root = Path(__file__).resolve().parents[1]
        app_path = backend_root / "app.py"
        spec = importlib.util.spec_from_file_location("backend_app", app_path)
        self.backend_app = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(self.backend_app)

    def test_documents_route_returns_documents(self):
        from app.utils.jwt_handler import generate_token

        token = generate_token(1, "test@example.com")
        client = self.backend_app.app.test_client()
        response = client.get(
            "/documents",
            headers={"Authorization": f"Bearer {token}"}
        )

        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertTrue(data.get("success"))
        self.assertIn("documents", data)
        self.assertIsInstance(data["documents"], list)


if __name__ == "__main__":
    unittest.main()
