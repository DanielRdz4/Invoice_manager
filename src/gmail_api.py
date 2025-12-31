from googleapiclient.discovery import build
from google.oauth2.credentials import Credentials
from src.core.config import load_user_config
from src.core.paths import RAW_DATA_DIR, PROCESSED_DATA_DIR
import base64

def get_gmail_service(credentials: Credentials):
    """Crea el servicio Gmail API"""
    return build("gmail", "v1", credentials=credentials)

def build_query(user_config):
    """Build's query with user's configuration"""
    query = (
        f"from:{user_config['sender_email']} "
        "has:attachment "
        "filename:xml"
    )

    return query

def download_xml_atts(service, user_config):
    """Downloads xml's that meets query criteria"""

    results = service.users().messages().list(
        userId="me",
        q=build_query(user_config)
    ).execute()

    messages = results.get("messages", [])
    print(f"Correos encontrados: {len(messages)}")

    for msg in messages:
        msg_id = msg["id"]

        message = service.users().messages().get(
            userId="me",
            id=msg_id
        ).execute()

        for part in message["payload"].get("parts", []):
            filename = part.get("filename", "")

            if not filename.lower().endswith(".xml"):
                continue

            body = part.get("body", {})
            attachment_id = body.get("attachmentId")

            if not attachment_id:
                continue

            attachment = service.users().messages().attachments().get(
                userId="me",
                messageId = msg_id,
                id = attachment_id
            ).execute()

            file_data = base64.urlsafe_b64decode(
                attachment["data"].encode("UTF-8")
            )

            file_path = RAW_DATA_DIR / filename

            if file_path.exists():
                print(f"Ya existe: {filename}")
            
            with open(file_path,"wb") as f:
                f.write(file_data)
            
            print(f"descargado: {filename}")