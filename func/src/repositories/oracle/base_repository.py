# Jormungandr - Onboarding
from ...domain.exceptions import InternalServerError
from ...infrastructures.oracle.infrastrucuture import OracleInfrastructure

# Standards
from typing import List

# Third Party
from etria_logger import Gladsheim
import cx_Oracle


class OracleBaseRepository:

    infra = OracleInfrastructure

    @classmethod
    async def query(cls, sql: str) -> list:
        try:
            async with cls.infra.get_connection() as cursor:
                await cursor.execute(sql)
                rows = await cursor.fetchall()
                rows = cls._normalize_encode(rows=rows)
                return rows

        except cx_Oracle.DataError as e:
            (error,) = e.args
            message = f"Oracle-Error-Code: {error.code}. Oracle-Error-Message: {error.message} - Sql: {sql} - Oracle-ex: {e}"
            Gladsheim.error(error=e, message=message)
            raise InternalServerError("common.process_issue")

        except cx_Oracle.ProgrammingError as e:
            (error,) = e.args
            message = f"Oracle-Error-Code: {error.code}. Oracle-Error-Message: {error.message} - Sql: {sql} - Oracle-ex: {e}"
            Gladsheim.error(error=e, message=message)
            raise InternalServerError("common.process_issue")

        except cx_Oracle.InternalError as e:
            (error,) = e.args
            message = f"Oracle-Error-Code: {error.code}. Oracle-Error-Message: {error.message} - Sql: {sql} - Oracle-ex: {e}"
            Gladsheim.error(error=e, message=message)
            raise InternalServerError("common.process_issue")

        except cx_Oracle.NotSupportedError as e:
            (error,) = e.args
            message = f"Oracle-Error-Code: {error.code}. Oracle-Error-Message: {error.message} - Sql: {sql} - Oracle-ex: {e}"
            Gladsheim.error(error=e, message=message)
            raise InternalServerError("common.process_issue")

        except cx_Oracle.DatabaseError as e:
            (error,) = e.args
            message = f"Oracle-Error-Code: {error.code}. Oracle-Error-Message: {error.message} - Sql: {sql} - Oracle-ex: {e}"
            Gladsheim.error(error=e, message=message)
            raise InternalServerError("common.process_issue")

        except cx_Oracle.Error as e:
            (error,) = e.args
            message = f"Oracle-Error-Code: {error.code}. Oracle-Error-Message: {error.message} - Sql: {sql} - Oracle-ex: {e}"
            Gladsheim.error(error=e, message=message)
            raise InternalServerError("common.process_issue")

        except Exception as e:
            message = f"Exception: {e}. Oracle-Error-Base-Exception Sql: {sql}"
            Gladsheim.error(error=e, message=message)
            raise InternalServerError("common.process_issue")

    @staticmethod
    def _normalize_encode(rows: List[tuple]) -> List[tuple]:
        new_rows = list()
        for row in rows:
            new_row = list()
            for item in row:
                if type(item) == str:
                    item = item.encode().decode("utf-8", "strict")
                new_row.append(item)
            new_rows.append(tuple(new_row))
        return new_rows

    @classmethod
    async def execute(cls, sql, values) -> None:
        try:
            async with cls.infra.get_connection() as cursor:
                await cursor.execute(sql, values)

        except cx_Oracle.DataError as e:
            (error,) = e.args
            message = f"Oracle-Error-Code: {error.code}. Oracle-Error-Message: {error.message} - Values: {values} - Oracle-ex: {e}"
            Gladsheim.error(error=e, message=message)
            raise InternalServerError("common.process_issue")

        except cx_Oracle.ProgrammingError as e:
            (error,) = e.args
            message = f"Oracle-Error-Code: {error.code}. Oracle-Error-Message: {error.message} - Values: {values} - Oracle-ex: {e}"
            Gladsheim.error(error=e, message=message)
            raise InternalServerError("common.process_issue")

        except cx_Oracle.InternalError as e:
            (error,) = e.args
            message = f"Oracle-Error-Code: {error.code}. Oracle-Error-Message: {error.message} - Values: {values} - Oracle-ex: {e}"
            Gladsheim.error(error=e, message=message)
            raise InternalServerError("common.process_issue")

        except cx_Oracle.NotSupportedError as e:
            (error,) = e.args
            message = f"Oracle-Error-Code: {error.code}. Oracle-Error-Message: {error.message} - Values: {values} - Oracle-ex: {e}"
            Gladsheim.error(error=e, message=message)
            raise InternalServerError("common.process_issue")

        except cx_Oracle.DatabaseError as e:
            (error,) = e.args
            message = f"Oracle-Error-Code: {error.code}. Oracle-Error-Message: {error.message} - Values: {values} - Oracle-ex: {e}"
            Gladsheim.error(error=e, message=message)
            raise InternalServerError("common.process_issue")

        except cx_Oracle.Error as e:
            (error,) = e.args
            message = f"Oracle-Error-Code: {error.code}. Oracle-Error-Message: {error.message} - Values: {values} - Oracle-ex: {e}"
            Gladsheim.error(error=e, message=message)
            raise InternalServerError("common.process_issue")
