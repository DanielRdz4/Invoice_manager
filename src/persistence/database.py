import sqlite3
from src.core.paths import DB_PATH

def get_connection():
    return sqlite3.connect(DB_PATH)

def initialize_db():
    """
    Creates 'invoices' table
    """
    conn = get_connection()
    cursor = conn.cursor()

    # Crear tabla si no existe
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS invoices (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        folio TEXT,
        fecha TEXT,
        emisor TEXT,
        receptor TEXT,
        tipo TEXT,
        total REAL,
        uuid TEXT UNIQUE
    )
    """)

    conn.commit()
    conn.close()
