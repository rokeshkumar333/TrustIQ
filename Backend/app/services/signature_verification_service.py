import os
import re
from datetime import datetime


def _normalize_text(value):
    if value is None:
        return ""
    if isinstance(value, (list, tuple)):
        return " | ".join(str(item) for item in value if item)
    return str(value)


def _parse_date(value):
    if not value:
        return None
    text = str(value)
    try:
        return datetime.fromisoformat(text.replace("Z", "+00:00"))
    except Exception:
        try:
            return datetime.strptime(text, "%Y-%m-%d")
        except Exception:
            return None


def inspect_pdf_signature(file_path):
    if not file_path or not os.path.exists(file_path):
        return {
            "signed": False,
            "signature_count": 0,
            "verification_status": "Unsupported",
            "signer_name": None,
            "issuer": None,
            "signing_time": None,
            "certificate_valid": None,
            "signature_algorithm": None,
            "hash_algorithm": None,
            "verification_message": "File is missing or unavailable for signature inspection.",
        }

    _, extension = os.path.splitext(file_path)
    if extension.lower() != ".pdf":
        return {
            "signed": False,
            "signature_count": 0,
            "verification_status": "Unsupported",
            "signer_name": None,
            "issuer": None,
            "signing_time": None,
            "certificate_valid": None,
            "signature_algorithm": None,
            "hash_algorithm": None,
            "verification_message": "Signature inspection is only supported for PDF documents.",
        }

    try:
        from pypdf import PdfReader
    except Exception:
        return {
            "signed": False,
            "signature_count": 0,
            "verification_status": "Unsupported",
            "signer_name": None,
            "issuer": None,
            "signing_time": None,
            "certificate_valid": None,
            "signature_algorithm": None,
            "hash_algorithm": None,
            "verification_message": "A supported PDF library is not available for signature inspection.",
        }

    try:
        reader = PdfReader(file_path)
        if not reader or not getattr(reader, "pages", None):
            return {
                "signed": False,
                "signature_count": 0,
                "verification_status": "Unsupported",
                "signer_name": None,
                "issuer": None,
                "signing_time": None,
                "certificate_valid": None,
                "signature_algorithm": None,
                "hash_algorithm": None,
                "verification_message": "The PDF could not be read for signature inspection.",
            }
    except Exception as exc:
        return {
            "signed": False,
            "signature_count": 0,
            "verification_status": "Unsupported",
            "signer_name": None,
            "issuer": None,
            "signing_time": None,
            "certificate_valid": None,
            "signature_algorithm": None,
            "hash_algorithm": None,
            "verification_message": f"PDF read failed: {exc}",
        }

    return {
        "signed": False,
        "signature_count": 0,
        "verification_status": "Not Signed",
        "signer_name": None,
        "issuer": None,
        "signing_time": None,
        "certificate_valid": None,
        "signature_algorithm": None,
        "hash_algorithm": None,
        "verification_message": "This PDF does not appear to contain a digital signature.",
    }
