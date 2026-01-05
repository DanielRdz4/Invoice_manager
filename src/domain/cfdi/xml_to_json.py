#Manages xml files
from pathlib import Path
from src.domain.cfdi.xml_parser import parse_cfdi_xml, CFDIParseError
from src.core.paths import RAW_DATA_DIR, PROCESSED_DATA_DIR
from src.utils.json_management import create_json, load_json
import re

def build_json_filename(cfdi_data: dict) -> str:
    """renames files to convention: UUID-F#-DATE and"""
    uuid = cfdi_data["uuid"]
    folio = cfdi_data.get("folio") or "NA"
    folio = re.sub(r"[^A-Za-z0-9_-]", "", folio)
    date_str = cfdi_data.get("fecha") or "NA"
    safe_date = date_str.split("T")[0]  # solo la fecha

    filename = f"{uuid}-{folio}-{safe_date}.json"
    return filename

def xml_to_json():
    """Reads all xml's in raw data directory, obtains info, renames
       the files to convention: UUID-F#-DATE and 
       stores them in processed data directory
    """
    downloaded_xmls = 0
    raw_xmls = RAW_DATA_DIR.glob("*.xml")
    for xml_path in raw_xmls:
        try:
            cfdi_data = parse_cfdi_xml(xml_path)

        except CFDIParseError as e:
            print(f"[ERROR] {xml_path.name}: {e}")
            continue

        new_filename = build_json_filename(cfdi_data)
        new_path = PROCESSED_DATA_DIR / new_filename

        if new_path.exists():
            continue

        create_json(cfdi_data, new_path)
        print(f"[OK] {xml_path.name} → {new_filename}")
        
        downloaded_xmls += 1
        
    if downloaded_xmls == 0:
        print(f"Base de datos al día")
    elif downloaded_xmls == 1:
        print(f"Se procesó exitosamente {downloaded_xmls} nueva factura")
    else:
        print(f"Se procesaron exitosamente {downloaded_xmls} nuevas facturas")

