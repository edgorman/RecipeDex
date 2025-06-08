from fastapi import FastAPI, Request, HTTPException, Depends
from google.auth.transport import requests as google_requests
from google.oauth2 import id_token as google_id_token

from internal.config.gcp import PROJECT_ID as GCP_PROJECT_ID
from internal.config.service import (
    NAME as SERVICE_NAME,
    VERSION as SERVICE_VERSION
)


app = FastAPI()


@app.get("/")
async def root():
    return {
        "name": SERVICE_NAME,
        "version": SERVICE_VERSION,
        "message": "Hello World :)"
    }

async def verify_token(request: Request):
    # Extract the auth from the request header
    auth_header = request.headers.get("Authorization")
    if not auth_header or not auth_header.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Authorization header missing or malformed")

    # Extract the bearer token
    token = auth_header.split("Bearer ")[1]

    try:
        # Verify the token, returning user object if successful
        user_data = google_id_token.verify_firebase_token(
            token, google_requests.Request(), audience=GCP_PROJECT_ID
        )
        if not user_data:
            raise HTTPException(status_code=401, detail="Invalid token")

        # e.g. name, user_id, email
        return user_data
    except Exception as e:
        raise HTTPException(status_code=401, detail=f"Token verification failed: {e}")

@app.get("/protected")
async def protected_route(user_data: dict = Depends(verify_token)):
    return {
        "name": SERVICE_NAME,
        "version": SERVICE_VERSION,
        "message": f"Welcome back {user_data.get('name')} :)"
    }
