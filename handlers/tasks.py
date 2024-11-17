from typing import Annotated

from fastapi import APIRouter, status, Depends

from schema.task import TaskSchema
from repository import TaskRepository
from dependecy import get_tasks_repository, get_task_service
from service import TaskService

router = APIRouter(prefix="/task", tags=["task"])


@router.get(
    "/all",
    response_model=list[TaskSchema]
)
async def get_tasks(
        task_service: Annotated[TaskService, Depends(get_task_service)],
):
    """
    Возвращает список всех созданных задач.
    """
    return task_service.get_tasks()


@router.post(
    "/",
    response_model=TaskSchema
)
async def create_task(
        task: TaskSchema,
        task_repository: Annotated[TaskRepository, Depends(get_tasks_repository)]
):
    """
    Создает новую задачу с указанным task_id.
    """
    task_id = task_repository.create_task(task)
    task.id = task_id  # Эта строка присваивает возвращенный task_id атрибуту id объекта task.
    return task


@router.patch(
    "/{task_id}",
    response_model=TaskSchema,
)
async def patch_task(
        task_id: int,
        name: str,
        task_repository: Annotated[TaskRepository, Depends(get_tasks_repository)]
):
    """
    Обнавляет задачу с указанным task_id.
    """
    return task_repository.update_task_name(task_id, name)


@router.delete(
    "/{task_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def delete_task(
        task_id: int,
        task_repository: Annotated[TaskRepository, Depends(get_tasks_repository)]
):
    """
    Удаляет задачу с указанным task_id.
    :param task_repository:
    :param task_id:
    :return:
    """
    task_repository.delete_task(task_id)
    return {"message": "task deleted successfully"}
