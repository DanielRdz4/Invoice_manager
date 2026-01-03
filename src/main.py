from src.oauth import get_gmail_credentials
from src.gmail_api import get_gmail_service
from src.core.config import fetch_user_config
from src.gmail_api import download_xml_atts
from src.xml_to_json import xml_to_json
from src.db_modules import save_to_db, db_to_xlsx


def main():

    #login
    creds = get_gmail_credentials()
    service = get_gmail_service(creds)

    #Show active user's email
    profile = service.users().getProfile(userId="me").execute()
    print("Correo autenticado:", profile["emailAddress"])

    #Creates query with user's config
    user_config = fetch_user_config()

    download_xml_atts(service, user_config)
    xml_to_json()
    
    #Creates secure Database with SQLite
    save_to_db()
    db_to_xlsx()

if __name__ == "__main__":
    main()
