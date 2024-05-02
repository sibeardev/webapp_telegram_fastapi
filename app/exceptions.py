from fastapi import HTTPException
from fastapi.responses import JSONResponse
from starlette.requests import Request
from starlette.status import (
    HTTP_401_UNAUTHORIZED,
    HTTP_403_FORBIDDEN,
    HTTP_404_NOT_FOUND,
    HTTP_500_INTERNAL_SERVER_ERROR,
)


async def server_error_exception(request: Request, exc: HTTPException):
    return JSONResponse(
        content={"message": "server error"},
        status_code=HTTP_500_INTERNAL_SERVER_ERROR,
    )


async def not_found_error_exception(request: Request, exc: HTTPException):
    return JSONResponse(
        content={"message": "404 page not found"},
        status_code=exc.status_code,
    )


async def forbidden_error_exception(request: Request, exc: HTTPException):
    return JSONResponse(
        content={"message": "forbidden error"},
        status_code=exc.status_code,
    )


async def unauthorized_error_exception(request: Request, exc: HTTPException):
    return JSONResponse(
        content={"message": "unauthorized error"},
        status_code=exc.status_code,
    )


exception_handlers = {
    HTTP_404_NOT_FOUND: not_found_error_exception,
    HTTP_403_FORBIDDEN: forbidden_error_exception,
    HTTP_401_UNAUTHORIZED: unauthorized_error_exception,
    HTTP_500_INTERNAL_SERVER_ERROR: server_error_exception,
}
