from app.ai.pdf_converter import convert_pdf_to_images
from app.ai.ocr_engine import extract_text


def process_document(file_path):
    """
    Complete AI document processing pipeline
    """

    result = {
        "images": [],
        "ocr_text": "",
        "fields": {},
        "trust_score": None
    }

    # Step 1 - Convert PDF to Images
    images = convert_pdf_to_images(
        file_path,
        "temp_images"
    )

    result["images"] = images

    # Step 2 - OCR
    text = extract_text(images)

    result["ocr_text"] = text

    return result