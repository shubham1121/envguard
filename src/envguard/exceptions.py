class EnvironmentValidationError(Exception):
    """Raised when environment configuration is invalid."""

    def __init__(self, issues: list[dict[str, str]]) -> None:
        self.issues = issues

        super().__init__("Environment validation failed")