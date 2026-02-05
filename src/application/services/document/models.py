from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from src.application.core.database.database import Base
from src.application.core.mixins.mixins import BaseMixin


class Document(Base, BaseMixin):
    document_name: Mapped[str] = mapped_column(String)
    filename: Mapped[str] = mapped_column(String)
    document_url: Mapped[str] = mapped_column(String)
    user_id: Mapped[int] = mapped_column(Integer)
    participiant_id: Mapped[int] = mapped_column(Integer)
    status: Mapped[str] = mapped_column(String, default="Sended")

    # Uses only for if status equals Rejected
    reason: Mapped[str] = mapped_column(String, nullable=True)
