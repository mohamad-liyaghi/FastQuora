import pytest
from elasticsearch import NotFoundError


class TestElasticRepository:
    @pytest.fixture(autouse=True)
    def setup(self, elastic_repository, elastic_record, user):
        self.repository = elastic_repository
        self.record = elastic_record
        self.user = user

    @pytest.mark.asyncio
    async def test_retrieve_valid_index(self):
        response = await self.repository.retrieve(self.user.id)
        assert response["_source"]["id"] == self.user.id

    @pytest.mark.asyncio
    async def test_retrieve_invalid_index_fails(self):
        with pytest.raises(NotFoundError):
            await self.repository.retrieve(999)
