from fastapi import APIRouter, status

from database import get_db_connection
from fixtures import tasks as fixture_tasks
from schema.task import Task

router = APIRouter(prefix="/task", tags=["task"])


@router.get("/all", response_model=list[Task])
async def get_tasks():
    """
    Возвращает список всех созданных задач.
    """
    result: list[Task] = []
    cursor = get_db_connection().cursor()
    tasks = cursor.execute("SELECT * FROM Tasks").fetchall()        # tasks=[(1, 'test 1', 10, 1), (2, 'test 2', 10, 2), (3, 'test 3', 10, 3)]
    # распарсим tuple
    for task in tasks:
        result.append(Task(
            id=task[0],
            name=task[1],
            pomodoro_count=task[2],
            category_id=task[3],  # category_id=Category(id=task[3], name=get_category_name(task[3]))  # Заменить на получение имени категории из БД
        ))

    # print(f"{result=}")
    return result


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
