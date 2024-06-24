from contextlib import asynccontextmanager

import logging
import os
import uvicorn

from starlette_csrf import CSRFMiddleware
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from prometheus_fastapi_instrumentator import Instrumentator
from logging_loki import LokiQueueHandler
from multiprocessing import Queue

from src import config
from src.apis.common import common_router
from src.apis.accounts import account_router
from src.database import close_db, create_db_and_tables


@asynccontextmanager
async def lifespan(app: FastAPI):
    await create_db_and_tables()
    yield
    await close_db()


app = FastAPI(lifespan=lifespan)
app.include_router(common_router)
app.include_router(account_router)

app.add_middleware(
    CORSMiddleware,
    allow_origins=config.cors.origins.split(","),
    allow_credentials=True,
    allow_methods=config.cors.methods.split(","),
    allow_headers=config.cors.headers.split(","),
)
app.add_middleware(
    CSRFMiddleware,
    secret=os.getenv("SECRET_KEY"),
    sensitive_cookies={"TEST_TOKEN"},
    cookie_domain="localhost"
)

instrumentator = Instrumentator().instrument(app)
instrumentator.expose(app, include_in_schema=False)

loki_logs_handler = LokiQueueHandler(
    Queue(-1),
    url = os.getenv("LOKI_ENDPOINT", None),
    tags={"application": "employedin"},
    version="1"
)
uvicorn_access_logger = logging.getLogger("uvicorn.access")
uvicorn_access_logger.addHandler(loki_logs_handler)


if __name__ == "__main__":
    uvicorn.run(app, host=config.web.host, port=config.web.port)
