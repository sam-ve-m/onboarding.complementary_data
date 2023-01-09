import pytest

from func.src.domain.validators.validator import Spouse


def test_when_cpf_valid_then_proceed():
    cpf_validated = Spouse.validate_cpf("44820841823")
    assert cpf_validated == "44820841823"


def test_when_cpf_invalid_then_raises():
    with pytest.raises(ValueError):
        Spouse.validate_cpf("44820841822")


def test_when_cpf_first_invalid_then_raises():
    with pytest.raises(ValueError):
        Spouse.validate_cpf("44820841833")


def test_when_cpf_10_digits_then_raises():
    with pytest.raises(ValueError):
        Spouse.validate_cpf("4482074182")


def test_when_cpf_9_digits_then_raises():
    with pytest.raises(ValueError):
        Spouse.validate_cpf("448207418")


def test_when_cpf_12_digits_then_raises():
    with pytest.raises(ValueError):
        Spouse.validate_cpf("44820741")


def test_when_cpf_13_digits_then_raises():
    with pytest.raises(ValueError):
        Spouse.validate_cpf("4482074")
