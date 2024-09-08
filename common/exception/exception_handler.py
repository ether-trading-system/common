from http import HTTPStatus
from typing import Any, Optional
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from dataclasses import dataclass
from pydantic import ValidationError
from pydantic_core import ErrorDetails
from .exception import EtherException
from .error_code import EtherErrorCode


@dataclass
class EtherErrorResponse:
    error_code: str
    message: str
    detail: str
    data: Optional[Any] = None


def register_exception_handler(app: FastAPI) -> None:

    @app.exception_handler(Exception)
    async def ether_exception_handler(request: Request, exception: Exception):
        return JSONResponse(
            status_code=HTTPStatus.INTERNAL_SERVER_ERROR,
            content=EtherErrorResponse(
                error_code=EtherErrorCode.UNKNOWN_ERROR.value,
                message=str(exception),
                detail=str(exception),
            ).__dict__
        )

    @app.exception_handler(ValidationError)
    async def validation_error_handler(request: Request, exception: ValidationError):
        errors: list[ErrorDetails] = exception.errors()

        return JSONResponse(
            status_code=HTTPStatus.BAD_REQUEST,
            content=EtherErrorResponse(
                error_code=EtherErrorCode.INVALID_REQUEST.value,
                message=errors[0].get('msg'),
                detail=errors[0].get('msg'),
                data=exception.errors()
            ).__dict__
        )

    @app.exception_handler(EtherException)
    async def exception_handler(request: Request, exception: EtherException):
        return JSONResponse(
            status_code=exception.status_code,
            content=EtherErrorResponse(
                error_code=exception.error_code.value,
                message=exception.message,
                detail=exception.detail,
                data=exception.data
            ).__dict__
        )