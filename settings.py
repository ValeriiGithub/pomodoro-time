from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    sqlite_db_name: str = '/mnt/c/db/pomodoro.sqlite'


# Инициализация экземпляра settings в файле settings.py и его импорт в
# другие части приложения. Это позволяет избежать повторного создания
# экземпляра и гарантирует, что переменные окружения будут загружены только
# один раз, что может быть более эффективно и удобно.
settings = Settings()
