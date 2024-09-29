import sentry_sdk
import logging
from fastapi import FastAPI, Response, Request
from fastapi.routing import APIRoute
from starlette.middleware.cors import CORSMiddleware
from starlette.types import Message
from starlette.background import BackgroundTask

from app.api.main import api_router
from app.core.config import settings


def custom_generate_unique_id(route: APIRoute) -> str:
    return f"{route.tags[0]}-{route.name}"


if settings.SENTRY_DSN and settings.ENVIRONMENT != "local":
    sentry_sdk.init(dsn=str(settings.SENTRY_DSN), enable_tracing=True)

app = FastAPI(
    title=settings.PROJECT_NAME,
    openapi_url=f"{settings.API_V1_STR}/openapi.json",
    generate_unique_id_function=custom_generate_unique_id,
)

# Set all CORS enabled origins
if settings.all_cors_origins:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.all_cors_origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

app.include_router(api_router, prefix=settings.API_V1_STR)


async def set_body(request: Request, body: bytes):
    async def receive() -> Message:
        return {'type': 'http.request', 'body': body}
    request._receive = receive

def log_info(req_body, res_body):
    req_body = req_body.decode('utf-8')
    res_body = res_body.decode('utf-8')

    logging.info(f"request body: {req_body}")
    logging.info(f"response body: {res_body}")

@app.middleware('http')
async def some_middleware(request: Request, call_next):
    req_body = await request.body()
    await set_body(request, req_body)
    response = await call_next(request)
    
    res_body = b''
    async for chunk in response.body_iterator:
        res_body += chunk
    
    task = BackgroundTask(log_info, req_body, res_body)
    return Response(content=res_body, status_code=response.status_code, 
        headers=dict(response.headers), media_type=response.media_type, background=task)