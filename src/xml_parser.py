#Manages xml information and functions

import xml.etree.ElementTree as ET
from pathlib import Path
from src.utils.safe_convert import get_float

#NAMESPACES
CFDI_NS = {
    "cfdi": "http://www.sat.gob.mx/cfd/4",
    "tfd": "http://www.sat.gob.mx/TimbreFiscalDigital",
}

class CFDIParseError(Exception):
    pass

def parse_cfdi_xml(xml_path: Path) -> dict: 
    """
    Parses a CFDI XML file and extracts key fiscal data.
    Raises CFDIParseError if UUID is missing.
    """

    try:
        tree= ET.parse(xml_path)
        root = tree.getroot()
    except ET.ParseError as e:
        raise CFDIParseError(f"XML inválido: {xml_path.name}") from e
    
    timbre = root.find(".//tfd:TimbreFiscalDigital", CFDI_NS)
    if timbre is None:
        raise CFDIParseError("No se encontró TimbreFiscalDigital")
    
    uuid = timbre.attrib.get("UUID")
    if not uuid:
        raise CFDIParseError("UUID no encontrado")
    
    comprobante= root
    folio = comprobante.attrib.get("Folio")
    date = comprobante.attrib.get("Fecha")
    type = comprobante.attrib.get("TipoDeComprobante")
    total = get_float(comprobante.attrib.get("Total"))

    transmitter=root.find("cfdi:Emisor", CFDI_NS)
    reciever = root.find("cfdi:Receptor",CFDI_NS)

    transmitter_name = transmitter.attrib.get("Nombre") if not None else None
    reciever_name = reciever.attrib.get("Nombre") if not None else None

    return {
        "uuid": uuid,
        "folio": folio,
        "date": date,
        "type": type,
        "total": total,
        "transmitter": transmitter_name,
        "reciever": reciever_name,
    }


    