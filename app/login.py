from fastapi import APIRouter, Request, Response
from fastapi.responses import JSONResponse
from sqlalchemy import select
from werkzeug.security import generate_password_hash

from app.auth.auth_handler import sign_jwt

from models.engine import db_session
from models.models import User

login_route = APIRouter(prefix='/login')


@login_route.post("/auth")
async def authorize(request: Request) -> Response:
    try:
        body = await request.json()
        auth = await sign_jwt(body)
        return auth
        if auth["status"] == 200:
            return JSONResponse(content={"access_token": auth["access_token"]}, status_code=200)
        else:
            return JSONResponse(content={"result": "Not authorized!"}, status_code=401)
    except Exception as e:
        return JSONResponse(content={"result": 'error', "message": str(e)}, status_code=500)


@login_route.post("/signup")
async def signup(request: Request) -> Response:
    try:
        body = await request.json()
        email = body.get('email')
        password = body.get('password')
        async with db_session() as db:
            user = await db.execute(select(User).filter_by(
                email=email))
            user = user.scalars().first()
            if user:  # check for user exist
                return JSONResponse(content={"result": 'error', "message": "User is already exist"}, status_code=401)
            # create if user isn't exists
            db.add(User(email=email, password=generate_password_hash(password, method='pbkdf2:sha256')))
            db.commit()
            return JSONResponse(content={"result": 'done!'}, status_code=200)
    except Exception as e:
        return JSONResponse(content={"result": 'error', "message": str(e)}, status_code=500)
