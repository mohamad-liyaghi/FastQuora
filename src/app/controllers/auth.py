from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from redis import Redis
from app.models import User
from core.controllers import BaseController
from core.handlers import PasswordHandler, JWTHandler


class AuthController(BaseController):
    def __init__(self, session: AsyncSession, redis_session: Redis):
        self.model = User
        super().__init__(model=self.model, session=session, redis_session=redis_session)

    async def register(self, data: dict) -> User:
        data = data.copy()

        if await self.database_repository.retrieve(email=data.get("email")):
            raise HTTPException(
                status_code=409,
                detail="User with this email already exists.",
            )

        if await self.database_repository.retrieve(nickname=data.get("nickname")):
            raise HTTPException(
                status_code=409,
                detail="User with this nickname already exists.",
            )

        hashed_password = await PasswordHandler.hash_password(data.get("password"))
        data.pop("password")
        data.setdefault("password", hashed_password)

        return await self.create(data=data)

    async def login(self, email: str, password: str) -> str:
        user = await self.database_repository.retrieve(email=email)

        if not user:
            raise HTTPException(status_code=404, detail="User with this email does not exist.")

        if not await PasswordHandler.verify_password(password, user.password):
            raise HTTPException(status_code=403, detail="Invalid password.")

        access_token = await JWTHandler.create_access_token(data={"user_uuid": str(user.uuid)})
        return access_token
