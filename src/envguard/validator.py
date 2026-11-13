
import os
from collections.abc import Mapping
from typing import TypeVar

from pydantic import BaseModel, ValidationError

from envguard.exceptions import EnvironmentValidationError

SettingsT = TypeVar("SettingsT", bound=BaseModel)


def validate_environment(
    settings_model: type[SettingsT],
    environ: Mapping[str, str] | None = None,
) -> SettingsT:
    """
    Validate environment variables against a Pydantic model.

    Return the validated settings instance when successful.
    """

    # 1. Select the environment source.
    # Use os.environ when no custom mapping is provided.
    if environ is None:
        environ = os.environ

    # 2. Validate the selected mapping using model_validate().

    try:
        validated_settings = settings_model.model_validate(dict(environ))
        return validated_settings
    # 3. Catch Pydantic ValidationError.

    except ValidationError as exc:

        # Convert Pydantic errors into safe, generic messages.
        issues = []

        for error in exc.errors(
            include_input=False,
            include_context=False,
            include_url=False,
        ):
            location = ".".join(str(part) for part in error["loc"])

            message = (
                "Required configuration is missing."
                if error["type"] == "missing"
                else "Invalid configuration value."
            )

            issues.append(
                {
                    "loc": location,
                    "msg": message,
                    "type": error["type"],
                }
            )

        raise EnvironmentValidationError(issues) from None