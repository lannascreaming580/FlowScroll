import re


def collect_invalid_regex_lines(raw_text: str) -> list[tuple[int, str]]:
    """Return invalid regex rules with their original 1-based line numbers."""
    invalid_rules: list[tuple[int, str]] = []
    for line_no, raw_line in enumerate(raw_text.splitlines(), start=1):
        pattern = raw_line.strip()
        if not pattern:
            continue
        try:
            re.compile(pattern)
        except re.error:
            invalid_rules.append((line_no, pattern))
    return invalid_rules
