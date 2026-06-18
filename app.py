import streamlit as st
import pandas as pd
import tempfile
from qr_scanner import read_qr
from PIL import Image
import pytesseract
import os

# ----------------------------
# FIX: Tesseract configuration (Windows)
# ----------------------------
tesseract_path = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

if os.path.exists(tesseract_path):
    pytesseract.pytesseract.tesseract_cmd = tesseract_path
else:
    st.error("❌ Tesseract not found. Check installation path.")

# ----------------------------
# Load registry
# ----------------------------
@st.cache_data
def load_registry():
    return pd.read_csv("registry.csv")

registry = load_registry()

# ----------------------------
# OCR function
# ----------------------------
def extract_text(image_file):
    image = Image.open(image_file)
    return pytesseract.image_to_string(image)

# ----------------------------
# UI
# ----------------------------
st.title("📜 Credential Verification System")

uploaded_file = st.file_uploader(
    "Upload Certificate",
    type=["png", "jpg", "jpeg"]
)

if uploaded_file is not None:

    st.image(uploaded_file, caption="Uploaded Certificate", use_container_width=True)

    # ----------------------------
    # STEP 1: QR SCAN
    # ----------------------------
    st.write("## Step 1: QR Scan")

    with tempfile.NamedTemporaryFile(delete=False, suffix=".png") as temp:
        temp.write(uploaded_file.getvalue())
        temp_path = temp.name

    try:
        cert_id = read_qr(temp_path)
        st.success(f"QR Code Extracted: {cert_id}")
    except Exception as e:
        st.error(f"QR Scan Failed: {e}")
        cert_id = None

    # ----------------------------
    # STEP 2: OCR
    # ----------------------------
    st.write("## Step 2: OCR Text Extraction")

    try:
        extracted_text = extract_text(uploaded_file)
        st.text(extracted_text)
    except Exception as e:
        st.error(f"OCR Failed: {e}")

    # ----------------------------
    # STEP 3: VERIFICATION
    # ----------------------------
    st.write("## Step 3: Verification Result")

    if cert_id is not None:

        match = registry[registry["hash"] == cert_id]

        if not match.empty:
            st.success("✅ Certificate is AUTHENTIC")
            st.dataframe(match)
        else:
            st.error("❌ Certificate NOT found in registry")

    else:
        st.warning("⚠️ QR code could not be read")



