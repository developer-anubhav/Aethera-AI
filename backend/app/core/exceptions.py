from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder

class AetheraException(Exception):
    """Base exception for all Aethera application errors."""
    def __init__(self, message: str, status_code: int = 400):
        self.message = message
        self.status_code = status_code
        super().__init__(message)

class CompoundNotFoundError(AetheraException):
    def __init__(self, identifier: str | int):
        super().__init__(
            message=f"Chemical Compound '{identifier}' not found in database.",
            status_code=404
        )

class CategoryNotFoundError(AetheraException):
    def __init__(self, identifier: str | int):
        super().__init__(
            message=f"Category '{identifier}' not found in database.",
            status_code=404
        )

def register_exception_handlers(app: FastAPI) -> None:
    @app.exception_handler(AetheraException)
    async def aethera_exception_handler(request: Request, exc: AetheraException):
        return JSONResponse(
            status_code=exc.status_code,
            content=jsonable_encoder({
                "success": False,
                "error": {
                    "code": exc.__class__.__name__,
                    "message": exc.message
                }
            })
        )

    @app.exception_handler(Exception)
    async def generic_exception_handler(request: Request, exc: Exception):
        # In a real environment, we'd log the stack trace.
        return JSONResponse(
            status_code=500,
            content=jsonable_encoder({
                "success": False,
                "error": {
                    "code": "InternalServerError",
                    "message": "An unexpected error occurred on the server. Please try again later."
                }
            })
        )
