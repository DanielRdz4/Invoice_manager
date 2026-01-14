from googleapiclient.discovery import build
from google.oauth2.credentials import Credentials
from src.core.paths import RAW_DATA_DIR
import base64
from pathlib import Path

def get_gmail_service(credentials: Credentials):
    """Crea el servicio Gmail API"""
    return build("gmail", "v1", credentials=credentials)

def show_active_user(service):
    profile = service.users().getProfile(userId="me").execute()
    print("Correo autenticado:", profile["emailAddress"])

def save_attachments(attachments):
    for att in attachments:
        file_path = RAW_DATA_DIR / att["filename"]

        if file_path.exists():
            print(f"Ya existe: {att['filename']}")
            continue

        with file_path.open("wb") as f:
            f.write(att["data"])

        print(f"Descargado: {att['filename']}")


def build_query(user_config):
    """Build's query with user's configuration"""

    query = (
        f"from:{user_config['sender_email']} "
        "has:attachment "
        "filename:xml"
    )

    return query

def download_attachment(service, msg_id, attachment_id, filename):
    attachment = service.users().messages().attachments().get(
        userId="me",
        messageId=msg_id,
        id=attachment_id
    ).execute()

    data = base64.urlsafe_b64decode(attachment["data"].encode("utf-8"))

    return {
        "filename": filename,
        "data": data
    }


def search_messages(service, user_config):
    """Looks for messages that match the query"""

    results = service.users().messages().list(
        userId="me",
        q=build_query(user_config)
    ).execute()

    messages = results.get("messages", [])
    print(f"Correos encontrados: {len(messages)}")

    return [msg['id'] for msg in messages]

def extract_xml_attachments(service, msg_id):
    message = service.users().messages().get(
        userId="me",
        id=msg_id
    ).execute()

    attachments = []

    for part in message["payload"].get("parts", []):
        filename = part.get("filename", "")

        if not filename.lower().endswith(".xml"):
            continue

        attachment_id = part.get("body", {}).get("attachmentId")
        if not attachment_id:
            continue

        attachments.append(
            download_attachment(service, msg_id, attachment_id, filename)
        )

    return attachments


def get_xml_atts(service, user_config):
    """Downloads XML attachments matching user config"""

    messages = search_messages(service, user_config)
    print(f"Correos encontrados: {len(messages)}")

    for msg_id in messages:
        attachments = extract_xml_attachments(service, msg_id)
        save_attachments(attachments)
