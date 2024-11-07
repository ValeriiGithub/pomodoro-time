from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# engine = create_engine('sqlite:///' + os.path.join(settings.project_root, settings.sqlite_db_name))
engine = create_engine('sqlite:///pomodoro.sqlite')

Session = sessionmaker(bind=engine)


def get_db_session() -> Session:
    return Session
