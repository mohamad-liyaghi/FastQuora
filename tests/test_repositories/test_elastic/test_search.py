import pytest


class TestElasticRepository:
    @pytest.fixture(autouse=True)
    def setup(self, elastic_repository, elastic_record, user):
        self.repository = elastic_repository
        self.record = elastic_record
        self.user = user

    @pytest.mark.asyncio
    async def test_search_valid_index(self):
        response = await self.repository.search({"query": {"match": {"id": self.user.id}}})
        assert response["_shards"]["successful"] == 1

    @pytest.mark.asyncio
    async def test_search_invalid_index_fails(self):
        response = await self.repository.search({"query": {"match": {"id": 999}}})
        assert response["hits"]["total"]["value"] == 0
