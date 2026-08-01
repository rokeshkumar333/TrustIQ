from app.services.fraud_detection_service import analyze_fraud


def test_analyze_fraud_returns_structured_checks():
    report = {
        "verification_report": {
            "ocr_results": {
                "extracted_text": "Invoice for payroll",
                "ocr_confidence": 0.9,
            },
            "metadata_analysis": {
                "creation_date": "2024-01-01",
                "modification_date": "2024-01-02",
                "author": "Finance",
                "producer": "Adobe PDF",
                "metadata_anomalies": [],
            },
            "document_classification": {
                "confidence_score": 0.9,
            },
            "qr_verification": {
                "qr_detected": True,
                "validation_result": "Valid",
                "confidence": 0.9,
            },
        }
    }

    result = analyze_fraud(report, file_path="dummy.pdf")

    assert result["fraud_score"] >= 0
    assert result["fraud_score"] <= 100
    assert result["risk_level"] in {"Genuine", "Low Risk", "Medium Risk", "High Risk", "Fraudulent"}
    assert isinstance(result["passed_checks"], list)
    assert isinstance(result["warnings"], list)
    assert isinstance(result["failed_checks"], list)


def test_analyze_fraud_flags_missing_metadata_and_qr():
    report = {
        "verification_report": {
            "ocr_results": {"extracted_text": "", "ocr_confidence": 0.2},
            "metadata_analysis": {
                "metadata_anomalies": ["Missing author metadata"],
            },
            "document_classification": {"confidence_score": 0.4},
            "qr_verification": {"qr_detected": False, "validation_result": "Invalid", "confidence": 0.0},
        }
    }

    result = analyze_fraud(report, file_path="dummy.pdf")

    assert result["fraud_score"] >= 0
    assert any("missing" in item.lower() or "invalid" in item.lower() for item in result["negative_indicators"])
