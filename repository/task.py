from sqlalchemy import select, delete, update
from sqlalchemy.orm import Session

from database import Tasks, Categories
from schema.task import TaskSchema


class TaskRepository:
    """
    TaskRepository класс:
        Этот класс отвечает за взаимодействие с базой данных для работы с задачами (Tasks).
        Он принимает в конструкторе объект Session из SQLAlchemy, который представляет соединение с базой данных.
        Метод get_task(self, task_id) возвращает задачу (Tasks) по ее идентификатору. Если задача не найдена, он генерирует исключение ValueError.
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

        with self.db_session() as session:
            query = select(Tasks)
            tasks: list[Tasks] = session.execute(query).scalars().all()
            if not tasks:
                raise ValueError("No tasks found")
            return tasks

    def get_task(self, task_id: int) -> Tasks | None:
        with self.db_session() as session:
            query = select(Tasks).where(Tasks.id == task_id)
            task: Tasks = session.execute(query).scalar_one_or_none()
            return task

    def create_task(self, task: TaskSchema) -> int:
        task_model = Tasks(name=task.name, pomodoro_count=task.pomodoro_count, category_id=task.category_id)
        with self.db_session() as session:
            session.add(task_model)
            session.commit()
            return task_model.id

    def delete_task(self, task_id: int) -> None:
        with self.db_session() as session:
            query = delete(Tasks).where(Tasks.id == task_id)
            session.execute(query)
            session.commit()

    def get_tasks_by_category_name(self, category_name: str) -> list[Tasks]:
        """
        Получает список задач, которые принадлежат категории с указанным именем.

        :param category_name: Имя категории
        :return: Список задач
        """
        with self.db_session() as session:
            query = session.query(Tasks).join(Categories, Tasks.category_id == Categories.id).filter(
                Categories.name == category_name)
            task: list[Tasks] = query.all()
            if not task:
                raise ValueError(f"No tasks found for category '{category_name}'")
            return task

    # def get_task_by_category_name(self, category_name: str) -> list[Tasks]:
    #     query = select(Tasks).join(Categories, Tasks.category_id == Categories.id).where(
    #         Categories.name == category_name)
    #     with self.db_session() as session:
    #         task: list[Tasks] = session.execute(query).scalars().all()
    #         return task

    def update_task_name(self, task_id: int, name: str) -> Tasks:
        query = update(Tasks).where(Tasks.id == task_id).values(name=name).returning(Tasks.id)
        with self.db_session() as session:
            task_id: int = session.execute(query).scalar_one_or_none()
            session.commit()
            return self.get_task(task_id)
