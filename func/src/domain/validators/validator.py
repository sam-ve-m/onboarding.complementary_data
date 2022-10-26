# Standards
from re import sub
from typing import Optional

# Third party
from pydantic import BaseModel, validator, constr


char_with_space = "[a-zA-Z\sáéíóúãẽĩõũâêîôûÁÉÍÓÚÃẼĨÕŨÂÊÎÔÛç]"
char_without_space = "[a-zA-ZáéíóúãẽĩõũâêîôûÁÉÍÓÚÃẼĨÕŨÂÊÎÔÛç]"
name_regex = rf"^{char_without_space}+\s{char_without_space}{char_with_space}*$"


class Spouse(BaseModel):
    name: Optional[constr(regex=name_regex, max_length=60)]
    nationality: int
    cpf: str

    @validator("cpf")
    def format_cpf(cls, cpf: str):
        cpf = sub("[^0-9]", "", cpf)
        return cpf

    @validator("cpf")
    def validate_cpf(cls, cpf: str) -> str:
        if len(cpf) != 11:
            raise ValueError("invalid cpf")

        first_digit_validation = sum(
            int(cpf[index]) * (10 - index) for index in range(9)
        )
        mod_first_digit = first_digit_validation % 11
        first_digit = 11 - mod_first_digit if mod_first_digit > 1 else 0
        if str(first_digit) != cpf[-2]:
            raise ValueError("invalid cpf")

        second_digit_validation = (
            first_digit_validation + sum(map(int, cpf[:9])) + 2 * first_digit
        )
        mod_second_digit = second_digit_validation % 11
        second_digit = 11 - mod_second_digit if mod_second_digit > 1 else 0
        if str(second_digit) != cpf[-1]:
            raise ValueError(f"invalid cpf")
        return cpf


class TaxResidence(BaseModel):
    country: constr(min_length=3, max_length=3)
    tax_number: str


class ComplementaryData(BaseModel):
    marital_status: int
    spouse: Optional[Spouse]
