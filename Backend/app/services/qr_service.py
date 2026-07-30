import re


def verify_qr(text, filename=""):
    if not text:
        text = ""

    combined = f"{text} {filename}".lower()

    tokens = ["qr", "barcode", "verify", "auth", "token", "serial", "tracking"]
    found_markers = [token for token in tokens if token in combined]

    if found_markers:
        return {
            "verified": True,
            "method": "text-pattern",
            "markers": found_markers,
            "message": "QR-style verification markers detected in document content.",
        }

    match = re.search(r"[A-Z0-9]{4,}", text)
    if match:
        return {
            "verified": True,
            "method": "text-pattern",
            "markers": ["alphanumeric-sequence"],
            "message": "Document contains a structured verification sequence.",
        }

    return {
        "verified": False,
        "method": "text-pattern",
        "markers": [],
        "message": "No QR verification markers detected.",
    }
