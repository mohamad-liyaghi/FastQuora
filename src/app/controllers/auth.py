from sqlalchemy.ext.asyncio import AsyncSession
from redis import Redis
from app.models import User
from core.controllers import BaseController
from core.handlers import PasswordHandler


class AuthController(BaseController):
    def __init__(self, session: AsyncSession, redis_session: Redis):
        self.model = User
        super().__init__(model=self.model, session=session, redis_session=redis_session)

    async def register(self, data: dict) -> User:
        data = data.copy()
        hashed_password = await PasswordHandler.hash_password(data.get("password"))
        data.pop("password")
        data.setdefault("password", hashed_password)

        return await self.create(data=data)
