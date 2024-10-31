import os

from dotenv import load_dotenv
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from contextlib import asynccontextmanager

from settings import ENV_FILE

load_dotenv(ENV_FILE)
config = os.environ

DB_URL = (f'{config["DB_DRIVER"]}://{config["DB_USER"]}:{config["DB_PASSWORD"]}'
          f'@{config["DB_HOST"]}:{config["DB_PORT"]}/{config["DB_SCHEMA"]}')
# Create the asynchronous engine
engine = create_async_engine(DB_URL, pool_pre_ping=True, pool_recycle=3600, max_overflow=30, pool_size=20,
                             pool_timeout=300,
                             connect_args={
                                 'sslmode': 'require',
                                 'connect_timeout': 100
                             })


# Create async session
@asynccontextmanager
async def db_session():
    # Async session maker
    async_session = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)
    async with async_session() as session:
        try:
            yield session
            await session.commit()
        except Exception as e:
            await session.rollback()
            raise
