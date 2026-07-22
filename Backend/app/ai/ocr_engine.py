import os
import cv2
import pytesseract

pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"


def preprocess_image(image_path):
    image = cv2.imread(image_path)

    if image is None:
        raise Exception(f"Unable to read image: {image_path}")

    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    gray = cv2.GaussianBlur(gray, (3, 3), 0)

    _, thresh = cv2.threshold(
        gray,
        0,
        255,
        cv2.THRESH_BINARY + cv2.THRESH_OTSU
    )

    return thresh


def extract_text(image_paths):

    if isinstance(image_paths, str):
        image_paths = [image_paths]

    final_text = ""

    for image_path in image_paths:

        if not os.path.exists(image_path):
            print(f"File not found: {image_path}")
            continue

        processed = preprocess_image(image_path)

        text = pytesseract.image_to_string(
            processed,
            lang="eng",
            config="--oem 3 --psm 6"
        )

        final_text += text
        final_text += "\n"

    return final_text.strip()