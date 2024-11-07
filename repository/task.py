from sqlalchemy import select, delete
from sqlalchemy.orm import Session

from database import Tasks, Categories, get_db_session


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
            if tasks is None:
                raise ValueError("No tasks found")
            return tasks

    def get_task(self, task_id: int) -> Tasks | None:
        with self.db_session() as session:
            query = select(Tasks).where(Tasks.id == task_id)
            task: Tasks = session.execute(query).scalar_one_or_none()
            return task

    def create_task(self, task: Tasks) -> None:
        with self.db_session() as session:
            session.add(task)
            session.commit()

    def delete_task(self, task_id: int) -> None:
        with self.db_session() as session:
            query = delete(Tasks).where(Tasks.id == task_id)
            session.execute(query)
            session.commit()

    def get_tasks_by_category_name(self, category_name: str) -> list[Tasks]:
        with self.db_session() as session:
            query = session.query(Tasks).join(Categories, Tasks.category_id == Categories.id).filter(
                Categories.name == category_name)
            tasks: list[Tasks] = query.all()
            if not tasks:
                raise ValueError(f"No tasks found for category '{category_name}'")
            return tasks

    # def get_tasks_by_category_name(self, category_name: str) -> list[Tasks]:
    #     query = select(Tasks).join(Categories, Tasks.category_id == Categories.id).where(Categories.name ==
    #                                                                                      category_name)
    #     with self.db_session as session:
    #         tasks: list[Tasks] = session.execute(query).scalars().all()
    #         if not tasks:
    #             raise ValueError(f"No tasks found for category '{category_name}'")
    #         return tasks

    # def get_tasks_by_category_name(self, category_name: str) -> list[Tasks]:
    #     with self.db_session as session:
    #         query = session.query(Tasks).join(Categories, Tasks.category_id == Categories.id).filter(
    #             Categories.name == category_name)
    #         tasks: list[Tasks] = query.all()
    #         if not tasks:
    #             raise ValueError(f"No tasks found for category '{category_name}'")
    #         return tasks

    def get_tasks_by_category_name_2(self, category_name):
        with self.db_session as session:
            query = session.query(Tasks).join(Categories, Tasks.category_id == Categories.id).filter(Categories.name == category_name)
            tasks = query.all()
            return [task for task in tasks]

    def get_tasks_by_category_name_3(self, category_name):
        """
        работает
        :param category_name:
        :return:
        """
        session = self.db_session()
        try:
            query = session.query(Tasks).join(Categories, Tasks.category_id == Categories.id).filter(Categories.name == category_name)
            tasks = query.all()
            return tasks
        finally:
            session.close()


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


if __name__ == "__main__":
    task_repo = get_task_repository()
    print(task_repo)
    print(task_repo.get_task(2))
    print(task_repo.get_task(2).name)
    print(len(task_repo.get_tasks()), task_repo.get_tasks())
    print(task_repo.get_tasks_by_category_name("work"))
    for i in range(2, 6):
        print(task_repo.get_task(i).name)

    task = task_repo.get_task(1)
    print(dir(task))

    task = task_repo.get_task(1)
    print(task.__dir__)
    task = task_repo.get_task(1)
    print(task.__doc__)

    # task = task_repo.get_task(1)
    # print(vars(task))

    import inspect

    task = task_repo.get_task(1)
    print(inspect.getmembers(task))