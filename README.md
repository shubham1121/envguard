
# EnvGuard

**Validate application environment configuration before startup.**

EnvGuard is a lightweight Python package and CLI tool that validates environment variables against a Pydantic model.

It helps developers detect missing or invalid configuration before their applications start.

## Features

- Validate environment variables using Pydantic models.
- Support required and optional configuration fields.
- Validate data types and constraints.
- Provide safe, readable validation reports.
- Avoid exposing rejected input values in validation errors.
- Use EnvGuard as a Python library or command-line tool.
- Return meaningful exit codes for automation and CI pipelines.

## Requirements

- Python 3.10 or later
- Pydantic 2.x

## Installation

Clone the repository and navigate into the project directory.

Install EnvGuard in editable mode:

```bash
python -m pip install -e .
```

To install the development dependencies:

```bash
python -m pip install -e ".[dev]"
```

## Quick Start

### 1. Define your settings model

```python
from pydantic import BaseModel, Field, SecretStr

class Settings(BaseModel):
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
```

### 2. Set environment variables

```bash
export DATABASE_URL="postgresql://localhost/demo"
export OPENAI_API_KEY="your-api-key"
export PORT=8000
```

### 3. Validate your configuration

```python
from envguard import validate_environment

settings = validate_environment(Settings)

print("Configuration validated successfully.")
```

EnvGuard returns a validated Pydantic model instance when validation succeeds.

## Command-Line Usage

EnvGuard provides a `check` command.

```bash
envguard check --settings module.path:ClassName
```

Example using the included demo settings model:

```bash
PYTHONPATH=. envguard check \
  --settings examples.demo_app.config:Settings
```

The settings argument follows this format:

`module.path:ClassName`

The specified module must be importable by Python.

## Python API

EnvGuard exposes the following public functions and exception:

| Name | Purpose |
|---|---|
| `validate_environment()` | Validate environment variables against a Pydantic model |
| `format_validation_report()` | Format validation issues into a readable report |
| `EnvironmentValidationError` | Exception raised when configuration validation fails |

Example error handling:

```python
from envguard import (
    EnvironmentValidationError,
    format_validation_report,
    validate_environment,
)

try:
    settings = validate_environment(Settings)

except EnvironmentValidationError as exc:
    report = format_validation_report(exc.issues)
    print(report)
```

## Exit Codes

| Exit code | Meaning |
|---|---|
| `0` | Configuration validation successful |
| `1` | Environment validation failed |
| `2` | Invalid CLI usage, settings path, or settings model |

## Security

EnvGuard avoids including rejected input values, validation context, or Pydantic documentation URLs in its validation issues.

For sensitive configuration fields, use Pydantic's `SecretStr` type.

EnvGuard reads from the process environment. It does not load `.env` files automatically.

## Development

Run the test suite:

```bash
python -m pytest -v
```

Run linting:

```bash
ruff check src tests
```

## Project Structure

```text
envguard/
├── examples/
│   └── demo_app/
├── src/
│   └── envguard/
│       ├── __init__.py
│       ├── cli.py
│       ├── exceptions.py
│       ├── reporting.py
│       └── validator.py
├── tests/
├── pyproject.toml
└── README.md
```

## License

## License

EnvGuard is licensed under the MIT License.
See the [LICENSE](LICENSE) file for details.
