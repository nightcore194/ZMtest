import logging

from fastapi import APIRouter, Depends, Request, Response
from fastapi.responses import JSONResponse
from app.auth.auth_bearer import JWTBearer
from models.engine import db_session
from models.models import Task

api_route = APIRouter(prefix='/tasks')

logger = logging.getLogger(__name__)


# CREATING TASK OBJ
@api_route.post("/create", dependencies=[Depends(JWTBearer())])
async def create_task(request: Request) -> Response:
    body: dict = await request.json()
    async with db_session() as db:
        if all(hasattr(Task, key) for key, value in body.items()):
            await db.add(Task(*body))
            return JSONResponse(content={"message": "added!"}, status_code=200)
        else:
            return JSONResponse(content={"message": "error - check your fields"}, status_code=500)


# GETTING TASK OBJ
@api_route.get("/{task_id}", dependencies=[Depends(JWTBearer())])
async def get_task(task_id: int) -> Response:
    async with db_session() as db:
        task = await db.get(Task, task_id)
        return JSONResponse(content={"result": task.to_dict()}, status_code=200) if task else JSONResponse(
            content={"message": "not exists!"}, status_code=500)


# EDITING TASK OBJ
@api_route.patch("/{task_id}/update", dependencies=[Depends(JWTBearer())])
async def update_task(task_id: int, request: Request) -> Response:
    body: dict = await request.json()
    async with db_session() as db:
        task = await db.get(Task, task_id)
        if task:
            for key, value in body.items():
                if hasattr(Task, key):
                    setattr(Task, key, value)
            db.add(task)
            return JSONResponse(content={"result": task.to_dict()}, status_code=200)
        else:
            return JSONResponse(content={"message": "not exists!"}, status_code=500)


# GETTING ALL TASKS
@api_route.get("/list", dependencies=[Depends(JWTBearer())])
async def get_all_tasks() -> Response:
    async with db_session() as db:
        tasks = await db.query(Task).all()
        return JSONResponse(content={"result": [task.to_dict() for task in tasks]}, status_code=200)
