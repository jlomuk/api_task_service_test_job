import asyncio
import re
import time

import pytest
import pytest_asyncio
from sqlalchemy import insert, text
from asyncpg.exceptions import InvalidCatalogNameError
from sqlalchemy.ext.asyncio import create_async_engine, AsyncEngine
from sqlalchemy.pool import NullPool
from app import app
from db.db import get_engine
from db.models import meta
from fastapi.testclient import TestClient

from settings import settings

TEST_URL = f"{settings.POSTGRES_URL}_test"
TEST_DATABASE = 'task_service_test'

engine: AsyncEngine = create_async_engine(TEST_URL + '?prepared_statement_cache_size=0', echo=True, future=True,
                                          poolclass=NullPool)


async def create_db_if_not_exist():
    try:
        async with engine.connect():
            pass

    except InvalidCatalogNameError:
        temp_db_url = re.match(r'(^postgresql\S+)/', settings.POSTGRES_URL).group(0)
        temp_engine = create_async_engine(temp_db_url)

        async with temp_engine.connect() as conn:
            await conn.execute(text("COMMIT"))
            await conn.execute(text(f"CREATE DATABASE {TEST_DATABASE}"))


async def connect_test_db() -> AsyncEngine:
    app.dependency_overrides[get_engine] = lambda: engine
    await create_db_if_not_exist()

    async with engine.begin() as conn:
        await conn.run_sync(meta.create_all)

    return engine


async def disconnect_test_db():
    async with engine.begin() as conn:
        await conn.run_sync(meta.drop_all)


@pytest.fixture(scope="session")
def event_loop():
    policy = asyncio.get_event_loop_policy()
    loop = policy.new_event_loop()
    yield loop
    loop.close()


@pytest_asyncio.fixture(scope='session', autouse=True)
async def preparing_for_test():
    await connect_test_db()
    yield
    await disconnect_test_db()


@pytest_asyncio.fixture(autouse=True)
async def clear_table():
    for table in meta.tables:
        async with engine.connect() as conn:
            await conn.execute(text(f"TRUNCATE TABLE {table} RESTART IDENTITY"))


@pytest.fixture(scope='module')
def test_client():
    with TestClient(app) as client:
        yield client


@pytest_asyncio.fixture()
async def create_fake_data() -> int:
    user_id = 1
    async with engine.begin() as conn:
        statement = insert(meta.tables['task'])
        data = [
            {'title': 'Title1', 'completed': False, 'user_id': user_id, 'username': 'TestUser'},
            {'title': 'Title2', 'completed': True, 'user_id': user_id, 'username': 'TestUser'},
        ]
        await conn.execute(statement, data)
    return user_id
