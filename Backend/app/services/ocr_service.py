import easyocr

# Create OCR Reader (only once)
reader = easyocr.Reader(['en'])


def extract_text(file_path):
    """
    Extract text from image using EasyOCR
    """

    result = reader.readtext(file_path)

    extracted_text = ""

    for item in result:
        extracted_text += item[1] + "\n"

    return extracted_text