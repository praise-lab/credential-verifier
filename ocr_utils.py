import pytesseract
from PIL import Image
import re

def run_ocr(image_path):
    image = Image.open(image_path)
    text = pytesseract.image_to_string(image)
    return text


def extract_cert_id(text):
    # Looks for patterns like CERT-123, CERT-2026-001 etc.
    match = re.search(r"CERT[-\w\d]+", text)
    return match.group(0) if match else None
