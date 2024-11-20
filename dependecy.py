# Dependency
from fastapi import Depends, Request, security, Security
from sqlalchemy.orm import Session

from settings import settings
from database import get_db_session
from cache import get_redis_connection
from repository import TaskRepository, TaskCacheRepository, UserRepository
from service import TaskService, UserService, AuthService


def get_tasks_repository(db_session: Session = Depends(get_db_session)) -> TaskRepository:
    """
    Назначение функции get_task_repository():

    Эта функция предоставляет единый точку доступа для получения экземпляра TaskRepository.
    Она скрывает детали создания TaskRepository, такие, как получение объекта Session из базы данных.
    Это позволяет легко заменить реализацию TaskRepository (например, если вы решите использовать другую базу данных или другой ORM) без необходимости изменять код, который использует TaskRepository.
    Такой подход называется "внедрение зависимостей" (Dependency Injection) и помогает сделать код более модульным, тестируемым и гибким.

    Таким образом, функция get_task_repository() играет важную роль в обеспечении правильного создания и использования TaskRepository в  приложении.
    :return: TaskRepository
    """
    return TaskRepository(db_session)


def get_tasks_cache_repository() -> TaskCacheRepository:
    """
    Получаем закешированные таски
    :return:
    """
    redis_connection = get_redis_connection()
    # redis_connection = get_cache_session()      # Асинхронное подключение
    return TaskCacheRepository(redis_connection)


def get_task_service(
        task_repository: TaskRepository = Depends(get_tasks_repository),
        task_cache: TaskCacheRepository = Depends(get_tasks_cache_repository),
) -> TaskService:
    """
    Получаем сервис для работы с тасками
    :return:
    """
    return TaskService(
        task_repository=task_repository,
        task_cache=task_cache,
    )


def get_user_repository(db_session: Session = Depends(get_db_session)) -> UserRepository:
    """
    Получаем репозиторий для работы с пользователями
    :return:
    """
    return UserRepository(db_session=db_session)


def get_auth_service(
        user_repository: UserRepository = Depends(get_user_repository)
) -> AuthService:
    return AuthService(user_repository=user_repository, settings=settings)


def get_user_service(
        user_repository: UserRepository = Depends(get_user_repository),
        auth_service: AuthService = Depends(get_auth_service),
) -> UserService:
    return UserService(user_repository=user_repository, auth_service=auth_service)


reusable_oauth2 = security.HTTPBearer()

def get_request_user_id(
        auth_service: AuthService = Depends(get_auth_service),
        token: security.http.HTTPAuthorizationCredentials = Security(reusable_oauth2)
) -> int:
    """
    Получаем идентификатор пользователя из заголовка Authorization
    :param request:
    :return:
    """
    user_id = auth_service.get_user_id_from_access_token(token.credentials)
    return user_id

    # bearer_token = request.headers.get("Authorization")
    # if bearer_token:
    #     access_token_parts = bearer_token.split(" ")
    #     if len(access_token_parts) == 2:
    #         token_type, access_token = access_token_parts
    #         if token_type == "Bearer":
    #             try:
    #                 user_id = jwt.decode(access_token, settings.SECRET_KEY, algorithms=["HS256"])["sub"]
    #                 return user_id
    #             except jwt.InvalidTokenError:
    #                 pass
    # raise HTTPException(status_code=401, detail="Could not validate credentials")