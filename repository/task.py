from sqlalchemy import select, delete
from sqlalchemy.orm import Session

from database import Task, get_db_session


class TaskRepository:
    """
    TaskRepository класс:
        Этот класс отвечает за взаимодействие с базой данных для работы с задачами (Task).
        Он принимает в конструкторе объект Session из SQLAlchemy, который представляет соединение с базой данных.
        Метод get_task(self, task_id) возвращает задачу (Task) по ее идентификатору. Если задача не найдена, он генерирует исключение ValueError.
        Метод get_tasks(self) (который пока пуст) должен возвращать список всех задач.

    get_task_repository() функция:
        Эта функция является зависимостью (Dependency) для получения экземпляра TaskRepository.
        Она вызывает функцию get_db_session() (которая не показана в приведенном коде), чтобы получить объект Session для базы данных.
        Затем она создает экземпляр TaskRepository и передает ему полученный объект Session.
        Эта функция возвращает экземпляр TaskRepository, который можно использовать в других частях вашего приложения.

    """

    def __init__(self, db_session: Session):
        self.db_session = db_session

    def get_tasks(self):
        query = select([Task])
        with self.db_session as session:
            tasks: list[Task] = session.execute(query).scalars().all()
            if tasks is None:
                raise ValueError("No tasks found")
            return tasks

    def get_task(self, task_id: int) -> Task | None:
        query = select([Task]).where(Task.id == task_id)
        with self.db_session as session:
            # task = session.execute(query).fetchone()
            # task = session.execute(query).scalars().first()        # Said
            task: Task = session.execute(query).scalar_one_or_none()  # Said
            # if task is None:
            #     raise ValueError(f"Task with id {task_id} not found")
            return task

    def create_task(self, task: Task) -> None:
        with self.db_session as session:
            session.add(task)
            session.commit()

    def delete_task(self, task_id: int) -> None:
        query = delete(Task).where(Task.id == task_id)
        with self.db_session as session:
            session.execute(query)
            session.commit()


# Dependency
def get_task_repository() -> TaskRepository:
    """
    Назначение функции get_task_repository():

    Эта функция предоставляет единый точку доступа для получения экземпляра TaskRepository.
    Она скрывает детали создания TaskRepository, такие, как получение объекта Session из базы данных.
    Это позволяет легко заменить реализацию TaskRepository (например, если вы решите использовать другую базу данных или другой ORM) без необходимости изменять код, который использует TaskRepository.
    Такой подход называется "внедрение зависимостей" (Dependency Injection) и помогает сделать код более модульным, тестируемым и гибким.

    Таким образом, функция get_task_repository() играет важную роль в обеспечении правильного создания и использования TaskRepository в  приложении.
    :return: TaskRepository
    """
    db_session = get_db_session()
    return TaskRepository(db_session)
