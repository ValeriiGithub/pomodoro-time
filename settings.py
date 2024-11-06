from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    GOOGLE_TOKEN_ID: str = "dfjijj3409u309j49009r3ijf034jife"


# Инициализация экземпляра settings в файле settings.py и его импорт в
# другие части приложения. Это позволяет избежать повторного создания
# экземпляра и гарантирует, что переменные окружения будут загружены только
# один раз, что может быть более эффективно и удобно.
settings = Settings()
