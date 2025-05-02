from fastapi import FastAPI
from app.routes.correo_routes import router
import spacy

app = FastAPI()

# Cargar modelo spaCy globalmente
app.nlp = spacy.load("es_core_news_sm")

# Registrar rutas
app.include_router(router)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)