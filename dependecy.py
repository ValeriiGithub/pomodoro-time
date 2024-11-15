# Dependency
from database import get_db_session
# from cache import get_redis_connection
from cache import get_cache_session
from repository import TaskRepository, TaskCacheRepository


def get_tasks_repository() -> TaskRepository:
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

def get_tasks_cache_repository() -> TaskCacheRepository:
    """
    Получаем закешированные таски
    :return:
    """
    redis_connection = get_cache_session()
    return TaskCacheRepository(redis_connection)
