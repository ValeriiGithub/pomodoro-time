from sqlalchemy.orm import Mapped, mapped_column, declarative_base

Base = declarative_base()


class Tasks(Base):
    __tablename__ = 'Tasks'

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = Mapped()
    pomodoro_count: Mapped[int] = Mapped()
    category_id: Mapped[int] = Mapped(foreign_key='categories.id')


class Categories(Base):
    __tablename__ = 'Categories'

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = Mapped()
