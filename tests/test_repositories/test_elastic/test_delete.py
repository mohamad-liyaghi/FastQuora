import pytest
from elasticsearch import NotFoundError


class TestElasticRepository:
    @pytest.fixture(autouse=True)
    def setup(self, elastic_repository, elastic_record, user):
        self.repository = elastic_repository
        self.record = elastic_record
        self.user = user

    @pytest.mark.asyncio
    async def test_delete_valid_index(self):
        response = await self.repository.delete(self.user.id)
        assert response["result"] == "deleted"

    @pytest.mark.asyncio
    async def test_delete_invalid_index_fails(self):
        with pytest.raises(NotFoundError):
            await self.repository.delete(999)
