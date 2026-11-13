
import pytest
from pydantic import BaseModel, ConfigDict, Field, SecretStr

from envguard.exceptions import EnvironmentValidationError
from envguard.validator import validate_environment


class DemoSettings(BaseModel):
    model_config = ConfigDict(extra="ignore")

    database_url: SecretStr = Field(
        validation_alias="DATABASE_URL"
    )

    openai_api_key: SecretStr = Field(
        validation_alias="OPENAI_API_KEY"
    )

    port: int = Field(
        default=8000,
        validation_alias="PORT",
        ge=1,
        le=65535,
    )


def test_valid_environment_returns_settings():
    environment = {
        "DATABASE_URL": "postgresql://localhost/demo",
        "OPENAI_API_KEY": "dummy-secret",
        "PORT": "9000",
    }

    settings = validate_environment(
        DemoSettings,
        environ=environment,
    )

    assert isinstance(settings, DemoSettings)
    assert settings.port == 9000


def test_missing_required_variable_raises_error():
    environment = {
        "DATABASE_URL": "postgresql://localhost/demo",
    }

    with pytest.raises(EnvironmentValidationError) as exc_info:
        validate_environment(
            DemoSettings,
            environ=environment,
        )

    assert any(
        issue["type"] == "missing"
        for issue in exc_info.value.issues
    )


def test_invalid_port_raises_error():
    environment = {
        "DATABASE_URL": "postgresql://localhost/demo",
        "OPENAI_API_KEY": "dummy-secret",
        "PORT": "hello",
    }

    with pytest.raises(EnvironmentValidationError) as exc_info:
        validate_environment(
            DemoSettings,
            environ=environment,
        )

    assert any(
        issue["loc"] == "PORT"
        for issue in exc_info.value.issues
    )


def test_default_port_is_used():
    environment = {
        "DATABASE_URL": "postgresql://localhost/demo",
        "OPENAI_API_KEY": "dummy-secret",
    }

    settings = validate_environment(
        DemoSettings,
        environ=environment,
    )

    assert settings.port == 8000


def test_secret_is_not_exposed_in_error():
    secret = "super-secret-api-key"

    environment = {
        "DATABASE_URL": "postgresql://localhost/demo",
        "OPENAI_API_KEY": secret,
        "PORT": "invalid",
    }

    with pytest.raises(EnvironmentValidationError) as exc_info:
        validate_environment(
            DemoSettings,
            environ=environment,
        )

    assert secret not in str(exc_info.value)
    assert secret not in repr(exc_info.value.issues)

def test_validation_errors_do_not_expose_input_values():
    import pytest
    from pydantic import BaseModel

    from envguard import (
        EnvironmentValidationError,
        format_validation_report,
        validate_environment,
    )

    class Settings(BaseModel):
        port: int

    private_value = "DO_NOT_EXPOSE_THIS_12345"

    with pytest.raises(EnvironmentValidationError) as exc_info:
        validate_environment(
            Settings,
            environ={"port": private_value},
        )

    report = format_validation_report(exc_info.value.issues)

    assert private_value not in report
    assert "Invalid configuration value." in report