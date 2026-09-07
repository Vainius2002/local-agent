from fastapi import Request, HTTPException
from fastapi.responses import RedirectResponse

from app.db import SessionLocal
from sqlalchemy import select
from app.models.sessions import Sessions
from app.models.users import User
from app.config import AUTH_SERVICE_URL, APP_URL
from datetime import datetime



LOGIN_REDIRECT = {"Location": f"{AUTH_SERVICE_URL}/authorize?redirect_uri={APP_URL}/callback"}

def get_current_user(request : Request):
    cookies = request.cookies.get("session_id")

    if not cookies:
        raise HTTPException(status_code=307, headers=LOGIN_REDIRECT)

    with SessionLocal() as session:
        session_id = session.scalar(select(Sessions).where(Sessions.session_id == cookies))

        if not session_id:
            raise HTTPException(status_code=307, headers=LOGIN_REDIRECT)

        if session_id.expires_at < datetime.utcnow():
            raise HTTPException(status_code=307, headers=LOGIN_REDIRECT)


        user = session.scalar(select(User).where(User.id == session_id.user_id))

        if not user:
            raise HTTPException(status_code=307, headers=LOGIN_REDIRECT)

        return user
