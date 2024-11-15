from pydantic_settings import BaseSettings

REDIS_HOST = 'localhost'
REDIS_PORT = 6379


class Settings(BaseSettings):
    # sqlite_db_name: str = '/mnt/c/db/pomodoro.sqlite'
    postgres_db_name: str = 'postgresql+psycopg2://postgres:password@0.0.0.0:5432/pomodoro'


# Инициализация экземпляра settings в файле settings.py и его импорт в
# другие части приложения. Это позволяет избежать повторного создания
# экземпляра и гарантирует, что переменные окружения будут загружены только
# один раз, что может быть более эффективно и удобно.
settings = Settings()
