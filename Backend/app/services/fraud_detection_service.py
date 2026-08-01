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
        return None


def analyze_fraud(document, file_path=None):
    document = document or {}
    report = document.get("verification_report") or {}
    metadata_analysis = report.get("metadata_analysis") or {}
    ocr_results = report.get("ocr_results") or {}
    qr_verification = report.get("qr_verification") or {}
    classification = report.get("document_classification") or {}

    passed_checks = []
    warnings = []
    failed_checks = []

    if metadata_analysis.get("author"):
        passed_checks.append("Author metadata present")
    else:
        warnings.append("Author metadata missing")

    if metadata_analysis.get("producer"):
        passed_checks.append("Producer metadata present")
    else:
        warnings.append("Producer metadata missing")

    if metadata_analysis.get("creation_date") and metadata_analysis.get("modification_date"):
        creation_dt = _parse_date(metadata_analysis.get("creation_date"))
        modification_dt = _parse_date(metadata_analysis.get("modification_date"))
        if creation_dt and modification_dt and creation_dt > modification_dt:
            failed_checks.append("Creation date is later than modification date")
        else:
            passed_checks.append("Timestamps appear consistent")
    else:
        warnings.append("Timestamp metadata incomplete")

    if metadata_analysis.get("metadata_anomalies"):
        failed_checks.extend(metadata_analysis.get("metadata_anomalies", [])[:3])

    ocr_text = _normalize_text(ocr_results.get("extracted_text"))
    ocr_confidence = float(ocr_results.get("ocr_confidence", 0) or 0)
    if ocr_text and ocr_confidence >= 0.8:
        passed_checks.append("OCR output appears readable")
    elif ocr_text:
        warnings.append("OCR confidence is moderate")
    else:
        failed_checks.append("OCR text is empty or unavailable")

    suspicious_tokens = ["tampered", "edited", "forged", "fake", "fraud", "altered"]
    if any(token in ocr_text.lower() for token in suspicious_tokens):
        failed_checks.append("OCR text contains suspicious wording")

    garbled = bool(re.search(r"[^\w\s.,;:()/-]{3,}", ocr_text))
    if garbled:
        warnings.append("OCR output contains unusual characters")

    qr_detected = bool(qr_verification.get("qr_detected"))
    qr_result = qr_verification.get("validation_result") or "Invalid"
    if qr_detected and qr_result == "Valid":
        passed_checks.append("QR verification passed")
    elif qr_detected and qr_result != "Valid":
        warnings.append("QR verification is uncertain")
    else:
        warnings.append("No QR verification evidence found")

    if qr_result == "Invalid":
        warnings.append("QR validation failed")

    if classification.get("confidence_score", 0) >= 0.8:
        passed_checks.append("Classification confidence is high")
    else:
        warnings.append("Classification confidence is moderate")

    file_path = file_path or document.get("file_path")
    if file_path and os.path.exists(file_path):
        size = os.path.getsize(file_path)
        if size > 0:
            passed_checks.append("Document file exists")
        else:
            failed_checks.append("Document file is empty")
    else:
        warnings.append("Document file path unavailable")

    if not os.path.splitext(file_path or "")[1].lower() in {".pdf", ".png", ".jpg", ".jpeg"}:
        warnings.append("Document extension is unusual")

    fraud_score = 0
    if failed_checks:
        fraud_score += min(60, len(failed_checks) * 8)
    if warnings:
        fraud_score += min(25, len(warnings) * 3)

    fraud_score = max(0, min(100, 100 - (100 - fraud_score)))

    if fraud_score >= 80:
        risk_level = "Fraudulent"
        recommended_action = "Block the document and alert the review team"
    elif fraud_score >= 60:
        risk_level = "High Risk"
        recommended_action = "Reject and investigate the file"
    elif fraud_score >= 35:
        risk_level = "Medium Risk"
        recommended_action = "Escalate for manual review"
    elif fraud_score >= 15:
        risk_level = "Low Risk"
        recommended_action = "Proceed with caution"
    else:
        risk_level = "Genuine"
        recommended_action = "Accept the document"

    return {
        "fraud_score": round(fraud_score, 2),
        "risk_level": risk_level,
        "fraud_indicators": failed_checks + warnings,
        "positive_indicators": passed_checks,
        "negative_indicators": failed_checks + warnings,
        "recommended_action": recommended_action,
        "confidence": round(min(0.99, 0.65 + (100 - fraud_score) / 100 * 0.3), 2),
        "passed_checks": passed_checks,
        "warnings": warnings,
        "failed_checks": failed_checks,
    }
