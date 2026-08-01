import fitz
from PIL import Image

from app.services.image_forgery_service import analyze_image_forgery


def test_analyze_image_forgery_returns_structured_result_for_missing_file():
    result = analyze_image_forgery("missing.png")

    assert isinstance(result, dict)
    assert "manipulated" in result
    assert result["manipulated"] is False
    assert 0 <= result["manipulation_score"] <= 100
    assert isinstance(result["suspected_regions"], list)
    assert isinstance(result["detected_artifacts"], list)
    assert isinstance(result["explanation"], str)


def test_analyze_image_forgery_handles_generated_image(tmp_path):
    image_path = tmp_path / "sample.png"
    image = Image.new("RGB", (400, 400), color="white")
    image.save(image_path)

    result = analyze_image_forgery(str(image_path))

    assert isinstance(result, dict)
    assert result["manipulation_score"] >= 0
    assert result["confidence"] >= 0
    assert result["confidence"] <= 1
    assert isinstance(result["detected_artifacts"], list)


def test_analyze_image_forgery_handles_generated_pdf(tmp_path):
    pdf_path = tmp_path / "sample.pdf"
    document = fitz.open()
    page = document.new_page()
    page.insert_text((72, 72), "TrustIQ forgery analysis test")
    document.save(pdf_path)
    document.close()

    result = analyze_image_forgery(str(pdf_path))

    assert isinstance(result, dict)
    assert "manipulated" in result
    assert 0 <= result["manipulation_score"] <= 100
