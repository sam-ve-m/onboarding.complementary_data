# Jormungandr - Onboarding
from ...domain.exceptions.exceptions import InternalServerError
from ...infrastructures.oracle.infrastrucuture import OracleInfrastructure

# Standards
from typing import List, Union

# Third Party
from etria_logger import Gladsheim
import cx_Oracle


class OracleBaseRepository:

    infra = OracleInfrastructure

    @classmethod
    async def query(cls, sql: str, filters: List[Union[str, int]]) -> list:
        try:
            async with cls.infra.get_connection() as cursor:
                await cursor.execute(sql, filters)
                rows = await cursor.fetchall()
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
