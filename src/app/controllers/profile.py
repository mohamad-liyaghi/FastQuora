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
        user = await self.retrieve(uuid=uuid, check_cache=True)
        if not user:
            raise HTTPException(status_code=404, detail="User not found.")
        return user

    async def update_user(self, user_uuid: UUID, requesting_user: User, data: dict) -> User:
        if not data:
            raise HTTPException(status_code=400, detail="No data provided to update the user.")

        user = await self.get_by_uuid(user_uuid)
        if user.uuid != requesting_user.uuid:
            raise HTTPException(status_code=403, detail="You are not allowed to update this user.")

        if email := data.get("email"):
            if await self.retrieve(email=email):
                raise HTTPException(status_code=409, detail="User with this email already exists.")

        if nickname := data.get("nickname"):
            if await self.retrieve(nickname=nickname):
                raise HTTPException(status_code=409, detail="User with this nickname already exists.")

        return await self.update(user, data)
