from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# engine = create_engine('sqlite:///' + os.path.join(settings.project_root, settings.sqlite_db_name))
# engine = create_engine('sqlite:////mnt/c/db/pomodoro.sqlite')       # BD sqlite3
engine = create_engine('postgresql+psycopg2://postgres:password@0.0.0.0:5432/pomodoro')       # BD postgresql
"""

sqlite:///path/to/database.db

Здесь три слэша (///) означают, что файл находится в файловой системе, а не в сетевом ресурсе.

Первые два слэша (//) указывают на то, что это файл, а не сетевой ресурс. Третий и четвертый слэши (////) необходимы, 
чтобы указать, что файл находится на диске Windows, доступном через каталог /mnt/ в WSL.

Таким образом, четыре слэша в начале пути позволяют корректно указать путь к файлу базы данных, расположенной 
на диске Windows, из среды WSL.
"""

Session = sessionmaker(bind=engine)


def get_db_session() -> Session:
    return Session
