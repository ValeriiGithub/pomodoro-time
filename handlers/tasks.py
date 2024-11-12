from typing import Annotated

from fastapi import APIRouter, status, Depends

from schema.task import TaskSchema
from repository import TaskRepository
from dependecy import get_task_repository

router = APIRouter(prefix="/task", tags=["task"])


@router.get(
    "/all",
    response_model=list[TaskSchema]
)
async def get_tasks(task_repository: Annotated[TaskRepository, Depends(get_task_repository)]):
    """
    Возвращает список всех созданных задач.
    """
    tasks = task_repository.get_tasks()
    return tasks


@router.post(
    "/",
    response_model=TaskSchema
)
async def create_task(
        task: TaskSchema,
        task_repository: Annotated[TaskRepository, Depends(get_task_repository)]
):
    """
    Создает новую задачу с указанным task_id.
    """
    task_id = task_repository.create_task(task)
    task.id = task_id                           # Эта строка присваивает возвращенный task_id атрибуту id объекта task.
    return task


@router.patch(
    "/{task_id}",
    response_model=TaskSchema,
)
async def patch_task(task_id: int, name: str):
    """
    Обнавляет задачу с указанным task_id.
    """
    connection = get_db_session()
    cursor = connection.cursor()
    cursor.execute("UPDATE Tasks SET name=? WHERE id=?", (name, task_id))
    connection.commit()
    task = cursor.execute("SELECT * FROM Tasks WHERE id=?",
                          (task_id,)).fetchall()[0]
    connection.close()
    return TaskSchema(
        id=task[0],
        name=task[1],
        pomodoro_count=task[2],
        category_id=task[3],
    )


@router.delete(
    "/{task_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def delete_task(task_id: int):
    """
    Удаляет задачу с указанным task_id.
    :param task_id:
    :return:
    """
    connection = get_db_session()
    cursor = connection.cursor()
    cursor.execute("DELETE FROM Tasks WHERE id=?", (task_id,))
    connection.commit()
    connection.close()
    return {"message": f"task {task_id} deleted successfully"}

    # for index, task in enumerate(fixture_tasks):
    #     if task["id"] == task_id:
    #         del fixture_tasks[index]
    #         # fixture_tasks.remove(task_id)  # Удаляет первое вхождение значения task_id
    #         return {"message": f"task {task_id} deleted"}

    return {"message": f"task {task_id} not found"}
