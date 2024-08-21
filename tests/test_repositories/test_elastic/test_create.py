import pytest
from mocks import generate_fake_user_data


class TestElasticRepository:
    @pytest.fixture(autouse=True)
    def setup(self, test_session, elastic_repository):
        self.repository = elastic_repository
        self.data = generate_fake_user_data()

    @pytest.mark.asyncio
    async def test_create_index(self):
        self.data["id"] = 1
        response = await self.repository.create(self.data)
        assert response["result"] == "created"

    @pytest.mark.asyncio
    async def test_create_index_with_invalid_data_fails(self):
        with pytest.raises(ValueError):
            await self.repository.create({})
