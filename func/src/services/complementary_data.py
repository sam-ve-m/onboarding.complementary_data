from ..repositories.mongo_db.user.repository import UserRepository
from ..domain.exceptions import UserUniqueIdNotExists
from ..domain.complementary_data.model import ComplementaryDataModel
from ..transports.audit.transport import Audit
from ..domain.exceptions import ErrorOnUpdateUser, InvalidSpouseCpf


class ComplementaryDataService:
    def __init__(self, unique_id, complementary_data_validated):
        self.unique_id = unique_id
        self.complementary_data_model = ComplementaryDataModel(complementary_data_validated=complementary_data_validated, unique_id=unique_id)

    async def update_user_with_complementary_data(self) -> bool:
        await self._validate_cpf_is_not_the_same()
        user_complementary_data = await self.complementary_data_model.get_user_update_template()
        await Audit.register_log(complementary_data_model=self.complementary_data_model)
        user_updated = await UserRepository.update_one_with_user_complementary_data(
            unique_id=self.unique_id,
            user_complementary_data=user_complementary_data
        )
        if not user_updated.acknowledged:
            raise ErrorOnUpdateUser
        return True

    async def _get_user(self) -> dict:
        user = await UserRepository.find_one_by_unique_id(unique_id=self.unique_id)
        if not user:
            raise UserUniqueIdNotExists
        return user

    async def _validate_cpf_is_not_the_same(self) -> bool:
        user = await self._get_user()
        user_cpf = user["identifier_document"].get("cpf")
        if self.complementary_data_model.spouse is not None\
                and self.complementary_data_model.spouse.cpf == user_cpf:
            raise InvalidSpouseCpf
        return True
