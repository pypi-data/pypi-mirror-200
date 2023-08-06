class DataValidationError(Exception):
    """Raised on error in any of the data validation methods."""

    def __init__(self, message: str):
        super().__init__(message)


class IndexConfigurationError(Exception):
    """Raised on error in any of the index configuration methods."""

    def __init__(self, message: str):
        super().__init__(message)


class IndexCalculationError(Exception):
    """Raised on error in any of the index calculation methods."""

    def __init__(self, message: str):
        super().__init__(message)

