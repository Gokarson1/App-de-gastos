from fastapi import APIRouter, Request, HTTPException
from app.models.token import TokenRequest
from app.services.gmail_service import get_user_emails
from app.services.nlp_service import analyze_text_with_context

router = APIRouter()

@router.post("/analizar-correos")
async def analizar_correos(data: TokenRequest, request: Request):
    try:
        emails = get_user_emails(data.access_token)
        resultado = analyze_text_with_context(emails)
        return resultado
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))