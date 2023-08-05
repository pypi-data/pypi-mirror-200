from typing import Optional


class DetailedError(Exception):
    def __init__(self, message: str, extra: Optional[dict] = None):
        """
        Args:
            message: Error message
            extra: Details for debugging (e.g. variable values, etc)
        """
        self.message = message
        self.extra = extra

    def __str__(self):
        return f"{self.message} --- {self.extra}"


class ImprovementNeededError(DetailedError):
    pass


class ApiClientError(DetailedError):
    pass


class DuplicateValueError(DetailedError):
    pass


class DataValidationError(DetailedError):
    pass


class DataMismatchError(DetailedError):
    pass
