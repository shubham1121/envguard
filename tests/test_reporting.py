from envguard.reporting import format_validation_report


def test_format_validation_errors():
    issues = [
        {
            "loc": "OPENAI_API_KEY",
            "msg": "Required configuration is missing.",
            "type": "missing",
        },
        {
            "loc": "PORT",
            "msg": "Invalid configuration value.",
            "type": "int_parsing",
        },
    ]

    report = format_validation_report(issues)

    assert "OPENAI_API_KEY" in report
    assert "PORT" in report
    assert "2 configuration errors found." in report

def test_format_validation_errors_empty():
    issues = []

    report = format_validation_report(issues)

    assert "Environment validation successful." in report
    assert "No configuration errors found." in report

def test_format_validation_errors_single_issue():
    issues = [
        {
            "loc": "DATABASE_URL",
            "msg": "Required configuration is missing.",
            "type": "missing",
        }
    ]

    report = format_validation_report(issues)

    assert "DATABASE_URL" in report
    assert "1 configuration error found." in report