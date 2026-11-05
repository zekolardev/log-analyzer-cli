from src.parser import parse_line


def test_parse_valid_log():
    line = "2026-11-05 10:30:00 ERROR Database connection failed"

    entry = parse_line(line)

    assert entry.timestamp == "2026-11-05 10:30:00"
    assert entry.level == "ERROR"
    assert entry.message == "Database connection failed"


def test_parse_info_log():
    entry = parse_line("INFO: Application started")

    assert entry.level == "INFO"
    assert entry.message == "Application started"


def test_parse_warning_alias():
    entry = parse_line("WARNING: High memory usage")

    assert entry.level == "WARN"


def test_parse_fatal_alias():
    entry = parse_line("FATAL: System failure")

    assert entry.level == "CRITICAL"


def test_parse_unknown_level():
    entry = parse_line("Application initialized")

    assert entry.level == "UNKNOWN"
    assert entry.message == "Application initialized"


def test_parse_empty_line():
    assert parse_line("") is None
    assert parse_line("   ") is None


def test_parse_invalid_timestamp():
    entry = parse_line(
        "2026-99-99 25:61:61 ERROR Invalid timestamp"
    )

    assert entry.timestamp is None
    assert entry.level == "ERROR"


def test_parse_preserves_raw_line():
    line = "INFO: Test message"

    entry = parse_line(line)

    assert entry.raw == line