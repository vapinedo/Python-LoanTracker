from decouple import config
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from firebase_admin import auth, credentials, initialize_app

# Obtén el valor de la variable de entorno FIREBASE_ADMIN_SDK_JSON
firebase_credentials_json = config('FIREBASE_ADMIN_SDK_JSON')

# Initialize Firebase Admin SDK
firebase_credentials = credentials.Certificate(firebase_credentials_json)
firebase_app = initialize_app(firebase_credentials)

app = FastAPI()

# Configure CORS settings
origins = [
    "http://localhost",
    "http://localhost:5173",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE"],
    allow_headers=["*"],
)

# Utility function to verify Firebase ID Token
def verify_firebase_token(token):
    try:
        decoded_token = auth.verify_id_token(token)
        return decoded_token
    except auth.InvalidIdTokenError:
        raise HTTPException(status_code=401, detail="Invalid Firebase ID Token")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Example endpoint to verify Firebase ID token
@app.post("/verify-token/")
async def verify_token(token: str):
    try:
        decoded_token = verify_firebase_token(token)
        uid = decoded_token["uid"]
        return {"uid": uid}
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
