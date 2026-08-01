import fitz
import os


def convert_pdf_to_images(pdf_path, output_folder):

    document = fitz.open(pdf_path)
    page_count = len(document)

    print(f"[QR_DEBUG] PDF page count: {page_count}")
    image_paths = []

    os.makedirs(output_folder, exist_ok=True)

    for page_number in range(page_count):

        page = document.load_page(page_number)
        print(f"[QR_DEBUG] Converting PDF page {page_number + 1}/{page_count}")

        pix = page.get_pixmap(dpi=300)

        image_path = os.path.join(
            output_folder,
            f"page_{page_number + 1}.png"
        )

        pix.save(image_path)
        image_paths.append(image_path)
        print(f"[QR_DEBUG] Saved page image: {image_path}")

    document.close()

    return image_paths