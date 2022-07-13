# Standards
from typing import List

# SPHINX
from .base_repository import OracleBaseRepository


class EnumerateRepository(OracleBaseRepository):

    @staticmethod
    def tuples_to_dict_list(fields: List[str], values: List[tuple]) -> List:
        dicts_result = list()
        for value in values:
            dicts_result.append(dict(zip(fields, value)))
        return dicts_result

    @classmethod
    async def get_nationality(cls, code) -> list:
        sql = f"""
            SELECT CODE as code, DESCRIPTION as description
            FROM USPIXDB001.SINCAD_EXTERNAL_NATIONALITY
            WHERE CODE = {code}
        """
        tuple_result = await cls.query(sql=sql)
        dict_result = cls.tuples_to_dict_list(
            fields=["code", "description"], values=tuple_result
        )
        return dict_result

    @classmethod
    async def get_country(cls, country_acronym) -> list:
        sql = f"""
            SELECT SG_PAIS as initials, NM_PAIS as description
            FROM CORRWIN.TSCPAIS
            WHERE SG_PAIS = {country_acronym}
        """
        tuple_result = await cls.query(sql=sql)
        dict_result = cls.tuples_to_dict_list(
            fields=["code", "description"], values=tuple_result
        )
        return dict_result

    @classmethod
    async def get_marital_status(cls, code) -> list:
        sql = f"""
            SELECT CODE as code, DESCRIPTION as description
            FROM USPIXDB001.SINCAD_EXTERNAL_MARITAL_STATUS
            WHERE CODE = {code}
        """
        tuple_result = await cls.query(sql=sql)

        return tuple_result
