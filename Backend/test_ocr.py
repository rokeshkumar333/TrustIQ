from app.ai.pdf_converter import convert_pdf_to_images
from app.ai.ocr_engine import extract_text


def process_document(pdf_path):
    """
    Complete AI document processing pipeline.
    """

    print("=" * 60)
    print("TrustIQ AI Pipeline Started")
    print("=" * 60)

    # Step 1: Convert PDF into images
    images = convert_pdf_to_images(
        pdf_path,
        "temp_images"
    )

    print(f"Pages Converted : {len(images)}")

    # Step 2: OCR
    extracted_text = extract_text(images)

    print("OCR Completed")

    result = {
        "images": images,
        "text": extracted_text
    }

    print("=" * 60)

    return result