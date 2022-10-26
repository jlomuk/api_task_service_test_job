from sqlalchemy.ext.asyncio import create_async_engine
from settings import settings
from db.models import meta

engine = create_async_engine(settings.POSTGRES_URL + '?prepared_statement_cache_size=0', echo=True, future=True)


async def create_tables():
    async with engine.begin() as conn:
        await conn.run_sync(meta.create_all)


def get_engine():
    return engine
