import re


def extract_fields(text):
    """
    Extract structured information from OCR text.
    """

    result = {
        "document_title": "",
        "document_type": "",
        "purpose": ""
    }

    if not text:
        return result

    lines = [
        line.strip()
        for line in text.split("\n")
        if line.strip()
    ]

    # Document title
    if len(lines) > 0:
        result["document_title"] = lines[0]

    # Document type
    title = result["document_title"].lower()

    if "employee" in title:
        result["document_type"] = "Employee Record"

    elif "invoice" in title:
        result["document_type"] = "Invoice"

    elif "certificate" in title:
        result["document_type"] = "Certificate"

    elif "passport" in title:
        result["document_type"] = "Passport"

    elif "aadhaar" in title:
        result["document_type"] = "Aadhaar"

    else:
        result["document_type"] = "Unknown"

    # Purpose
    match = re.search(
        r"Purpose:(.*)",
        text,
        re.IGNORECASE | re.DOTALL
    )

    if match:
        result["purpose"] = match.group(1).strip()

    return result