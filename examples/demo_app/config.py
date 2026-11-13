
from pydantic import BaseModel, ConfigDict, Field, SecretStr


class Settings(BaseModel):
    # Ignore environment variables that this application
    # does not explicitly define.
    model_config = ConfigDict(extra="ignore")

    # Required database connection string.
    database_url: SecretStr = Field(
        validation_alias="DATABASE_URL"
    )

    # Required API key. Treat it as sensitive information.
    openai_api_key: SecretStr = Field(
        validation_alias="OPENAI_API_KEY"
    )

    # Optional port with a default value and valid range.
    port: int = Field(
        default=8000,
        validation_alias="PORT",
        ge=1,
        le=65535
    )
