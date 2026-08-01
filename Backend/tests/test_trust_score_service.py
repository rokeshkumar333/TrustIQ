from app.services.trust_score_service import calculate_ai_trust_score


def test_calculate_ai_trust_score_returns_structured_analysis():
    report = {
        "ocr_results": {
            "extracted_text": "Invoice for payroll",
            "ocr_confidence": 0.91,
            "detected_language": "English",
        },
        "metadata_analysis": {
            "creation_date": "2024-01-02",
            "modification_date": "2024-01-03",
            "author": "Finance",
            "producer": "Adobe PDF",
            "metadata_anomalies": [],
        },
        "document_classification": {
            "confidence_score": 0.95,
        },
        "qr_verification": {
            "qr_detected": True,
            "validation_result": "Valid",
            "confidence": 0.96,
        },
        "ai_trust_score": {
            "overall_score": 70,
            "confidence": 0.7,
        },
    }

    result = calculate_ai_trust_score(report)

    assert result["overall_score"] >= 0
    assert result["overall_score"] <= 100
    assert result["risk_level"] in {
        "Genuine",
        "Low Risk",
        "Medium Risk",
        "High Risk",
        "Fraudulent",
    }
    assert isinstance(result["reasons_affecting_score"], list)
    assert isinstance(result["positive_indicators"], list)
    assert isinstance(result["negative_indicators"], list)
    assert result["recommended_action"]
