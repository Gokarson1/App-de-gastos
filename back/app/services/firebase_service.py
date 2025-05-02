import firebase_admin
from firebase_admin import credentials, auth

cred = credentials.Certificate("./credentials.json")
firebase_admin.initialize_app(cred)

# Ejemplo: verificar un ID token
decoded_token = auth.verify_id_token(token)
uid = decoded_token["uid"]