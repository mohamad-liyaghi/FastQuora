from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from redis import Redis
from uuid import UUID
from app.models import User
from core.controllers import BaseController


class ProfileController(BaseController):
    def __init__(self, session: AsyncSession, redis_session: Redis):
        self.model = User
        super().__init__(model=self.model, session=session, redis_session=redis_session)

    async def get_by_uuid(self, uuid: UUID) -> User:
        user = await self.retrieve(uuid=uuid)
        if not user:
            raise HTTPException(status_code=404, detail="User not found.")
        return user
