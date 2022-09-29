# Jormungandr
from .base_repository import OracleBaseRepository

# Standards
from typing import List


class EnumerateRepository(OracleBaseRepository):
    @classmethod
    async def get_nationality(cls, nationality_code: int) -> List:
        sql = f"""
            SELECT 1
            FROM USPIXDB001.SINCAD_EXTERNAL_NATIONALITY
            WHERE CODE = :filter
        """
        result = await cls.query(sql=sql, filters=[nationality_code])

        return result

    @classmethod
    async def get_country(cls, country_acronym: str) -> List:
        sql = f"""
            SELECT 1
            FROM CORRWIN.TSCPAIS
            WHERE SG_PAIS = :filter
        """
        result = await cls.query(sql=sql, filters=[country_acronym])

        return result

    @classmethod
    async def get_marital_status(cls, marital_code: int) -> List:
        sql = f"""
            SELECT 1
            FROM USPIXDB001.SINCAD_EXTERNAL_MARITAL_STATUS
            WHERE CODE = :filter
        """
        result = await cls.query(sql=sql, filters=[marital_code])

        return result
