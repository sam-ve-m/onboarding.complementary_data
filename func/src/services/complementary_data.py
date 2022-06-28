from ..repositories.mongo_db.user.repository import UserRepository
from ..domain.exceptions import UserUniqueIdNotExists


class ComplementaryDataService:
    def __init__(self, unique_id, complementary_data_validated):
        self.unique_id = unique_id
        self.complementary_data = complementary_data_validated

    async def update_user_complementary_data(self):
        current_user = await self._get_user()
        pass

    async def _get_user(self):
        user = await UserRepository.find_one_by_unique_id(unique_id=self.unique_id)
        if not user:
            raise UserUniqueIdNotExists
        return user

    @staticmethod
    async def get_user_complementary_data_for_user_update(
            user_complementary_data: dict,
    ):
        return {
            "marital": {
                "status": user_complementary_data.get("marital_status"),
                "spouse": user_complementary_data.get("spouse"),
            }
        }