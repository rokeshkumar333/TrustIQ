import os
import re
from datetime import datetime

from app.ai.field_extractor import extract_fields
from app.ai.trust_score import calculate_trust_score
from app.services.classification_service import classify_document


def _normalize_text(value):
    if value is None:
        return ""
    if isinstance(value, (list, tuple)):
        return " | ".join(str(item) for item in value if item)
    return str(value)


def _format_file_size(file_path):
    if not file_path or not os.path.exists(file_path):
        return "Unavailable"

    size_bytes = os.path.getsize(file_path)
    if size_bytes < 1024:
        return f"{size_bytes} bytes"
    if size_bytes < 1024 * 1024:
        return f"{round(size_bytes / 1024, 1)} KB"
    return f"{round(size_bytes / (1024 * 1024), 1)} MB"


def _extract_pdf_metadata(file_path):
    if not file_path or not os.path.exists(file_path):
        return {}

    _, extension = os.path.splitext(file_path)
    if extension.lower() != ".pdf":
        return {}

    try:
        from PyPDF2 import PdfReader
    except Exception:
        return {}

    try:
        reader = PdfReader(file_path)
        metadata = reader.metadata or {}
    except Exception:
        return {}

    if not metadata:
        return {}

    def get_value(key):
        value = getattr(metadata, key, None)
        return _normalize_text(value)

    return {
        "title": get_value("title"),
        "author": get_value("author"),
        "creator": get_value("creator"),
        "producer": get_value("producer"),
        "creation_date": get_value("creation_date"),
        "modification_date": get_value("modification_date"),
    }


def _detect_language(text):
    if not text:
        return "Unknown"
    ascii_letters = sum(1 for char in text if char.isalpha())
    if ascii_letters == 0:
        return "Unknown"
    if len(text) < 20:
        return "English"
    return "English"


def _build_anomalies(metadata, ocr_text, fields, qr_verification):
    anomalies = []

    if not metadata:
        anomalies.append("No embedded PDF metadata found")

    if not metadata.get("creation_date"):
        anomalies.append("Missing creation date")

    if not metadata.get("modification_date"):
        anomalies.append("Missing modification date")

    if not metadata.get("author"):
        anomalies.append("Missing author metadata")

    if not metadata.get("producer"):
        anomalies.append("Missing producer metadata")

    if ocr_text and not fields.get("document_title"):
        anomalies.append("OCR text present but title extraction failed")

    if qr_verification.get("validation_result") == "Invalid":
        anomalies.append("QR validation failed")

    if qr_verification.get("qr_found") is False and not ocr_text:
        anomalies.append("No QR or readable OCR evidence detected")

    return anomalies


def build_verification_report(document, file_path=None):
    document = document or {}

    ocr_text = _normalize_text(document.get("ocr_text"))
    fields = document.get("fields") or {}
    if not fields and ocr_text:
        fields = extract_fields(ocr_text)

    original_filename = _normalize_text(document.get("original_filename"))
    file_type = _normalize_text(document.get("file_type")) or "unknown"
    uploaded_at = _normalize_text(document.get("uploaded_at")) or "Not available"
    resolved_path = file_path or document.get("file_path")

    pdf_metadata = _extract_pdf_metadata(resolved_path)
    qr_verification = document.get("qr_verification") or {}
    classification = classify_document(fields, original_filename)
    trust_result = calculate_trust_score(fields)

    base_score = int(document.get("trust_score", trust_result.get("trust_score", 0)))
    score = max(0, min(100, base_score))

    if qr_verification.get("validated") or qr_verification.get("verification_result") == "Valid":
        score += 5
    if qr_verification.get("validation_result") == "Invalid":
        score -= 20
    if qr_verification.get("qr_found"):
        score += 5
    if not pdf_metadata:
        score -= 10
    if not fields.get("document_title"):
        score -= 10

    score = max(0, min(100, score))

    suspicious_indicators = []
    if score < 60:
        suspicious_indicators.append("Trust score is below the review threshold")
    if qr_verification.get("validation_result") == "Invalid":
        suspicious_indicators.append("QR validation failed")
    if not pdf_metadata.get("author") or not pdf_metadata.get("producer"):
        suspicious_indicators.append("Missing document metadata")
    if ocr_text and not fields.get("document_title"):
        suspicious_indicators.append("OCR text lacks strong structural extraction")

    anomalies = _build_anomalies(pdf_metadata, ocr_text, fields, qr_verification)

    if score < 40 or (qr_verification.get("validation_result") == "Invalid" and score < 60):
        final_decision = "Fraudulent"
    elif suspicious_indicators or anomalies:
        final_decision = "Suspicious"
    else:
        final_decision = "Genuine"

    risk_level = "Low"
    if score < 70:
        risk_level = "Medium"
    if score < 50:
        risk_level = "High"

    return {
        "document_information": {
            "file_name": original_filename or os.path.basename(resolved_path or "unknown"),
            "file_type": file_type.upper() if file_type else "UNKNOWN",
            "upload_date": uploaded_at,
            "file_size": _format_file_size(resolved_path),
        },
        "ocr_results": {
            "extracted_text": ocr_text or "No OCR text available for this document.",
            "ocr_confidence": round(0.82 if ocr_text else 0.34, 2),
            "detected_language": _detect_language(ocr_text),
        },
        "metadata_analysis": {
            "pdf_metadata": pdf_metadata or {"status": "No embedded metadata detected"},
            "creation_date": pdf_metadata.get("creation_date", "Not available"),
            "modification_date": pdf_metadata.get("modification_date", "Not available"),
            "author": pdf_metadata.get("author", "Not available"),
            "producer": pdf_metadata.get("producer", "Not available"),
            "metadata_anomalies": anomalies,
        },
        "document_classification": {
            "predicted_document_type": fields.get("document_type") or classification.get("category", "General"),
            "confidence_score": classification.get("confidence", 0.0),
        },
        "qr_verification": {
            "qr_detected": bool(qr_verification.get("qr_found")),
            "qr_content": qr_verification.get("qr_content") or [],
            "validation_result": qr_verification.get("validation_result") or "Invalid",
            "confidence": qr_verification.get("confidence", 0.0),
            "detection_method": qr_verification.get("method") or "text-pattern",
        },
        "ai_trust_score": {
            "overall_score": score,
            "risk_level": risk_level,
            "suspicious_indicators": suspicious_indicators,
            "confidence": round(min(0.99, 0.65 + (score / 100) * 0.3), 2),
        },
        "fraud_detection_summary": {
            "tampering_indicators": [
                item for item in anomalies if "metadata" in item.lower() or "OCR" in item
            ],
            "missing_metadata": [
                item for item in anomalies if "missing" in item.lower() or "metadata" in item.lower()
            ],
            "ocr_inconsistencies": [
                item for item in anomalies if "OCR" in item
            ],
            "invalid_qr": [
                item for item in anomalies if "QR" in item
            ],
            "suspicious_patterns": suspicious_indicators,
        },
        "final_decision": final_decision,
    }
