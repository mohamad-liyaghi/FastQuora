from fastapi import Depends
from app.controllers import (
    AuthController,
    ProfileController,
    QuestionController,
    AnswerController,
    VoteController,
)
from core.database import get_db
from core.redis import get_redis


class Factory:
    """
    Factory class to create instances of controllers
    """

    @staticmethod
    def get_auth_controller(db: Depends = Depends(get_db), redis: Depends = Depends(get_redis)) -> AuthController:
        """
        Returns a UserController instance
        """
        return AuthController(redis_session=redis, session=db)

    @staticmethod
    def get_profile_controller(db: Depends = Depends(get_db), redis: Depends = Depends(get_redis)) -> ProfileController:
        """
        Returns a ProfileController instance
        """
        return ProfileController(redis_session=redis, session=db)

    @staticmethod
    def get_question_controller(
        db: Depends = Depends(get_db), redis: Depends = Depends(get_redis)
    ) -> QuestionController:
        """
        Returns a QuestionController instance
        """
        return QuestionController(redis_session=redis, session=db)

    @staticmethod
    def get_answer_controller(db: Depends = Depends(get_db), redis: Depends = Depends(get_redis)) -> AnswerController:
        """
        Returns an AnswerController instance
        """
        return AnswerController(redis_session=redis, session=db)

    @staticmethod
    def get_vote_controller(db: Depends = Depends(get_db), redis: Depends = Depends(get_redis)) -> VoteController:
        """
        Returns a VoteController instance
        """
        return VoteController(redis_session=redis, session=db)
