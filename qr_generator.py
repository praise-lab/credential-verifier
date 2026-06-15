import qrcode
from database import init_db, add_certificate

init_db()

def create_certificate(cert_id, name, course, date):
    # 1. Save to database
    add_certificate(cert_id, name, course, date)

    # 2. Create QR code containing ONLY cert_id
    qr = qrcode.make(cert_id)

    # 3. Save QR image
    filename = f"{cert_id}.png"
    qr.save(filename)

    print("Certificate created:", cert_id)
    print("QR saved as:", filename)


# TEST EXAMPLE
create_certificate("CERT-002", "Alice Smith", "Data Science", "2026-06-13")
