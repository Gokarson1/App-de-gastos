import base64
import re
import os
import json
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from email import message_from_bytes

# ======== Configuración OAuth2 para Gmail API ========

SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']

# ======== Funciones ========

def autenticar_gmail():
    flow = InstalledAppFlow.from_client_secrets_file(
        'credential.json', SCOPES)
    creds = flow.run_local_server(port=0)
    return build('gmail', 'v1', credentials=creds)

def leer_emails(service, query=''):
    results = service.users().messages().list(userId='me', q=query, maxResults=10).execute()
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

def extraer_montos_regex(texto):
    """Extrae montos usando expresiones regulares"""
    patrones = [
        r'\$\s?\d{1,3}(?:[.,]\d{3})*(?:[.,]\d{2})?',     # $1.234,56 o $ 1,234.56
        r'\d{1,3}(?:[.,]\d{3})*(?:[.,]\d{2})?\s?(USD|EUR|MXN|COP|€|\$)',  # 1.000,00 EUR o 1,000.00 USD
    ]
    montos = []
    for patron in patrones:
        encontrados = re.findall(patron, texto)
        montos.extend(encontrados)
    return montos


def load_banks():
    bank_data_path = os.path.join(os.path.dirname(__file__), 'bancos.json')
    with open(bank_data_path, 'r', encoding='utf-8') as f:
        return json.load(f)

# ======== Código principal ========

def main():
    service = autenticar_gmail()
    
    bank_data = load_banks()
    banks = bank_data['banks']

    bank_domains = [domain for bank in banks for domain in bank['domains']]
    bank_query = " OR ".join([f"from:{domain}" for domain in bank_domains])
    full_query = f"({bank_query}) AND (factura OR pago OR compra OR boleta OR cobro OR recibo OR abono OR cargo)"
    emails = leer_emails(service, query=full_query)
    
    detected_charges = []
    
    for idx, email in enumerate(emails, 1):
        email_info = {
            "id": idx,
            "amounts": []
        }
        
        montos = extraer_montos_regex(email)
        
        if montos:
            email_info["amounts"] = montos
            
        detected_charges.append(email_info)
    
    # Convert to JSON
    charges_json = json.dumps(detected_charges, indent=4, ensure_ascii=False)
    
    # Print JSON to console
    print(charges_json)
    
    # Optionally save to file
    with open("detected_charges.json", "w", encoding="utf-8") as f:
        f.write(charges_json)

if __name__ == '__main__':
    main()