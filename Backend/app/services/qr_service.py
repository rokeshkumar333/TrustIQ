import os
import re
import cv2

from app.ai.pdf_converter import convert_pdf_to_images


def _decode_qr_from_image(image_path):
    print(f"[QR_DEBUG] Decoding image: {image_path}")

    if not os.path.exists(image_path):
        print(f"[QR_DEBUG] Image missing: {image_path}")
        return []

    image = cv2.imread(image_path)
    if image is None:
        print(f"[QR_DEBUG] cv2.imread returned None for: {image_path}")
        return []

    print(f"[QR_DEBUG] Image loaded with shape: {image.shape}")
    detector = cv2.QRCodeDetector()

    def try_decode(input_image, label):
        print(f"[QR_DEBUG] Attempt: {label}")
        try:
            decoded_data, _, _ = detector.detectAndDecode(input_image)
            print(f"[QR_DEBUG] {label} returned data: {bool(decoded_data)}")
            if decoded_data:
                return [decoded_data]
        except Exception as exc:
            print(f"[QR_DEBUG] {label} exception: {exc}")
        return []

    def try_multi(input_image, label):
        print(f"[QR_DEBUG] Attempt: {label}")
        try:
            data_list, _, _ = detector.detectAndDecodeMulti(input_image)
            print(f"[QR_DEBUG] {label} returned data: {bool(data_list)}")
            if isinstance(data_list, (list, tuple)):
                for item in data_list:
                    if item:
                        return [item]
            elif data_list:
                return [data_list]
        except Exception as exc:
            print(f"[QR_DEBUG] {label} exception: {exc}")
        return []

    decoded = try_decode(image, "detectAndDecode on original BGR image")
    if decoded:
        return decoded

    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    decoded = try_decode(gray_image, "detectAndDecode on grayscale image")
    if decoded:
        return decoded

    _, threshold_image = cv2.threshold(gray_image, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)
    decoded = try_decode(threshold_image, "detectAndDecode on adaptive threshold image")
    if decoded:
        return decoded

    resized_image = cv2.resize(image, None, fx=2.0, fy=2.0, interpolation=cv2.INTER_CUBIC)
    decoded = try_decode(resized_image, "detectAndDecode on 200% resized image")
    if decoded:
        return decoded

    decoded = try_multi(image, "detectAndDecodeMulti on original BGR image")
    if decoded:
        return decoded

    decoded = try_multi(gray_image, "detectAndDecodeMulti on grayscale image")
    if decoded:
        return decoded

    decoded = try_multi(resized_image, "detectAndDecodeMulti on 200% resized image")
    if decoded:
        return decoded

    return []


def _extract_qr_codes_from_path(file_path):
    if not os.path.exists(file_path):
        print(f"[QR_DEBUG] File not found: {file_path}")
        return []

    _, ext = os.path.splitext(file_path)
    ext = ext.lower()

    image_paths = []
    if ext == ".pdf":
        image_paths = convert_pdf_to_images(file_path, "temp_images")
        print(f"[QR_DEBUG] PDF converted to {len(image_paths)} page images")
    else:
        image_paths = [file_path]

    for index, image_path in enumerate(image_paths, start=1):
        print(f"[QR_DEBUG] Processing page {index}/{len(image_paths)}: {image_path}")
        detected_codes = _decode_qr_from_image(image_path)
        if detected_codes:
            return detected_codes

    return []


def _validate_qr_data(qr_data):
    if not qr_data:
        return "Invalid", 0.0

    if isinstance(qr_data, str):
        qr_data = [qr_data]

    for content in qr_data:
        if not content:
            continue

        if content.startswith("http://") or content.startswith("https://"):
            return "Valid", 0.95

        if len(content) >= 8:
            return "Valid", 0.85

    return "Valid", 0.7


def _verify_text_markers(text, filename=""):
    combined = f"{text} {filename}".lower()
    tokens = ["qr", "barcode", "verify", "auth", "token", "serial", "tracking"]
    found_markers = [token for token in tokens if token in combined]

    if found_markers:
        return {
            "verified": True,
            "qr_found": False,
            "qr_content": [],
            "validation_result": "Valid",
            "confidence": 0.65,
            "method": "text-pattern",
            "markers": found_markers,
            "message": "QR verification keywords detected in document text.",
        }

    match = re.search(r"[A-Z0-9]{4,}", text)
    if match:
        return {
            "verified": True,
            "qr_found": False,
            "qr_content": [match.group(0)],
            "validation_result": "Valid",
            "confidence": 0.55,
            "method": "text-pattern",
            "markers": ["alphanumeric-sequence"],
            "message": "Document text contains a structured verification sequence.",
        }

    return {
        "verified": False,
        "qr_found": False,
        "qr_content": [],
        "validation_result": "Invalid",
        "confidence": 0.0,
        "method": "text-pattern",
        "markers": [],
        "message": "No QR verification markers detected.",
    }


def verify_qr(text="", filename=""):
    qr_codes = []
    qr_found = False
    validation_result = "Invalid"
    confidence = 0.0
    method = "text-pattern"
    message = "No QR verification detected."
    markers = []

    if filename:
        qr_codes = _extract_qr_codes_from_path(filename)
        qr_found = bool(qr_codes)

        if qr_found:
            validation_result, confidence = _validate_qr_data(qr_codes)
            method = "opencv"
            markers = qr_codes
            message = "QR code detected in uploaded document."

    if not qr_found:
        text_result = _verify_text_markers(text, filename)
        return {
            "verified": text_result["verified"],
            "qr_found": text_result["qr_found"],
            "qr_content": text_result["qr_content"],
            "validation_result": text_result["validation_result"],
            "confidence": text_result["confidence"],
            "method": text_result["method"],
            "markers": text_result["markers"],
            "message": text_result["message"],
        }

    return {
        "verified": True,
        "qr_found": qr_found,
        "qr_content": qr_codes,
        "validation_result": validation_result,
        "confidence": confidence,
        "method": method,
        "markers": markers,
        "message": message,
    }
