from contextlib import asynccontextmanager

import os
import uvicorn

from starlette_csrf import CSRFMiddleware
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

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

if __name__ == "__main__":
    uvicorn.run(app, host=config.web.host, port=config.web.port)
