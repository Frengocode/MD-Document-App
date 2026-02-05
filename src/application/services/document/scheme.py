from enum import Enum
from typing import Optional, Self

from pydantic import BaseModel, model_validator

from src.application.services.document.exception import EmptyReasonException
from src.application.services.user.scheme import SUser


class Status(str, Enum):
    REJECTED = "rejected"


class SUpdateStatus(BaseModel):
    id: int
    status: Status
    reason: Optional[str]

    @model_validator(mode="after")
    def validate_reason(self) -> Self:
        if self.status == Status.REJECTED.value:
            if not self.reason:
                raise EmptyReasonException()
            return self


class SDocument(BaseModel):
    id: int
    user: Optional[SUser] = None
    participiant_id: int
    document_name: str
    document_url: str
    reason: Optional[str] = None
    status: str
