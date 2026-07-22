from app.ai.pdf_converter import convert_pdf_to_images

images = convert_pdf_to_images(
    "uploads/TrustIQ_Sample_Company_Document.pdf",
    "temp_images"
)

print(images)