from ..domain.models.device_info import DeviceInfo
from ..domain.validators.validator import ComplementaryData
from ..repositories.mongo_db.user.repository import UserRepository
from ..domain.exceptions.exceptions import ErrorOnUpdateUser
from ..domain.complementary_data.model import ComplementaryDataModel
from ..transports.audit.transport import Audit


class ComplementaryDataService:
    @staticmethod
    async def update_user_with_complementary_data(
        payload_validated: ComplementaryData, unique_id: str, device_info: DeviceInfo
    ) -> bool:
        complementary_data_model = ComplementaryDataModel(
            payload_validated=payload_validated,
            unique_id=unique_id,
            device_info=device_info,
        )
        user_complementary_data_template = (
            await complementary_data_model.get_user_update_template()
        )
        await Audit.record_message_log(
            complementary_data_model=complementary_data_model
        )
        user_updated = await UserRepository.update_one_with_user_complementary_data(
            unique_id=unique_id,
            user_complementary_data=user_complementary_data_template,
        )
        if not user_updated.matched_count:
            raise ErrorOnUpdateUser()
        return True
