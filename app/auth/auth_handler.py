import logging
import os
import time
import jwt
from dotenv import load_dotenv
from sqlalchemy import select
from werkzeug.security import check_password_hash

from models.engine import db_session
from models.models import User
from settings import ENV_FILE

load_dotenv(ENV_FILE)

JWT_SECRET = os.environ['JWT_SECRET_KEY']
JWT_ALGORITHM = "HS256"


async def sign_jwt(payload: dict) -> dict:
    expire_time = 600
    async with db_session() as db:
        user = await db.execute(select(User).filter_by(email=payload["email"]))
        user = user.scalars().first()
        password = payload["password"]
        if user and check_password_hash(user.password, password):
            payload["expires"] = time.time() + expire_time
            token = jwt.encode(payload, JWT_SECRET, algorithm=JWT_ALGORITHM)
            return {"result": "Authorized!", "status": 200, "access_token": token, "expires_in": expire_time}
        else:
            return {"result": "Not authorized!", "status": 401, "access_token": None}


async def decode_jwt(token: str) -> dict:
    try:
        decoded_token = jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
        async with db_session() as db:
            user = await db.execute(select(User).filter_by(email=decoded_token["email"]))
            user = user.scalars().first()
            if user and check_password_hash(user.password, decoded_token["password"]):
                return decoded_token if decoded_token["expires"] >= time.time() else None
        return {}
    except Exception as e:
        return {}
