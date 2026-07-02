from fastapi import HTTPException, Request, status
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

from backend.core.logger import get_logger


logger = get_logger("errors")


async def http_exception_handler(request: Request, exception: HTTPException):
    if exception.status_code >= 500:
        logger.error(
            "HTTP error path=%s status_code=%s detail=%s",
            request.url.path,
            exception.status_code,
            exception.detail
        )
    else:
        logger.warning(
            "Handled HTTP exception path=%s status_code=%s detail=%s",
            request.url.path,
            exception.status_code,
            exception.detail
        )

    return JSONResponse(
        status_code=exception.status_code,
        content={
            "detail": exception.detail
        }
    )


async def validation_exception_handler(
    request: Request,
    exception: RequestValidationError
):
    logger.warning(
        "Validation error path=%s errors=%s",
        request.url.path,
        exception.errors()
    )

    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content={
            "detail": "Error de validación en los datos enviados.",
            "errors": exception.errors()
        }
    )


async def unhandled_exception_handler(request: Request, exception: Exception):
    logger.exception(
        "Unhandled exception path=%s error=%s",
        request.url.path,
        str(exception)
    )

    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={
            "detail": "Ocurrió un error interno en el servidor."
        }
    )


def register_exception_handlers(app):
    app.add_exception_handler(HTTPException, http_exception_handler)
    app.add_exception_handler(RequestValidationError, validation_exception_handler)
    app.add_exception_handler(Exception, unhandled_exception_handler)