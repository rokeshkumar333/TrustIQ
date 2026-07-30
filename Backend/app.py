from flask import Flask
from flask_cors import CORS
from dotenv import load_dotenv
from pathlib import Path
from app.routes.documents import documents
from app.routes.dashboard import dashboard
from app.routes.analytics import analytics

# Load environment variables
BASE_DIR = Path(__file__).resolve().parent
load_dotenv(BASE_DIR / ".env")

# Import Blueprints
from app.routes.auth import auth
from app.routes.upload import upload

# Create Flask App
app = Flask(__name__)

# Enable CORS
CORS(app)

# Register Blueprints
app.register_blueprint(auth)
app.register_blueprint(upload)
app.register_blueprint(documents)
app.register_blueprint(dashboard)
app.register_blueprint(analytics)

# Home Route
@app.route("/")
def home():
    return "Welcome to TrustIQ Backend"

# Health Check Route
@app.route("/health")
def health():
    return {
        "status": "OK",
        "application": "TrustIQ",
        "version": "1.0.0"
    }

# Run Application
if __name__ == "__main__":
    app.run(debug=True)