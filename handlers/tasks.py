from fastapi import APIRouter

router = APIRouter(prefix="/task",
                   tags=["task"])


@router.get("/all")
async def get_tasks():
    return {"message": "ok"}


@router.post("/")
async def create_task():
    return {"text": "task created"}


tasks = []


@router.post("/{task_id}")
def create_task(task_id: int):
    """
    Создает новую задачу с указанным task_id.
    """
    tasks.append(task_id)
    return {"message": f"Задача с id {task_id} создана."}


@router.get("/tasks")
def get_tasks():
    """
    Возвращает список всех созданных задач.
    """
    return {"tasks": tasks}

@router.put("/{task_id}")
async def update_task(task_id: int):
    """
    Обнавляет задачу с указанным task_id.
    """
    return {"message": f"task {task_id} updated"}

@router.patch("/{task_id}")
async def patch_task(task_id: int, name: str):
    return {"message": f"task {task_id}, {name} patched"}

@router.delete("/{task_id}")
async def delete_task(task_id: int):
    tasks.remove(task_id)  # Удаляет первое вхождение значения task_id
    return {"message": f"task {task_id} deleted"}
