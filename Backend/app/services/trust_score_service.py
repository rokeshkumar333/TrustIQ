def _add_unique(items, value):
    if value and value not in items:
        items.append(value)


def calculate_ai_trust_score(report):
    report = report or {}

    ocr_results = report.get("ocr_results") or {}
    metadata_analysis = report.get("metadata_analysis") or {}
    classification = report.get("document_classification") or {}
    qr_verification = report.get("qr_verification") or {}
    ai_trust_score = report.get("ai_trust_score") or {}

    reasons = []
    positives = []
    negatives = []
    breakdown = []

    ocr_confidence = float(ocr_results.get("ocr_confidence", 0) or 0)
    ocr_text_present = bool(ocr_results.get("extracted_text") and str(ocr_results.get("extracted_text", "")).strip())
    ocr_score = round(min(25, 25 * ocr_confidence), 2)

    if ocr_text_present and ocr_confidence >= 0.8:
        _add_unique(positives, "OCR confidence is strong")
        _add_unique(reasons, "Strong OCR confidence supported the score")
        impact = "positive"
    elif ocr_text_present:
        _add_unique(negatives, "OCR confidence is moderate")
        _add_unique(reasons, "OCR confidence reduced overall confidence")
        impact = "neutral"
    else:
        _add_unique(negatives, "OCR output is limited")
        _add_unique(reasons, "OCR text was unavailable or weak")
        impact = "negative"

    breakdown.append({
        "module": "OCR",
        "score": ocr_score,
        "max_score": 25,
        "impact": impact,
        "reason": "OCR confidence and text availability affect readability and evidence quality.",
        "confidence": round(ocr_confidence, 2),
    })

    qr_confidence = float(qr_verification.get("confidence", 0) or 0)
    qr_valid = qr_verification.get("validation_result") == "Valid"
    qr_detected = bool(qr_verification.get("qr_detected"))

    if qr_valid and qr_confidence >= 0.7:
        qr_score = 20
        _add_unique(positives, "QR validation passed")
        _add_unique(reasons, "QR evidence validated successfully")
        impact = "positive"
    elif qr_detected:
        qr_score = 12
        _add_unique(negatives, "QR could not be fully validated")
        _add_unique(reasons, "QR validation was uncertain")
        impact = "neutral"
    else:
        qr_score = 10
        _add_unique(negatives, "QR is missing or invalid")
        _add_unique(reasons, "Missing or invalid QR reduced confidence")
        impact = "negative"

    breakdown.append({
        "module": "QR",
        "score": round(qr_score, 2),
        "max_score": 20,
        "impact": impact,
        "reason": "QR validation contributes trust when the content is verified and consistent.",
        "confidence": round(qr_confidence, 2),
    })

    metadata_anomalies = metadata_analysis.get("metadata_anomalies") or []
    metadata_complete = bool(metadata_analysis.get("author")) and bool(metadata_analysis.get("producer"))
    metadata_completeness = 0
    if metadata_analysis.get("creation_date"):
        metadata_completeness += 25
    if metadata_analysis.get("modification_date"):
        metadata_completeness += 25
    if metadata_analysis.get("author"):
        metadata_completeness += 25
    if metadata_analysis.get("producer"):
        metadata_completeness += 25

    metadata_score = 15 if metadata_complete and not metadata_anomalies else 10 if metadata_completeness >= 50 else 7
    if metadata_complete and not metadata_anomalies:
        _add_unique(positives, "Metadata appears complete and consistent")
        _add_unique(reasons, "Metadata completeness supported the score")
        impact = "positive"
    elif metadata_anomalies:
        _add_unique(negatives, "Metadata integrity is inconsistent")
        _add_unique(reasons, "Metadata anomalies reduced confidence")
        impact = "negative"
    else:
        _add_unique(negatives, "Metadata is incomplete")
        _add_unique(reasons, "Missing metadata lowered confidence")
        impact = "neutral"

    breakdown.append({
        "module": "Metadata",
        "score": round(metadata_score, 2),
        "max_score": 15,
        "impact": impact,
        "reason": "Metadata completeness and consistency strengthen document authenticity evidence.",
        "confidence": round(metadata_completeness / 100, 2),
    })

    classification_confidence = float(classification.get("confidence_score", 0) or 0)
    classification_score = round(min(15, 15 * classification_confidence), 2)
    if classification_confidence >= 0.8:
        _add_unique(positives, "Document classification confidence is high")
        _add_unique(reasons, "Classification confidence supported the score")
        impact = "positive"
    else:
        _add_unique(negatives, "Document classification confidence is low")
        _add_unique(reasons, "Classification confidence was moderate")
        impact = "neutral"

    breakdown.append({
        "module": "Classification",
        "score": classification_score,
        "max_score": 15,
        "impact": impact,
        "reason": "Classification confidence indicates how clearly the document type was recognized.",
        "confidence": round(classification_confidence, 2),
    })

    suspicious_patterns = report.get("fraud_detection_summary", {}).get("suspicious_patterns") or []
    integrity_penalty = 0
    if suspicious_patterns:
        integrity_penalty += min(10, len(suspicious_patterns) * 3)
    if metadata_anomalies:
        integrity_penalty += 3
    if not ocr_text_present:
        integrity_penalty += 3
    if qr_verification.get("validation_result") == "Invalid":
        integrity_penalty += 4

    integrity_score = round(max(0, 25 - integrity_penalty), 2)
    if integrity_penalty == 0:
        _add_unique(positives, "Document integrity appears consistent")
        _add_unique(reasons, "Integrity checks remained stable")
        impact = "positive"
    elif integrity_penalty < 8:
        _add_unique(negatives, "Minor integrity concerns were observed")
        _add_unique(reasons, "Some integrity factors reduced confidence")
        impact = "neutral"
    else:
        _add_unique(negatives, "Integrity concerns were observed")
        _add_unique(reasons, "Multiple integrity concerns reduced confidence")
        impact = "negative"

    breakdown.append({
        "module": "Integrity",
        "score": integrity_score,
        "max_score": 25,
        "impact": impact,
        "reason": "Integrity combines suspicious patterns, OCR consistency, and verification signals.",
        "confidence": round(max(0, 1 - (integrity_penalty / 25)), 2),
    })

    existing_score = float(ai_trust_score.get("overall_score", 0) or 0)
    overall_score = round(
        max(0, min(100, sum(item["score"] for item in breakdown) * 0.7 + existing_score * 0.3)),
        2,
    )

    if overall_score >= 90:
        risk_level = "Genuine"
        recommended_action = "Accept and archive the document"
    elif overall_score >= 75:
        risk_level = "Low Risk"
        recommended_action = "Proceed with standard review"
    elif overall_score >= 55:
        risk_level = "Medium Risk"
        recommended_action = "Escalate for manual review"
    elif overall_score >= 35:
        risk_level = "High Risk"
        recommended_action = "Review manually and investigate the document"
    else:
        risk_level = "Fraudulent"
        recommended_action = "Block the document and alert the review team"

    return {
        "overall_score": overall_score,
        "risk_level": risk_level,
        "reasons_affecting_score": reasons,
        "positive_indicators": positives,
        "negative_indicators": negatives,
        "recommended_action": recommended_action,
        "score_breakdown": breakdown,
        "confidence_breakdown": {
            "ocr_confidence": round(ocr_confidence, 2),
            "classification_confidence": round(classification_confidence, 2),
            "qr_confidence": round(qr_confidence, 2),
            "metadata_completeness": round(metadata_completeness / 100, 2),
            "processing_time_ms": report.get("processing_time_ms", 0),
        },
    }
