from pydantic import BaseModel


class BaseTaskRequest(BaseModel):
    id: int


class GetTaskRequest(BaseTaskRequest):
    pass


class DeleteTaskRequest(BaseTaskRequest):
    pass


class CreateTaskRequest(BaseModel):
    title: str
    completed: bool
    user_id: int
    username: str


class TaskResponse(BaseModel):
    id: int
    title: str
    completed: bool
    user_id: int
    username: str
