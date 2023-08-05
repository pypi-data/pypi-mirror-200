from fastapi import Depends, FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

from chlore.request import request_context
from chlore.logging import setup_app_logging, setup_standard_logging
from chlore.config import CONFIG
from chlore.errors import ChloreError
from chlore.etna_auth import header_auth, any_auth


app = FastAPI(dependencies=[Depends(any_auth)])


@app.on_event("startup")
def setup_logging():
    config = CONFIG.logging
    setup_standard_logging(config)
    setup_app_logging(config)


@app.on_event("startup")
def setup_cors():
    if CONFIG.cors is not None and CONFIG.cors.allowed_origin_re:
        app.add_middleware(
            CORSMiddleware,
            allow_origin_regex=CONFIG.cors.allowed_origin_re,
            allow_credentials=True,
            allow_methods=["GET", "POST", "PUT", "DELETE", "PATCH", "OPTIONS", "HEAD"],
            allow_headers=["Content-Type", "turbo-frame", "Cookie"],
            max_age=600,
        )


@app.middleware("http")
async def setup_request_context(request, call_next):
    with request_context(request):
        return await call_next(request)


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request, exc: RequestValidationError):
    return JSONResponse(status_code=400, content={"detail": exc.errors()})


@app.exception_handler(ChloreError)
async def exception_handler_hub(request: Request, exc: ChloreError):
    return JSONResponse(
        status_code=exc.status_code,
        content={"message": exc.detail, "error_code": exc.error_code},
    )
