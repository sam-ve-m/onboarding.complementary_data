# Standards
import asyncio
from hashlib import sha1
from typing import List, Optional

# SPHINX
# from .base_repository import OracleBaseRepository
from func.src.repositories.oracle.base_repository import OracleBaseRepository

# # # Third party
# # import nest_asyncio
#
# nest_asyncio.apply()


class SinacorRepository(OracleBaseRepository):

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

    # @classmethod
    # async def query_with_cache(cls, sql: str) -> list:
    #     _sha1 = sha1()
    #     _sha1.update(str(sql).encode())
    #     partial_key = _sha1.hexdigest()
    #     key = f"sinacor_types:{partial_key}"
    #     value = await cls.cache.get(key=key)
    #     if not value:
    #         partial_value = await cls.query(sql=sql)
    #         value = {"value": partial_value}
    #         await cls.cache.set(key=key, value=value, ttl=86400)
    #
    #     value = value.get("value")
    #     return value


if __name__ == "__main__":
    import asyncio
    a = asyncio.run(SinacorRepository.get_marital_status(code=2))
    print(a)
