import importlib.util
from pathlib import Path

backend_root = Path(__file__).resolve().parent
app_path = backend_root / 'app.py'

spec = importlib.util.spec_from_file_location('backend_app', app_path)
backend_app = importlib.util.module_from_spec(spec)
spec.loader.exec_module(backend_app)

from app.utils.jwt_handler import generate_token

token = generate_token(1, 'test@example.com')
client = backend_app.app.test_client()
print('health', client.get('/health').status_code)
r2 = client.get('/documents', headers={'Authorization': f'Bearer {token}'})
print('/documents', r2.status_code)
print(r2.get_data(as_text=True)[:500])
