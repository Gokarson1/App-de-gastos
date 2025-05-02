from typing import List
from fastapi import HTTPException
from google.auth.credentials import Credentials as GoogleCredentials
from googleapiclient.discovery import build

class AccessTokenCredentials(GoogleCredentials):
    def __init__(self, token: str):
        super().__init__()
        self.token = token

    def refresh(self, request):
        raise Exception("Este token no es refrescable")

    @property
    def expired(self):
        return False

    @property
    def valid(self):
        return True

def get_user_emails(access_token: str) -> List[str]:
    try:
        creds = AccessTokenCredentials(access_token)
        service = build('gmail', 'v1', credentials=creds)
        results = service.users().messages().list(userId='me', maxResults=10).execute()
        messages = results.get('messages', [])

        emails = []
        for msg in messages:
            msg_data = service.users().messages().get(userId='me', id=msg['id']).execute()
            snippet = msg_data.get('snippet', '')
            emails.append(snippet)

        return emails
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error accediendo a Gmail: {str(e)}")