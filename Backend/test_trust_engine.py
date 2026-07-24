from app.services.document_pipeline import process_document

result = process_document(
    "uploads/TrustIQ_Sample_Company_Document.pdf"
)

print("=" * 60)
print("TRUSTIQ AI REPORT")
print("=" * 60)

print("Document Title :", result["fields"]["document_title"])
print("Document Type  :", result["fields"]["document_type"])
print("Purpose        :", result["fields"]["purpose"])
print()

print("Trust Score    :", result["trust_score"])
print("Status         :", result["status"])