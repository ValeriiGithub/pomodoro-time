from pydantic_settings import BaseSettings

# REDIS_HOST = 'localhost'
# REDIS_PORT = 6379


class Settings(BaseSettings):
    # PostgreSQL settings
    DB_HOST: str = '0.0.0.0'
    DB_PORT: int = 5432
    DB_USER: str = 'postgres'
    DB_PASSWORD: str = 'password'
    DB_NAME: str = 'pomodoro'
    DB_DRIVER: str = 'postgresql+psycopg2'

    # Redis settings
    CACHE_HOST: str = '0.0.0.0'
    CACHE_PORT: int = 6379
    CACHE_DB: int = 0

    @property
    def db_url(self):
        return f'{self.DB_DRIVER}://{self.DB_USER}:{self.DB_PASSWORD}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}'


    # sqlite_db_name: str = '/mnt/c/db/pomodoro.sqlite'
    postgres_db_name: str = 'postgresql+psycopg2://postgres:password@0.0.0.0:5432/pomodoro'


# Инициализация экземпляра settings в файле settings.py и его импорт в
# другие части приложения. Это позволяет избежать повторного создания
# экземпляра и гарантирует, что переменные окружения будут загружены только
# один раз, что может быть более эффективно и удобно.
settings = Settings()
