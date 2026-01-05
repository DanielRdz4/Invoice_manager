from src.integrations.gmail.oauth import get_gmail_credentials
from src.integrations.gmail.client import get_gmail_service, download_xml_atts
from src.core.config import fetch_user_config
from src.domain.cfdi.xml_to_json import xml_to_json
from src.persistence.repositories import save_invoices_from_json
from src.persistence.database import initialize_db
from src.reporting.excel_exporter import db_to_xlsx


def run_pipeline():

    #login
    creds = get_gmail_credentials()
    service = get_gmail_service(creds)

    #Show active user's email
    profile = service.users().getProfile(userId="me").execute()
    print("Correo autenticado:", profile["emailAddress"])

    #Creates query with user's config
    user_config = fetch_user_config()

    #Flujo princial
    download_xml_atts(service, user_config)
    xml_to_json()
    initialize_db()
    save_invoices_from_json()
    db_to_xlsx()

