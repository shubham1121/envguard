from envguard.cli import main


def test_check_succeeds_with_valid_environment(monkeypatch, capsys):
    monkeypatch.setenv(
        "DATABASE_URL",
        "postgresql://localhost/demo",
    )
    monkeypatch.setenv("OPENAI_API_KEY", "dummy-key")
    monkeypatch.setenv("PORT", "8000")

    exit_code = main([
        "check",
        "--settings",
        "examples.demo_app.config:Settings",
    ])

    captured = capsys.readouterr()

    assert exit_code == 0
    assert "Environment validation successful." in captured.out
    assert captured.err == ""
    assert "dummy-key" not in captured.out


def test_check_fails_when_required_variables_are_missing(
    monkeypatch,
    capsys,
):
    monkeypatch.delenv("DATABASE_URL", raising=False)
    monkeypatch.delenv("OPENAI_API_KEY", raising=False)

    exit_code = main([
        "check",
        "--settings",
        "examples.demo_app.config:Settings",
    ])

    captured = capsys.readouterr()

    assert exit_code == 1
    assert "Environment validation failed" in captured.err
    assert "DATABASE_URL" in captured.err
    assert "OPENAI_API_KEY" in captured.err


def test_check_returns_two_for_invalid_settings_path(capsys):
    exit_code = main([
        "check",
        "--settings",
        "invalid-settings-path",
    ])

    captured = capsys.readouterr()

    assert exit_code == 2
    assert "Invalid settings path" in captured.err