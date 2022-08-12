# Jormungandr
from .base_repository import OracleBaseRepository

# Standards
from typing import List


class EnumerateRepository(OracleBaseRepository):
    @classmethod
    async def get_nationality(cls, code) -> List:
        sql = f"""
            SELECT CODE as code, DESCRIPTION as description
            FROM USPIXDB001.SINCAD_EXTERNAL_NATIONALITY
            WHERE CODE = {code}
        """
        result = await cls.query(sql=sql)

        return result

    @classmethod
    async def get_country(cls, country_acronym: str) -> List:
        sql = f"""
            SELECT SG_PAIS as initials, NM_PAIS as description
            FROM CORRWIN.TSCPAIS
            WHERE SG_PAIS = "{country_acronym}"
        """
        result = await cls.query(sql=sql)

        return result

    @classmethod
    async def get_marital_status(cls, code: int) -> List:
        sql = f"""
            SELECT CODE as code, DESCRIPTION as description
            FROM USPIXDB001.SINCAD_EXTERNAL_MARITAL_STATUS
            WHERE CODE = {code}
        """
        result = await cls.query(sql=sql)

        return result
