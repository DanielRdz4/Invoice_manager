import sqlite3
from pathlib import Path
from src.core.paths import DB_PATH, PROCESSED_DATA_DIR, XLSX_PATH
from src.xml_parser import parse_cfdi_xml
from openpyxl import Workbook
from src.file_manager import load_json
DB_PATH = DB_PATH

def save_to_db():
    """
    Cycles every xml file in PROCESSED_DATA_DIR and
    adds them to the database
    """
    conn = sqlite3.connect(DB_PATH)
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

    #Insertar datos recursivamente
    for json_path in PROCESSED_DATA_DIR.glob("*.json"):

        json_data = load_json(json_path)
        cursor.execute("""
        INSERT OR IGNORE INTO invoices (folio, fecha, emisor, receptor, tipo, total, uuid)
        VALUES (:folio, :fecha, :emisor, :receptor, :tipo, :total, :uuid)
        """, json_data)

    conn.commit()
    conn.close()

def db_to_xlsx():
    """Reads .db file ando converts it to xlsx"""

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM invoices")
    rows = cursor.fetchall()
    column_names = [desc[0] for desc in cursor.description]

    wb = Workbook()
    ws = wb.active
    ws.title = "Invoices"

    ws.append(column_names)
    for row in rows:
        ws.append(row)
        
    cursor.execute("SELECT COUNT(*) FROM invoices")
    print("Registros en invoices:", cursor.fetchone()[0])

    wb.save(XLSX_PATH)

    conn.close()
