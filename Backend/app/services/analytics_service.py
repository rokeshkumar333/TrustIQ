from collections import Counter


def build_analytics_summary(documents):
    status_counts = Counter(str(doc.get("status", "Not Processed") or "Not Processed") for doc in documents)

    score_values = [int(doc.get("trust_score", 0) or 0) for doc in documents]
    if score_values:
        average_score = round(sum(score_values) / len(score_values))
        max_score = max(score_values)
        min_score = min(score_values)
    else:
        average_score = 0
        max_score = 0
        min_score = 0

    return {
        "total_documents": len(documents),
        "average_score": average_score,
        "max_score": max_score,
        "min_score": min_score,
        "status_breakdown": dict(status_counts),
    }
