from app.ai.pdf_converter import convert_pdf_to_images
from app.ai.ocr_engine import extract_text
from app.ai.field_extractor import extract_fields
from app.ai.trust_score import calculate_trust_score
from app.services.qr_service import verify_qr


def process_document(file_path):

    result = {
        "images": [],
        "ocr_text": "",
        "fields": {},
        "trust_score": 0,
        "status": ""
    }

    # PDF → Image
    images = convert_pdf_to_images(
        file_path,
        "temp_images"
    )

    result["images"] = images

    # OCR
    text = extract_text(images)

    result["ocr_text"] = text

    # Field Extraction
    fields = extract_fields(text)

    result["fields"] = fields

    # Trust Score
    trust = calculate_trust_score(fields)

    result["trust_score"] = trust["trust_score"]
    result["status"] = trust["status"]

    qr_result = verify_qr(text, file_path)
    result["qr_verification"] = qr_result

    return result