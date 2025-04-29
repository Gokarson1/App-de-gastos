from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build

def get_user_emails(id_token: str, max_results=10):
    creds = Credentials(token=id_token)
    service = build("gmail", "v1", credentials=creds)

    results = service.users().messages().list(userId='me', maxResults=max_results).execute()
    messages = results.get('messages', [])
    emails = []

    for msg in messages:
        msg_data = service.users().messages().get(userId='me', id=msg['id']).execute()
        snippet = msg_data.get('snippet', '')
        emails.append(snippet)

    return emails
