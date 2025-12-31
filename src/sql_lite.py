import sqlite3
from pathlib import Path
from src.core.paths import DB_PATH
from src.core.paths import PROCESSED_DATA_DIR
from src.xml_parser import parse_cfdi_xml
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
        total REAL,
        timbre TEXT UNIQUE
    )
    """)

    #Insertar datos recursivamente
    for xml_path in PROCESSED_DATA_DIR.glob("*.xml"):
        xml_data = parse_cfdi_xml(xml_path)
        
        cursor.execute("""
        INSERT OR IGNORE INTO invoices (folio, fecha, emisor, receptor, total, timbre)
        VALUES (:folio, :date, :transmitter, :reciever, :total, :uuid)
        """, xml_data)

    conn.commit()
    conn.close()
