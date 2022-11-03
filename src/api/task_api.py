from fastapi import APIRouter, Depends, HTTPException, Request
from schemas import task
from starlette import status
from services.task import TaskCRUD

task_router = APIRouter(prefix='/task', tags=['task'])


@task_router.get("/",
                 description='Получение списка всех задач пользователя',
                 response_model=list[task.TaskResponse],
                 status_code=status.HTTP_200_OK)
async def get_list_task(user_id: int, task_crud: TaskCRUD = Depends(TaskCRUD)):
    return await task_crud.list(user_id)


@task_router.get("/{task_id}",
                 description='Получение конкретной задачи по id',
                 response_model=task.TaskResponse,
                 status_code=status.HTTP_200_OK)
async def get_task(task_id: int, user_id: int, task_crud: TaskCRUD = Depends(TaskCRUD)):
    result = await task_crud.retrieve(pk=task_id, user_id=user_id)
    if result:
        return result
    raise HTTPException(status_code=status.HTTP_206_PARTIAL_CONTENT, detail='Задача не найдена')


@task_router.post("/",
                  description='Добавление новой задачи',
                  response_model=task.TaskResponse,
                  status_code=status.HTTP_201_CREATED)
async def add_task(new_task: task.CreateTaskRequest, task_crud: TaskCRUD = Depends(TaskCRUD)):
    return await task_crud.create(new_task.dict())


@task_router.delete("/{task_id}",
                    description='Удаление задачи по id',
                    status_code=status.HTTP_204_NO_CONTENT)
async def delete_task(task_id: int, user_id: int, task_crud: TaskCRUD = Depends(TaskCRUD)):
    res = await task_crud.delete(task_id, user_id=user_id)
    if not res:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Задача не найдена')