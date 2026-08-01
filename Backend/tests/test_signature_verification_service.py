from app.services.signature_verification_service import inspect_pdf_signature


def test_inspect_pdf_signature_returns_structured_result_for_missing_file():
    result = inspect_pdf_signature("missing.pdf")

    assert result["signed"] is False
    assert result["signature_count"] == 0
    assert result["verification_status"] in {"Unsupported", "Not Signed"}
    assert "verification_message" in result


def test_inspect_pdf_signature_returns_structured_result_for_pdf_file():
    result = inspect_pdf_signature("sample.pdf")

    assert result["signed"] is False
    assert result["signature_count"] == 0
    assert result["verification_status"] in {"Unsupported", "Not Signed"}
