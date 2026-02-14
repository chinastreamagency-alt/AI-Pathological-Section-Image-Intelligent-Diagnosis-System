import os
import uuid
import base64
from PIL import Image
from config import UPLOAD_DIR, ALLOWED_EXTENSIONS


def validate_extension(filename: str) -> bool:
    ext = os.path.splitext(filename)[1].lower()
    return ext in ALLOWED_EXTENSIONS


def save_upload(file_bytes: bytes, original_name: str) -> dict:
    ext = os.path.splitext(original_name)[1].lower()
    unique_name = f"{uuid.uuid4().hex}{ext}"
    filepath = os.path.join(UPLOAD_DIR, unique_name)

    os.makedirs(UPLOAD_DIR, exist_ok=True)
    with open(filepath, "wb") as f:
        f.write(file_bytes)

    img = Image.open(filepath)
    width, height = img.size
    img.close()

    return {
        "filename": unique_name,
        "original_name": original_name,
        "file_size": len(file_bytes),
        "image_width": width,
        "image_height": height,
        "filepath": filepath,
    }


def image_to_base64(filepath: str) -> str:
    with open(filepath, "rb") as f:
        return base64.b64encode(f.read()).decode("utf-8")


def get_mime_type(filename: str) -> str:
    ext = os.path.splitext(filename)[1].lower()
    mime_map = {
        ".jpg": "image/jpeg",
        ".jpeg": "image/jpeg",
        ".png": "image/png",
        ".bmp": "image/bmp",
        ".tiff": "image/tiff",
        ".tif": "image/tiff",
        ".webp": "image/webp",
    }
    return mime_map.get(ext, "image/jpeg")
