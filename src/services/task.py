from typing import TypeVar

from sqlalchemy import select, delete, insert
from sqlalchemy.engine import CursorResult
from sqlalchemy.sql.schema import Table
from sqlalchemy.ext.asyncio.engine import AsyncEngine
from db.db import get_engine
from db.models import task
from fastapi import Depends

TableType = TypeVar('TableType', bound=Table)


class TaskCRUD:
    Table: TableType = task

    def __init__(self, conn: AsyncEngine = Depends(get_engine)):
        self.table: TableType = self.Table
        self.connection: AsyncEngine = conn

    async def list(self, user_id: int) -> dict:
        async with self.connection.begin() as conn:
            result: CursorResult = await conn.execute(
                select(self.table)
                .where(self.table.c.user_id == user_id)
            )

        return result.mappings().all()

    async def retrieve(self, pk: int, user_id: int) -> dict:
        async with self.connection.begin() as conn:
            result: CursorResult = await conn.execute(
                select(self.table).
                where(self.table.c.id == pk, self.table.c.user_id == user_id)
            )

        return result.mappings().first()

    async def create(self, data: dict) -> dict:
        async with self.connection.begin() as conn:
            statement = insert(self.table).returning(*self.table.c)
            result: CursorResult = await conn.execute(statement, data)
        return result.mappings().first()

    async def delete(self, pk: int, user_id: int):
        statement = delete(self.table). \
            where(self.table.c.id == pk, self.table.c.user_id == user_id)
        async with self.connection.begin() as conn:
            await conn.execute(statement)
