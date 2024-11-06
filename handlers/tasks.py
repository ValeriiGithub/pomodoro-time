from fastapi import APIRouter, status

from database import get_db_connection
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
    connection = get_db_connection()
    cursor = connection.cursor()
    cursor.execute("INSERT INTO Tasks (name, pomodoro_count, category_id) VALUES (?,?,?)",
                   (task.name, task.pomodoro_count, task.category_id))
    connection.commit()
    connection.close()
    return task


@router.patch(
    "/{task_id}",
    response_model=Task,
)
async def patch_task(task_id: int, name: str):
    """
    Обнавляет задачу с указанным task_id.
    """
    connection = get_db_connection()
    cursor = connection.cursor()
    cursor.execute("UPDATE Tasks SET name=? WHERE id=?", (name, task_id))
    connection.commit()
    task = cursor.execute("SELECT * FROM Tasks WHERE id=?",
                          (task_id,)).fetchall()[0]
    connection.close()
    return Task(
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
    connection = get_db_connection()
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
