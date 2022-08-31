# Standards
from re import sub
from typing import Optional

# Third party
from pydantic import BaseModel, validator, constr


class Spouse(BaseModel):
    name: constr(min_length=1, max_length=100)
    nationality: int
    cpf: str

    @validator("cpf", always=True, allow_reuse=True)
    def format_cpf(cls, cpf: str):
        cpf = sub("[^0-9]", "", cpf)
        return cpf

    @validator("cpf", always=True, allow_reuse=True)
    def validate_cpf(cls, cpf: str):
        cpf_last_digits = cpf[:-2]
        reversed_count = 10
        total = 0

        for index in range(19):
            if index > 8:
                index -= 9
            total += int(cpf_last_digits[index]) * reversed_count
            reversed_count -= 1

            if reversed_count < 2:
                reversed_count = 11
                digits = 11 - (total % 11)

                if digits > 9:
                    digits = 0
                total = 0
                cpf_last_digits += str(digits)

        sequence = cpf_last_digits == str(cpf_last_digits[0]) * len(cpf)
        if not cpf == cpf_last_digits or sequence:
            raise ValueError("invalid cpf")
        return cpf


class TaxResidence(BaseModel):
    country: constr(min_length=3, max_length=3)
    tax_number: str


class ComplementaryData(BaseModel):
    marital_status: int
    spouse: Optional[Spouse]
