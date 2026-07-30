import re


def classify_document(fields, original_filename=""):
    combined_text = " ".join(
        [
            (fields or {}).get("document_title", ""),
            (fields or {}).get("document_type", ""),
            (fields or {}).get("purpose", ""),
            original_filename or "",
        ]
    ).lower()

    if any(token in combined_text for token in ["invoice", "bill", "receipt"]):
        category = "Financial"
    elif any(token in combined_text for token in ["passport", "aadhaar", "id", "identity"]):
        category = "Identity"
    elif any(token in combined_text for token in ["certificate", "degree", "license"]):
        category = "Credential"
    elif any(token in combined_text for token in ["employee", "employment", "hr"]):
        category = "HR"
    else:
        category = "General"

    confidence = 0.65
    if re.search(r"invoice|passport|aadhaar|certificate|employee", combined_text):
        confidence = 0.9

    return {
        "category": category,
        "confidence": round(confidence, 2),
    }
