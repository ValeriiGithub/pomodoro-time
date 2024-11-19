from typing import Optional

from sqlalchemy.orm import Mapped, mapped_column

from database import Base


class UserProfile(Base):
    # __tablename__ = 'UserProfile'

    id: Mapped[int] = mapped_column(primary_key=True, nullable=False)
    username: Mapped[str] = mapped_column(nullable=False)
    password: Mapped[str] = mapped_column(nullable=False)
    access_token: Mapped[Optional[str]]