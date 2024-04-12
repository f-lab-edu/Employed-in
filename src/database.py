from sqlalchemy.ext.asyncio import create_async_engine
from sqlmodel import SQLModel, pool
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker

from src import config
from src.models import post, accounts, profile

async_engine = create_async_engine(
    url=config.db.async_url,
    echo=config.db.echo,
    poolclass=pool.StaticPool,
)
engine = create_engine(url=config.db.sync_url)
session = sessionmaker(autocommit=False, autoflush=False, bind=engine)


async def create_db_and_tables() -> None:
    async with async_engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)


def get_db():
    db = session()
    try:
        yield db
    finally:
        db.close()


async def close_db() -> None:
    await async_engine.dispose()
