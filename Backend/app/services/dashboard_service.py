from datetime import datetime


def build_dashboard_summary(documents):
    total_documents = len(documents)
    average_trust_score = 0

    if total_documents:
        average_trust_score = round(
            sum(doc.get("trust_score", 0) for doc in documents) / total_documents
        )

    suspicious_documents = sum(
        1 for doc in documents if str(doc.get("status", "")).lower() != "verified"
    )

    today_uploads = 0
    today = datetime.utcnow().date()
    for doc in documents:
        uploaded_at = doc.get("uploaded_at")
        if not uploaded_at:
            continue

        try:
            if isinstance(uploaded_at, str):
                parsed = datetime.fromisoformat(uploaded_at.replace(" ", "T"))
            else:
                parsed = uploaded_at
            if parsed.date() == today:
                today_uploads += 1
        except ValueError:
            continue

    return {
        "total_documents": total_documents,
        "average_trust_score": average_trust_score,
        "suspicious_documents": suspicious_documents,
        "today_uploads": today_uploads,
    }
