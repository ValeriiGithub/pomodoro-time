from sqlalchemy import select
from sqlalchemy.orm import Session

from database import Task, get_db_session


class TaskRepository:
    def __init__(self, db_session: Session):
        self.db_session = db_session

    def get_task(self, task_id):
        query = select([Task]).where(Task.id == task_id)
        with self.db_session() as session:
            task = session.execute(query).fetchone()
            if task is None:
                raise ValueError(f"Task with id {task_id} not found")
            return task

    def get_tasks(self):
        pass


# Dependency
def get_task_repository() -> TaskRepository:
    db_session = get_db_session()
    return TaskRepository(db_session)
