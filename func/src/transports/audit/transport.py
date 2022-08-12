# Jormungandr - Onboarding
from ...domain.exceptions.exceptions import ErrorOnSendAuditLog
from ...domain.enums.types import QueueTypes
from ...domain.complementary_data.model import ComplementaryDataModel

# Third party
from decouple import config
from etria_logger import Gladsheim
from persephone_client import Persephone


class Audit:
    audit_client = Persephone

    @classmethod
    async def send_audit_log(cls, complementary_data_model: ComplementaryDataModel):
        message = await complementary_data_model.get_audit_template()
        partition = QueueTypes.USER_COMPLEMENTARY_DATA.value
        topic = config("PERSEPHONE_TOPIC_USER")
        schema_name = config("PERSEPHONE_COMPLEMENTARY_DATA_SCHEMA")
        (
            success,
            status_sent_to_persephone,
        ) = await cls.audit_client.send_to_persephone(
            topic=topic,
            partition=partition,
            message=message,
            schema_name=schema_name,
        )
        if not success:
            Gladsheim.error(
                message="Audit::register_user_log::Error on trying to register log"
            )
            raise ErrorOnSendAuditLog
