def calculate_trust_score(fields):
    """
    Calculate trust score based on extracted fields.
    """

    score = 0

    if fields.get("document_title"):
        score += 30

    if fields.get("document_type") != "Unknown":
        score += 30

    if fields.get("purpose"):
        score += 40

    if score >= 80:
        status = "Verified"
    elif score >= 50:
        status = "Needs Manual Review"
    else:
        status = "Rejected"

    return {
        "trust_score": score,
        "status": status
    }