from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

from src.application.core.database.database import Base
from src.application.core.mixins.mixins import BaseMixin


class User(Base, BaseMixin):
    username: Mapped[str] = mapped_column(String(30))
    role: Mapped[str] = mapped_column(String)
    password: Mapped[str] = mapped_column(String)
