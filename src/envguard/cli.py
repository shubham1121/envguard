
import argparse
import sys
from collections.abc import Sequence
from importlib import import_module

from pydantic import BaseModel

from envguard.exceptions import EnvironmentValidationError
from envguard.reporting import format_validation_report
from envguard.validator import validate_environment


def load_settings_model(settings_path: str) -> type[BaseModel]:
    """
    Dynamically load a Pydantic settings model.

    Expected format: module.path:ClassName
    """

    module_path, separator, class_name = settings_path.partition(":")

    if not separator or not module_path or not class_name:
        raise ValueError(
            "Invalid settings path. Expected module.path:ClassName"
        )

    module = import_module(module_path)

    settings_model = getattr(module, class_name)

    if (
        not isinstance(settings_model, type)
        or not issubclass(settings_model, BaseModel)
    ):
        raise TypeError(
            "The specified settings object must be a Pydantic BaseModel."
        )

    return settings_model


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="envguard",
        description="Validate application environment configuration.",
    )

    subparsers = parser.add_subparsers(
        dest="command",
        required=True,
    )

    check_parser = subparsers.add_parser(
        "check",
        help="Validate environment configuration.",
    )

    check_parser.add_argument(
        "--settings",
        required=True,
        help="Settings model in module.path:ClassName format.",
    )

    return parser

def main(argv: Sequence[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)

    if args.command == "check":
        try:
            settings_model = load_settings_model(args.settings)
            validate_environment(settings_model)
            report = format_validation_report([])
            print(report)
            return 0
        except EnvironmentValidationError as e:
            report = format_validation_report(e.issues)
            print(report, file=sys.stderr)
            return 1
        except (ValueError, TypeError, ImportError, AttributeError) as e:
            print(f"Error: {e}", file=sys.stderr)
            return 2

    return 2
