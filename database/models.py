from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Task(DeclarativeBase):
    __tablename__ = 'Tasks'

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = Mapped()
    pomodoro_count: Mapped[int] = Mapped()
    category_id: Mapped[int] = Mapped(foreign_key='categories.id')

class Category(DeclarativeBase):
    __tablename__ = 'Categories'

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = Mapped()
