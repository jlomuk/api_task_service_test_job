from fastapi import APIRouter
from api.task_api import task_router

root_router = APIRouter(prefix='/api/v1')
root_router.include_router(task_router)