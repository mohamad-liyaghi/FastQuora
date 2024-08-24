from passlib.context import CryptContext

context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class PasswordHandler:
    @staticmethod
    async def hash_password(password: str) -> str:
        return context.hash(password)

    @staticmethod
    async def verify_password(hashed_password: str, password: str) -> bool:
        return context.verify(password, hashed_password)
