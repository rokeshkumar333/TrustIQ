import hashlib
import os
import re
import tempfile
from typing import Any

import numpy as np
from PIL import Image

from app.ai.pdf_converter import convert_pdf_to_images


def _normalize_text(value):
    if value is None:
        return ""
    if isinstance(value, (list, tuple)):
        return " | ".join(str(item) for item in value if item)
    return str(value).strip()


def _tokenize(text):
    return [token for token in re.findall(r"\b\w+\b", (_normalize_text(text) or "").lower()) if len(token) > 2]


def _jaccard_similarity(left, right):
    left_tokens = set(_tokenize(left))
    right_tokens = set(_tokenize(right))
    if not left_tokens and not right_tokens:
        return 0.0
    union = left_tokens | right_tokens
    if not union:
        return 0.0
    return round(len(left_tokens & right_tokens) / len(union), 4)


def _value_similarity(left, right):
    left_val = _normalize_text(left).lower()
    right_val = _normalize_text(right).lower()
    if not left_val and not right_val:
        return 0.0
    if left_val and right_val and left_val == right_val:
        return 1.0
    return 0.0


def _mapping_similarity(left_mapping, right_mapping):
    left_items = left_mapping or {}
    right_items = right_mapping or {}
    if not left_items and not right_items:
        return 0.0
    keys = sorted(set(left_items.keys()) | set(right_items.keys()))
    if not keys:
        return 0.0
    matches = 0
    for key in keys:
        if _value_similarity(left_items.get(key), right_items.get(key)) > 0.0:
            matches += 1
    return round(matches / len(keys), 4)


def _calculate_file_hash(file_path):
    if not file_path or not os.path.exists(file_path):
        return None
    hasher = hashlib.sha256()
    with open(file_path, "rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            hasher.update(chunk)
    return hasher.hexdigest()


def _compute_perceptual_hash(file_path):
    if not file_path or not os.path.exists(file_path):
        return []

    extension = os.path.splitext(file_path)[1].lower()
    if extension == ".pdf":
        temp_dir = None
        try:
            temp_dir = tempfile.mkdtemp(prefix="trustiq_similarity_", dir=os.path.dirname(file_path) or None)
            image_paths = convert_pdf_to_images(file_path, temp_dir)
            if not image_paths:
                return []
            hashes = []
            for image_path in image_paths:
                hashes.append(_compute_perceptual_hash(image_path))
            return [item for sublist in hashes for item in sublist]
        finally:
            if temp_dir and os.path.isdir(temp_dir):
                import shutil
                shutil.rmtree(temp_dir, ignore_errors=True)

    try:
        image = Image.open(file_path).convert("L")
    except Exception:
        return []

    resized = image.resize((8, 8), Image.Resampling.LANCZOS)
    pixels = np.array(resized, dtype=np.float32)
    mean_value = float(np.mean(pixels))
    bits = "".join("1" if pixel >= mean_value else "0" for pixel in pixels.flatten())
    return [int(bit) for bit in bits]


def _hamming_similarity(left_bits, right_bits):
    if not left_bits or not right_bits:
        return 0.0
    length = min(len(left_bits), len(right_bits))
    if length == 0:
        return 0.0
    distance = sum(1 for idx in range(length) if left_bits[idx] != right_bits[idx])
    return round(1 - (distance / max(1, length)), 4)


def _compare_perceptual_hashes(left_path, right_path):
    left_hashes = _compute_perceptual_hash(left_path)
    right_hashes = _compute_perceptual_hash(right_path)
    if not left_hashes or not right_hashes:
        return 0.0
    if len(left_hashes) != len(right_hashes):
        length = min(len(left_hashes), len(right_hashes))
        left_hashes = left_hashes[:length]
        right_hashes = right_hashes[:length]
    return _hamming_similarity(left_hashes, right_hashes)


def analyze_document_similarity(document, existing_documents=None, current_report=None):
    document = document or {}
    current_report = current_report or {}
    current_file_path = document.get("file_path")
    current_ocr_text = _normalize_text(document.get("ocr_text") or (current_report.get("ocr_results") or {}).get("extracted_text"))
    current_fields = document.get("fields") or {}
    current_metadata = (current_report.get("metadata_analysis") or {})
    current_pdf_metadata = current_metadata.get("pdf_metadata") or {}
    current_hash = _calculate_file_hash(current_file_path)

    candidate_documents = existing_documents or []
    best_match = None
    best_score = 0.0

    for candidate in candidate_documents:
        if not candidate:
            continue
        candidate_id = candidate.get("id")
        if candidate_id is not None and document.get("id") is not None and candidate_id == document.get("id"):
            continue

        candidate_file_path = candidate.get("file_path")
        candidate_ocr_text = _normalize_text(candidate.get("ocr_text") or "")
        candidate_fields = candidate.get("fields") or {}
        candidate_hash = _calculate_file_hash(candidate_file_path)

        ocr_similarity = _jaccard_similarity(current_ocr_text, candidate_ocr_text)
        metadata_similarity = 0.0
        metadata_values = {}
        candidate_metadata = {}
        if current_pdf_metadata:
            metadata_values = {
                "title": current_pdf_metadata.get("title") or current_metadata.get("title") or "",
                "author": current_metadata.get("author") or current_pdf_metadata.get("author") or "",
                "producer": current_metadata.get("producer") or current_pdf_metadata.get("producer") or "",
                "creation_date": current_metadata.get("creation_date") or current_pdf_metadata.get("creation_date") or "",
                "modification_date": current_metadata.get("modification_date") or current_pdf_metadata.get("modification_date") or "",
            }
        if candidate.get("verification_report"):
            candidate_metadata = candidate.get("verification_report", {}).get("metadata_analysis", {}) or {}
        if candidate.get("fields"):
            candidate_metadata.update({
                "author": candidate_metadata.get("author") or candidate.get("fields", {}).get("author") or "",
                "producer": candidate_metadata.get("producer") or candidate.get("fields", {}).get("producer") or "",
            })
        if metadata_values and candidate_metadata:
            metadata_similarity = _mapping_similarity(metadata_values, {
                "title": candidate_metadata.get("title") or candidate.get("original_filename") or "",
                "author": candidate_metadata.get("author") or candidate.get("fields", {}).get("author") or "",
                "producer": candidate_metadata.get("producer") or candidate.get("fields", {}).get("producer") or "",
                "creation_date": candidate_metadata.get("creation_date") or "",
                "modification_date": candidate_metadata.get("modification_date") or "",
            })

        field_similarity = _mapping_similarity(current_fields, candidate_fields)
        hash_similarity = 1.0 if current_hash and candidate_hash and current_hash == candidate_hash else 0.0
        perceptual_similarity = _compare_perceptual_hashes(current_file_path, candidate_file_path)

        overall_similarity = round(
            (ocr_similarity * 0.3) + (metadata_similarity * 0.2) + (field_similarity * 0.2) + (hash_similarity * 0.15) + (perceptual_similarity * 0.15),
            4,
        )

        if hash_similarity == 1.0:
            overall_similarity = 1.0

        matching_sections = []
        if ocr_similarity >= 0.6:
            matching_sections.append("OCR text")
        if metadata_similarity >= 0.5:
            matching_sections.append("Metadata")
        if field_similarity >= 0.5:
            matching_sections.append("Extracted fields")
        if hash_similarity == 1.0:
            matching_sections.append("File hash")
        if perceptual_similarity >= 0.6:
            matching_sections.append("Image perceptual hash")

        if not matching_sections and overall_similarity >= 0.4:
            matching_sections.append("Content overlap")

        if overall_similarity > best_score:
            best_score = overall_similarity
            best_match = {
                "document_id": candidate.get("id"),
                "filename": candidate.get("original_filename") or candidate.get("stored_filename") or "Unknown",
                "similarity_score": round(overall_similarity * 100, 2),
                "matching_sections": matching_sections,
            }

    if best_match is None or best_score < 0.4:
        return {
            "duplicate": False,
            "exact_match": False,
            "similarity_score": 0.0,
            "matched_document_id": None,
            "matched_filename": None,
            "matching_sections": [],
            "confidence": 0.1,
            "explanation": "No meaningful duplicate or near-duplicate document was detected.",
        }

    exact_match = best_score >= 0.99 or (current_hash and best_match.get("document_id") and best_score >= 0.95 and current_hash == _calculate_file_hash(next((item.get("file_path") for item in candidate_documents if item.get("id") == best_match["document_id"]), None)))
    duplicate = exact_match or best_score >= 80

    if exact_match:
        explanation = "The document matches an existing file exactly and appears to be a duplicate upload."
    elif best_score >= 95:
        explanation = "The document is highly similar to an existing document and is likely a near duplicate."
    elif best_score >= 80:
        explanation = "The document shares strong OCR, metadata, and content characteristics with an existing document."
    else:
        explanation = "The document shows moderate overlap with an existing document but is not a strong duplicate candidate."

    return {
        "duplicate": duplicate,
        "exact_match": exact_match,
        "similarity_score": round(best_score * 100, 2),
        "matched_document_id": best_match["document_id"],
        "matched_filename": best_match["filename"],
        "matching_sections": best_match["matching_sections"],
        "confidence": round(min(0.99, 0.55 + (best_score * 0.4)), 2),
        "explanation": explanation,
    }
