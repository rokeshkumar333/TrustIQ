import os
import shutil
import tempfile
from io import BytesIO

import numpy as np
from PIL import Image, ImageChops, ImageFilter

from app.ai.pdf_converter import convert_pdf_to_images

_SUPPORTED_EXTENSIONS = {".pdf", ".jpg", ".jpeg", ".png"}


def _default_result(message="No supported image input was available for forgery inspection."):
    return {
        "manipulated": False,
        "confidence": 0.1,
        "manipulation_score": 0,
        "suspected_regions": [],
        "detected_artifacts": [],
        "explanation": message,
    }


def _ratio_score(value, threshold, weight):
    return min(weight, max(0, value / threshold * weight)) if threshold else 0


def _analyze_single_image(image_path):
    if not image_path or not os.path.exists(image_path):
        return _default_result("The provided file could not be read for forgery inspection.")

    image = Image.open(image_path).convert("RGB")
    width, height = image.size
    gray = np.array(image.convert("L"), dtype=np.float32)

    artifacts = []
    regions = []

    resolution_ratio = max(width, height) / max(1, min(width, height))
    if resolution_ratio > 3 or min(width, height) < 120:
        artifacts.append("Resolution or aspect-ratio inconsistencies were detected.")
        regions.append({"label": "Resolution anomaly", "x": 0, "y": 0, "width": width, "height": height})

    blur_variance = float(np.var(gray))
    if blur_variance < 1600:
        artifacts.append("The image appears blurred or softened.")
        regions.append({"label": "Blurred region", "x": width // 4, "y": height // 4, "width": width // 2, "height": height // 2})

    quarters = []
    for y0 in range(0, height, height // 2):
        for x0 in range(0, width, width // 2):
            x1 = min(width, x0 + max(1, width // 2))
            y1 = min(height, y0 + max(1, height // 2))
            if x1 <= x0 or y1 <= y0:
                continue
            quarter = gray[y0:y1, x0:x1]
            quarters.append((x0, y0, quarter))

    if len(quarters) >= 4:
        stds = [float(np.std(q[2])) for q in quarters]
        if max(stds) - min(stds) > 120:
            artifacts.append("Noise variance differs significantly across regions.")
            regions.append({"label": "Noise inconsistency", "x": quarters[0][0], "y": quarters[0][1], "width": max(1, width // 2), "height": max(1, height // 2)})

    edge_map = np.abs(np.diff(gray, axis=0)) + np.abs(np.diff(gray, axis=1))
    if edge_map.size:
        edge_density = float(np.mean(edge_map > 25))
        if edge_density < 0.06:
            artifacts.append("Edge consistency is weak or irregular.")
            regions.append({"label": "Edge inconsistency", "x": width // 3, "y": height // 3, "width": width // 3, "height": height // 3})

    resized = image.resize((256, 256), Image.Resampling.LANCZOS)
    buffer = BytesIO()
    resized.save(buffer, format="JPEG", quality=90)
    buffer.seek(0)
    recompressed = Image.open(buffer).convert("RGB")
    difference = ImageChops.difference(resized, recompressed)
    ela_array = np.array(difference).astype(np.float32)
    ela_score = float(np.mean(np.abs(ela_array)) / 255.0)
    if ela_score > 0.05:
        artifacts.append("Error Level Analysis suggests local editing or recompression.")
        regions.append({"label": "Possible edited region", "x": width // 5, "y": height // 5, "width": width // 2, "height": height // 2})

    if width >= 64 and height >= 64:
        block_size = max(8, min(16, width // 16))
        block_means = []
        for y in range(0, height - block_size + 1, block_size):
            for x in range(0, width - block_size + 1, block_size):
                region_patch = gray[y:y + block_size, x:x + block_size]
                block_means.append((float(np.mean(region_patch)), (x, y)))
        if len(block_means) >= 6:
            block_means.sort(key=lambda item: item[0])
            for index, (mean_value, location) in enumerate(block_means):
                for other_mean, other_location in block_means[index + 1:]:
                    dist = abs(location[0] - other_location[0]) + abs(location[1] - other_location[1])
                    if dist > 32 and abs(mean_value - other_mean) < 5:
                        artifacts.append("Duplicate regions or repeated blocks were detected.")
                        regions.append({"label": "Duplicate block", "x": location[0], "y": location[1], "width": block_size, "height": block_size})
                        break
                if artifacts and artifacts[-1].startswith("Duplicate"):
                    break

    if len(artifacts) >= 2:
        artifacts.append("Splicing inconsistencies are likely present between image regions.")
        regions.append({"label": "Splice boundary", "x": width // 3, "y": height // 5, "width": width // 3, "height": height // 2})

    score = 0.0
    if any("Resolution" in artifact for artifact in artifacts):
        score += 8
    if any("blurred" in artifact.lower() for artifact in artifacts):
        score += 10
    if any("Noise variance" in artifact for artifact in artifacts):
        score += 12
    if any("Edge consistency" in artifact for artifact in artifacts):
        score += 10
    if any("Error Level Analysis" in artifact for artifact in artifacts):
        score += 18
    if any("Duplicate regions" in artifact for artifact in artifacts):
        score += 16
    if any("Splicing inconsistencies" in artifact for artifact in artifacts):
        score += 20

    manipulation_score = min(100, round(score, 2))
    confidence = min(0.99, round(0.45 + min(0.5, manipulation_score / 100.0) * 0.5, 2))
    manipulated = manipulation_score >= 60

    if manipulation_score >= 70:
        explanation = "The document image shows strong evidence of digital manipulation and should be treated as suspicious."
    elif manipulation_score >= 35:
        explanation = "The document image contains several suspicious forensic patterns that may indicate tampering."
    else:
        explanation = "The document image appears consistent and does not show strong forensic evidence of tampering."

    return {
        "manipulated": manipulated,
        "confidence": confidence,
        "manipulation_score": manipulation_score,
        "suspected_regions": regions[:5],
        "detected_artifacts": artifacts,
        "explanation": explanation,
    }


def analyze_image_forgery(file_path):
    if not file_path:
        return _default_result("No file path was provided for forgery inspection.")

    extension = os.path.splitext(file_path)[1].lower()
    if extension not in _SUPPORTED_EXTENSIONS:
        return _default_result("The file type is not supported for image forgery analysis.")

    if not os.path.exists(file_path):
        return _default_result("The selected file does not exist on disk.")

    if extension == ".pdf":
        temp_dir = None
        try:
            temp_dir = tempfile.mkdtemp(prefix="trustiq_forgery_", dir=os.path.dirname(file_path) or None)
            image_paths = convert_pdf_to_images(file_path, temp_dir)
            if not image_paths:
                return _default_result("The PDF did not yield any renderable page images.")
            summaries = [_analyze_single_image(path) for path in image_paths]
            if not summaries:
                return _default_result("The PDF could not be inspected.")
            combined = summaries[0]
            for item in summaries[1:]:
                combined["manipulation_score"] = max(combined["manipulation_score"], item["manipulation_score"])
                combined["confidence"] = max(combined["confidence"], item["confidence"])
                combined["manipulated"] = combined["manipulated"] or item["manipulated"]
                combined["detected_artifacts"].extend(item["detected_artifacts"])
                combined["suspected_regions"].extend(item["suspected_regions"])
                combined["detected_artifacts"] = list(dict.fromkeys(combined["detected_artifacts"]))
                combined["suspected_regions"] = combined["suspected_regions"][:8]
            return combined
        finally:
            if temp_dir and os.path.isdir(temp_dir):
                shutil.rmtree(temp_dir, ignore_errors=True)

    return _analyze_single_image(file_path)
