#Manages xml files
from pathlib import Path
from src.xml_parser import parse_cfdi_xml, CFDIParseError
from src.core.paths import RAW_DATA_DIR, PROCESSED_DATA_DIR
import re

def build_filename(cfdi_data: dict) -> str:
    """renames files to convention: UUID-F#-DATE and"""
    uuid = cfdi_data["uuid"]
    folio = cfdi_data.get("folio") or "NA"
    folio = re.sub(r"[^A-Za-z0-9_-]", "", folio)
    date_str = cfdi_data.get("date") or "NA"
    safe_date = date_str.split("T")[0]  # solo la fecha

    filename = f"{uuid}-{folio}-{safe_date}.xml"
    return filename

def process_xml_files():
    """Reads all xml's in raw data directory, obtains info, renames
       the files to convention: UUID-F#-DATE and 
       stores them in processed data directory
    """
    for xml_path in RAW_DATA_DIR.glob("*.xml"):
        try:
            cfdi_data = parse_cfdi_xml(xml_path)

        except CFDIParseError as e:
            print(f"[ERROR] {xml_path.name}: {e}")
            continue

        new_filename = build_filename(cfdi_data)
        new_path = PROCESSED_DATA_DIR / new_filename

        if new_path.exists():
            print(f"[DUPLICADO] {new_filename} ya existe, saltando")
            continue

        xml_path.rename(new_path)
        print(f"[OK] {xml_path.name} → {new_filename}")