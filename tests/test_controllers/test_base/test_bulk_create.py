import pytest
from mocks import generate_fake_user_data


class TestBaseController:
    @pytest.fixture(autouse=True)
    def setup(self, test_session, base_controller):
        self.controller = base_controller
        self.data = generate_fake_user_data()
        self.another_data = generate_fake_user_data()

    @pytest.mark.asyncio
    async def test_create_with_valid_data_should_return_instances(self):
        instances = await self.controller.bulk_create([self.data, self.another_data])
        assert len(instances) == 2

    @pytest.mark.asyncio
    async def test_create_with_invalid_data_should_raise_exception(self):
        with pytest.raises(ValueError):
            await self.controller.bulk_create([])
