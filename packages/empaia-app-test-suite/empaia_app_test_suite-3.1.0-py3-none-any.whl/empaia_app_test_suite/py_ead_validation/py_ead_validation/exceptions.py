class EadValidationError(Exception):
    pass


class EadSchemaMissingError(EadValidationError):
    pass


class EadSchemaNotAvailableError(EadValidationError):
    pass


class EadSchemaValidationError(EadValidationError):
    pass


class EadContentValidationError(EadValidationError):
    pass


class ConfigValidationError(Exception):
    pass


class JobValidationPreconditionError(Exception):
    pass


class JobValidationError(Exception):
    pass
