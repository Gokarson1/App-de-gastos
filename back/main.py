from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List
from google.auth.credentials import Credentials as GoogleCredentials
from googleapiclient.discovery import build
import spacy

app = FastAPI()
nlp = spacy.load("es_core_news_sm")

class TokenRequest(BaseModel):
    access_token: str

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

def analyze_text_with_spacy(emails: List[str]) -> List[str]:
    gastos_detectados = []
    for email in emails:
        doc = nlp(email)
        for ent in doc.ents:
            if ent.label_ in ['MONEY']:
                gastos_detectados.append(f"Gasto detectado: {ent.text} en '{email[:50]}...'")
    return gastos_detectados

@app.post("/analizar-correos")
async def analizar_correos(data: TokenRequest):
    try:
        emails = get_user_emails(data.access_token)
        gastos = analyze_text_with_spacy(emails)
        return {
            "cantidad_correos_analizados": len(emails),
            "gastos_detectados": gastos
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
