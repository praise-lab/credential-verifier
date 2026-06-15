import streamlit as st
import tempfile
import pytesseract

pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

from database import init_db, verify_certificate
from qr_scanner import read_qr
from ocr_utils import run_ocr, extract_cert_id

init_db()

st.title("📜 Hybrid Certificate Verification System")

uploaded_file = st.file_uploader("Upload Certificate", type=["png", "jpg", "jpeg"])

if uploaded_file:

    # Save file temporarily
    with tempfile.NamedTemporaryFile(delete=False, suffix=".png") as tmp:
        tmp.write(uploaded_file.getbuffer())
        temp_path = tmp.name

    st.image(uploaded_file, caption="Uploaded Certificate", use_container_width=True)

    cert_id = None

    # -------------------------
    # STEP 1: TRY QR CODE
    # -------------------------
    st.subheader("🔍 Step 1: QR Scan")

    cert_id = read_qr(temp_path)

    if cert_id:
        st.success(f"QR Found: {cert_id}")
    else:
        st.warning("No QR detected. Moving to OCR...")

        # -------------------------
        # STEP 2: OCR FALLBACK
        # -------------------------
        st.subheader("🧠 Step 2: OCR Extraction")

        text = run_ocr(temp_path)
        st.text_area("Extracted Text", text, height=200)

        cert_id = extract_cert_id(text)

        if cert_id:
            st.success(f"Certificate ID extracted: {cert_id}")
        else:
            st.error("No Certificate ID found in text")

    # -------------------------
    # STEP 3: DATABASE CHECK
    # -------------------------
    if cert_id:
        st.subheader("📊 Verification Result")

        record = verify_certificate(cert_id)

        if record:
            st.success("Certificate is AUTHENTIC ✅")
            st.json({
                "Certificate ID": record[0],
                "Name": record[1],
                "Course": record[2],
                "Date Issued": record[3]
            })
        else:
            st.error("Certificate NOT FOUND ❌")



