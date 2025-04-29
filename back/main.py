import base64
import re
import spacy
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from email import message_from_bytes

# ======== Configuración OAuth2 para Gmail API ========

# Alcances que pedimos: solo lectura
SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']

# Cargar modelo de spaCy en español
nlp = spacy.load('es_core_news_sm')

# ======== Funciones ========

def autenticar_gmail():
    """Autentica el acceso a la API de Gmail"""
    flow = InstalledAppFlow.from_client_secrets_file(
        'credentials.json', SCOPES)  # ← Tu archivo de credenciales
    creds = flow.run_local_server(port=0)
    return build('gmail', 'v1', credentials=creds)

def leer_emails(service, query=''):
    """Lee emails que coincidan con la query"""
    results = service.users().messages().list(userId='me', q=query, maxResults=5).execute()
    messages = results.get('messages', [])
    
    emails = []
    for msg in messages:
        txt = service.users().messages().get(userId='me', id=msg['id'], format='raw').execute()
        raw_msg = base64.urlsafe_b64decode(txt['raw'].encode('ASCII'))
        mime_msg = message_from_bytes(raw_msg)
        
        if mime_msg.is_multipart():
            parts = mime_msg.get_payload()
            content = ''
            for part in parts:
                if part.get_content_type() == 'text/plain':
                    content += part.get_payload(decode=True).decode()
        else:
            content = mime_msg.get_payload(decode=True).decode()
        
        emails.append(content)
    return emails

def extraer_info(texto):
    """Procesa el texto de un correo para extraer montos y entidades"""
    doc = nlp(texto)
    gastos = []

    for ent in doc.ents:
        if ent.label_ == 'MONEY':  # Entidades de tipo dinero
            gastos.append(ent.text)
    
    # Además, busquemos montos con regex por si spaCy falla
    regex_montos = re.findall(r'\$\s?\d+(?:,\d{3})*(?:\.\d{2})?', texto)
    gastos.extend(regex_montos)

    return gastos

# ======== Código principal ========

def main():
    service = autenticar_gmail()
    
    # Puedes ajustar la query a tus necesidades
    emails = leer_emails(service, query="factura OR pago OR compra")

    for idx, email in enumerate(emails, 1):
        print(f"\n--- Email #{idx} ---")
        print("Texto:")
        print(email)
        
        gastos = extraer_info(email)
        
        if gastos:
            print("\nGastos detectados:")
            for gasto in gastos:
                print(f"- {gasto}")
        else:
            print("\nNo se detectaron gastos.")

if __name__ == '__main__':
    main()