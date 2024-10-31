from fastapi import FastAPI, Request, Response
from fastapi.responses import JSONResponse


def create_app():
    app = FastAPI()

    @app.exception_handler(Exception)
    async def handle_error(request: Request, e: Exception) -> Response:
        response = {"result": str(e)}
        return JSONResponse(content=response, status_code=500)

    from app.api import api_route
    from app.login import login_route
    app.include_router(api_route)
    app.include_router(login_route)

    return app
