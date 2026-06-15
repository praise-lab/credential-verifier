import sqlite3

def init_db():
    conn = sqlite3.connect("registry.db")
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS certificates (
        cert_id TEXT PRIMARY KEY,
        name TEXT,
        course TEXT,
        date_issued TEXT
    )
    """)

    conn.commit()
    conn.close()


def add_certificate(cert_id, name, course, date):
    conn = sqlite3.connect("registry.db")
    cursor = conn.cursor()

    cursor.execute("""
    INSERT OR REPLACE INTO certificates VALUES (?, ?, ?, ?)
    """, (cert_id, name, course, date))

    conn.commit()
    conn.close()


def verify_certificate(cert_id):
    conn = sqlite3.connect("registry.db")
    cursor = conn.cursor()

    cursor.execute(
        "SELECT * FROM certificates WHERE cert_id=?",
        (cert_id,)
    )

    result = cursor.fetchone()
    conn.close()
    return result
