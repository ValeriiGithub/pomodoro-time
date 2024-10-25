from fastapi import APIRouter, status

from fixtures import tasks as fixture_tasks
from schema.task import Task

router = APIRouter(prefix="/task", tags=["task"])


@router.get("/all", response_model=list[Task])
async def get_tasks():
    """
    Возвращает список всех созданных задач.
    """
    return fixture_tasks


@router.post("/", response_model=Task)
async def create_task(task: Task):
    """
    Создает новую задачу с указанным task_id.
    """
    fixture_tasks.append(task)
    return task


@router.patch(
    "/{task_id}",
    response_model=Task,
)
async def patch_task(task_id: int, name: str):
    """
    Обнавляет задачу с указанным task_id.
    """
    for task in fixture_tasks:
        if task["id"] == task_id:
            task["name"] = name
            return task


@router.delete(
    "/{task_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def delete_task(task_id: int):
    for index, task in enumerate(fixture_tasks):
        if task["id"] == task_id:
            del fixture_tasks[index]
            # fixture_tasks.remove(task_id)  # Удаляет первое вхождение значения task_id
            return {"message": f"task {task_id} deleted"}

    return {"message": f"task {task_id} not found"}
