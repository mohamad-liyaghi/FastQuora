from core.repositories import DatabaseRepository


class BaseController:
    def __init__(self, model, session):
        self.model = model
        self.database_repository = DatabaseRepository(model=model, session=session)

    async def create(self, **kwargs):
        return await self.database_repository.create(**kwargs)

    async def retrieve(self, **kwargs):
        return await self.database_repository.retrieve(**kwargs)

    async def update(self, instance, **kwargs):
        return await self.database_repository.update(instance=instance, **kwargs)

    async def delete(self, instance):
        return await self.database_repository.delete(instance=instance)
