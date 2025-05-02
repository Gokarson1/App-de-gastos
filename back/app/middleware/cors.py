from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

def add_cors(app: FastAPI):
    origins = [
        "http://localhost",
        "http://localhost:3000",
        "http://127.0.0.1:3000",
        "capacitor://localhost",
        # Puedes añadir más orígenes aquí
    ]

    app.add_middleware(
        CORSMiddleware,
        allow_origins=origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )