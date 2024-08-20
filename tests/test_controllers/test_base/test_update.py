import pytest
import pytest_asyncio
from sqlalchemy.exc import IntegrityError
from mocks import generate_fake_user_data


class TestBaseController:
    @pytest_asyncio.fixture(autouse=True)
    async def setup(self, test_session, user, base_controller):
        self.data = generate_fake_user_data()
        self.controller = base_controller
        self.user = user

    @pytest.mark.asyncio
    async def test_update_existing_record(self):
        new_first_name = "new name"
        result = await self.controller.update(self.user, {"first_name": new_first_name})
        assert result.first_name == new_first_name

    @pytest.mark.asyncio
    async def test_update_existing_record_with_invalid_data(self):
        with pytest.raises(IntegrityError):
            await self.controller.update(self.user, {"email": None})
