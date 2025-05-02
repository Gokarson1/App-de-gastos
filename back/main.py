from fastapi import FastAPI
from app.routes.correo_routes import router
import spacy
from app.middleware.cors import add_cors


app = FastAPI()


# Cargar modelo spaCy globalmente
app.nlp = spacy.load("es_core_news_sm")

# Configurar CORS
add_cors(app)

# Registrar rutas
app.include_router(router)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)