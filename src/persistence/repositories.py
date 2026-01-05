
from src.persistence.database import get_connection
from src.core.paths import PROCESSED_DATA_DIR
from src.domain.cfdi.xml_to_json import load_json

def save_invoices_from_json():
    """
    Cycles every xml file in PROCESSED_DATA_DIR and
    adds them to the database
    """
    
    conn = get_connection()
    cursor = conn.cursor()
    query = """
        INSERT OR IGNORE INTO invoices (folio, fecha, emisor, receptor, tipo, total, uuid)
        VALUES (:folio, :fecha, :emisor, :receptor, :tipo, :total, :uuid)
        """

    #Insertar datos recursivamente
    for json_path in PROCESSED_DATA_DIR.glob("*.json"):

        json_data = load_json(json_path)
        cursor.execute(query, json_data)

    conn.commit()
    conn.close()

