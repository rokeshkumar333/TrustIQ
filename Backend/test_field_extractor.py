from app.services.document_pipeline import process_document

result = process_document(
    "uploads/TrustIQ_Sample_Company_Document.pdf"
)

print("=" * 60)
print("OCR TEXT")
print("=" * 60)

print(result["ocr_text"])

print()

print("=" * 60)
print("FIELDS")
print("=" * 60)

print(result["fields"])