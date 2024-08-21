import pytest
from elasticsearch import NotFoundError


class TestElasticRepository:
    @pytest.fixture(autouse=True)
    def setup(self, elastic_repository, elastic_record, user):
        self.repository = elastic_repository
        self.record = elastic_record
        self.data = {"nick_name": "updated"}
        self.user = user

    @pytest.mark.asyncio
    async def test_update_existing_record(self):
        result = await self.repository.update(self.user.id, self.data)
        assert result["result"] == "updated"
        assert int(result["_id"]) == self.user.id

    @pytest.mark.asyncio
    async def test_update_non_existing_record(self):
        with pytest.raises(NotFoundError):
            await self.repository.update(1000, self.data)
