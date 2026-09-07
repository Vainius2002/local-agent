from fastapi import APIRouter
from fastapi.responses import RedirectResponse

from app.models.users import User
from app.models.sessions import Sessions

from app.db import SessionLocal
from sqlalchemy import select
import secrets
from datetime import datetime, timedelta
import httpx

from app.config import AUTH_SERVICE_URL




router = APIRouter()


@router.get("/callback")
def validate_code(code: str):

    token_response = httpx.post(f"{AUTH_SERVICE_URL}/token", data={"code":code}, verify=False)


    if token_response.status_code != 200:
        return RedirectResponse(f"{AUTH_SERVICE_URL}/login")

    user_data = token_response.json()


    with SessionLocal() as session:
        existing_user = session.scalar(select(User).where(User.auth_user_id == user_data["user_id"]))

        if existing_user:
            user = existing_user
        
        else:
            user = User(
                auth_user_id = user_data["user_id"],
                username = user_data["username"]
            )

            session.add(user)
            session.commit()
            session.refresh(user)

        session_id = secrets.token_urlsafe(32)
        
        sessions_table = Sessions(
            user_id = user.id,
            session_id = session_id,
            expires_at = datetime.utcnow() + timedelta(days=7)
        )

        session.add(sessions_table)
        session.commit()
        session.refresh(sessions_table)


        redirect = RedirectResponse("/ask")

        redirect.set_cookie(key="session_id", 
                            value=session_id,
                            httponly=True,
                            secure=True,
                            samesite="lax"
        )

        return redirect