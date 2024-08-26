import pytest_asyncio
from app.models import Question


@pytest_asyncio.fixture(scope="class")
async def question(question_controller, user) -> Question:
    data = {
        "title": "Test Title",
        "content": "Test Content",
        "user_id": user.id,
    }
    return await question_controller.create(data=data)


@pytest_asyncio.fixture(scope="class")
async def another_question(question_controller, another_user) -> Question:
    data = {
        "title": "Another Test Title",
        "content": "Another Test Content",
        "user_id": another_user.id,
    }
    return await question_controller.create(data=data)
