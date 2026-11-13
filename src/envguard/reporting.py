
from collections.abc import Mapping, Sequence


def format_validation_report(
    issues: Sequence[Mapping[str, str]],
) -> str:
    """
    Format sanitized validation issues into a readable report.
    """

    # 1. Create a list containing the report heading.
    if not issues:
        lines = ["Environment validation successful."]
    else:
        lines = ["Environment validation failed with the following issues:"]

    # 2. Iterate over the issues.
    for issue in issues:
        location = issue["loc"]
        message = issue["msg"]
        lines.append(f"  - {location}: {message}")
    # 5. Add the total number of errors.
    if len(issues) == 0:
        lines.append("No configuration errors found.")
    elif len(issues) == 1:
        lines.append(f"{len(issues)} configuration error found.")
    else:
        lines.append(f"{len(issues)} configuration errors found.")

    # 6. Join all lines and return the final string.
    return "\n".join(lines)
