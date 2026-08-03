from app.services.document_similarity_service import analyze_document_similarity


def test_analyze_document_similarity_returns_structured_result_for_no_match():
    result = analyze_document_similarity(
        {
            "id": 1,
            "file_path": "missing.pdf",
            "ocr_text": "Unique invoice for trustiq",
            "fields": {"document_title": "Invoice"},
        },
        existing_documents=[
            {
                "id": 2,
                "file_path": "missing2.pdf",
                "ocr_text": "Different contract",
                "fields": {"document_title": "Contract"},
            }
        ],
    )

    assert isinstance(result, dict)
    assert "duplicate" in result
    assert "similarity_score" in result
    assert result["similarity_score"] >= 0
    assert isinstance(result["matching_sections"], list)
    assert isinstance(result["explanation"], str)


def test_analyze_document_similarity_detects_identical_documents(tmp_path):
    file_path = tmp_path / "duplicate.pdf"
    file_path.write_bytes(b"duplicate-content")

    result = analyze_document_similarity(
        {
            "id": 3,
            "file_path": str(file_path),
            "ocr_text": "Identical report",
            "fields": {"document_title": "Report"},
        },
        existing_documents=[
            {
                "id": 4,
                "file_path": str(file_path),
                "ocr_text": "Identical report",
                "fields": {"document_title": "Report"},
            }
        ],
    )

    assert result["duplicate"] is True
    assert result["exact_match"] is True
    assert result["similarity_score"] >= 90
