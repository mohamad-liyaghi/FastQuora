import pytest_asyncio
from app.models import Answer


@pytest_asyncio.fixture(scope="class")
async def answer(answer_controller, user, question) -> Answer:
    data = {
        "user_id": user.id,
        "question_id": question.id,
        "content": "This is a test answer",
    }
    return await answer_controller.create(data=data)


@pytest_asyncio.fixture(scope="class")
async def another_answer(answer_controller, another_user, another_question) -> Answer:
    data = {
        "user_id": another_user.id,
        "question_id": another_question.id,
        "content": "This is another test answer",
    }
    return await answer_controller.create(data=data)


@pytest_asyncio.fixture(scope="class")
async def answer_with_parent(answer_controller, user, question, answer) -> Answer:
    data = {
        "user_id": user.id,
        "question_id": question.id,
        "content": "This is a test answer with parent",
        "parent_id": answer.id,
    }
    return await answer_controller.create(data=data)
