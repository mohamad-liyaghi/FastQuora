from passlib.context import CryptContext
import os

context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class PasswordHandler:
    @staticmethod
    async def hash_password(password: str) -> str:
        if os.getenv("TESTING", "0") == "1":
            return password[::-1]
        return context.hash(password)

    @staticmethod
    async def verify_password(hashed_password: str, password: str) -> bool:
        if os.getenv("TESTING", "0") == "1":
            return hashed_password == password[::-1]
        return context.verify(password, hashed_password)
