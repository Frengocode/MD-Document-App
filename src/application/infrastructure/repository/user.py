from dataclasses import dataclass
from typing import Any, List

from sqlalchemy import Result, Select, select
from sqlalchemy.ext.asyncio import AsyncSession

from src.application.core.repository.user import ABCUserRepository
from src.application.services.user.models import User
from src.application.services.user.scheme import SCreateUserRequest, SUpdateUserRequest


@dataclass
class UserRepository(ABCUserRepository):
    session: AsyncSession
    model = User

    async def create(self, request: SCreateUserRequest) -> User:
        user: User = self.model(**request.model_dump())
        self.session.add(user)
        await self.session.commit()
        await self.session.refresh(user)
        return user

    async def get(self, **filters: Any) -> User | None:
        stmt: Select[User] = select().filter_by(**filters)
        result: Result[User] = await self.session.execute(stmt)
        return result

    async def get_all(self, offset: int, limit: int, **filters: Any) -> List[User]:
        stmt: Select[User] = (
            select(self.model).offset(offset).limit(limit).filter_by(**filters)
        )
        result: Result[User] = await self.session.execute(stmt)
        return result.scalars().all()

    async def update(self, request: SUpdateUserRequest, **filters: Any) -> User:
        stmt: Select[User] = select(self.model).filter_by(**filters)
        result: Result[User] = await self.session.execute(stmt)
        user: User = result.scalars().first()

        # Updating fields
        for name, value in request.model_dump().items():
            setattr(user, name, value)
        await self.session.commit()
        await self.session.refresh(user)
        return user
