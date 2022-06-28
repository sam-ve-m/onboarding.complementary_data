class ComplementaryDataModel:
    def __init__(self, complementary_data_validated):
        self.spouse = complementary_data_validated.get("spouse", None)
        self.foreign_account_tax = complementary_data_validated.get("foreign_account_tax", None)
        self.marital_status = complementary_data_validated.get("marital_status", None)


    @validator("marital_status", always=True, allow_reuse=True)
    def validate_value(cls, marital_status):
        sinacor_types_repository = SinacorTypesRepository()

        if sinacor_types_repository.validate_marital_regime(value=marital_status):
            return marital_status
        raise ValueError("marital not exists")


    @validator("country", always=True, allow_reuse=True)
    def validate_country(cls, e):
        sinacor_types_repository = "SinacorTypesRepository()"
        if sinacor_types_repository.validate_country(value=e):
            return e
        raise ValueError("country not exists")


    @validator("nationality", always=True, allow_reuse=True)
    def validate_value(cls, e):
        sinacor_types_repository = "SinacorTypesRepository()"
        if sinacor_types_repository.validate_nationality(value=e):
            return e
        raise ValueError("Nationality not exists")
