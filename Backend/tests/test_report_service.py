from app.services.report_service import build_verification_report


def test_build_verification_report_includes_unified_sections():
    document = {
        "id": 1,
        "original_filename": "invoice.pdf",
        "file_type": "pdf",
        "uploaded_at": "2026-08-01 11:00:00",
        "ocr_text": "Invoice\nPurpose: Payroll",
        "trust_score": 80,
        "status": "Verified",
        "fields": {
            "document_title": "Invoice",
            "document_type": "Invoice",
            "purpose": "Payroll"
        },
        "qr_verification": {
            "verified": True,
            "qr_found": True,
            "qr_content": ["https://verify.example"],
            "validation_result": "Valid",
            "confidence": 0.95,
            "method": "opencv"
        }
    }

    report = build_verification_report(document, file_path="dummy.pdf")

    assert report["document_information"]["file_name"] == "invoice.pdf"
    assert report["ocr_results"]["extracted_text"].startswith("Invoice")
    assert report["document_classification"]["predicted_document_type"] == "Invoice"
    assert report["qr_verification"]["qr_detected"] is True
    assert report["ai_trust_score"]["overall_score"] >= 0
    assert report["final_decision"] in {"Genuine", "Suspicious", "Fraudulent"}
