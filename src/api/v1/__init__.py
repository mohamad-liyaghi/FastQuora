from fastapi import APIRouter
from .auth import router as auth_router
from .profile import router as profile_router
from .question import router as question_router
from .answer import router as answer_router

v1_router = APIRouter()
v1_router.include_router(auth_router, prefix="/auth")
v1_router.include_router(profile_router, prefix="/profiles")
v1_router.include_router(question_router, prefix="/questions")
v1_router.include_router(answer_router, prefix="/answers")
