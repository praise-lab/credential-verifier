print("SCRIPT STARTED")

from database import init_db, add_certificate, verify_certificate

print("IMPORTS OK")

init_db()
print("DB INIT OK")

add_certificate("CERT-001", "John Doe", "AI Course", "2026-06-13")
print("DATA INSERTED")

result = verify_certificate("CERT-001")
print("RESULT:", result)
