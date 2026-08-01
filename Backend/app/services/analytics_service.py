from collections import Counter


def build_analytics_summary(documents):
    status_counts = Counter(str(doc.get("status", "Not Processed") or "Not Processed") for doc in documents)

    signature_counts = {
        "total_signed_documents": 0,
        "valid_signatures": 0,
        "invalid_signatures": 0,
        "unsigned_documents": 0,
        "expired_certificates": 0,
    }

    forgery_counts = {
        "total_manipulated_documents": 0,
        "forgery_detection_rate": 0,
        "manipulation_percentage": 0,
    }

    for doc in documents:
        sig = (doc.get("signature_verification") or {})
        if sig.get("signed"):
            signature_counts["total_signed_documents"] += 1
            if sig.get("verification_status") == "Valid":
                signature_counts["valid_signatures"] += 1
            else:
                signature_counts["invalid_signatures"] += 1
            if sig.get("certificate_valid") is False:
                signature_counts["expired_certificates"] += 1
        else:
            signature_counts["unsigned_documents"] += 1

        image_forgery = (doc.get("image_forgery_analysis") or (doc.get("verification_report") or {}).get("image_forgery_analysis") or {})
        if image_forgery.get("manipulated"):
            forgery_counts["total_manipulated_documents"] += 1

    score_values = [int(doc.get("trust_score", 0) or 0) for doc in documents]
    if score_values:
        average_score = round(sum(score_values) / len(score_values))
        max_score = max(score_values)
        min_score = min(score_values)
    else:
        average_score = 0
        max_score = 0
        min_score = 0

    if documents:
        forgery_counts["forgery_detection_rate"] = round((forgery_counts["total_manipulated_documents"] / len(documents)) * 100, 2)
        forgery_counts["manipulation_percentage"] = round((forgery_counts["total_manipulated_documents"] / len(documents)) * 100, 2)

    return {
        "total_documents": len(documents),
        "average_score": average_score,
        "max_score": max_score,
        "min_score": min_score,
        "status_breakdown": dict(status_counts),
        "signature_metrics": signature_counts,
        "forgery_metrics": forgery_counts,
    }
