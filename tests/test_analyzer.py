from src.analyzer import analyze_lines


def test_analyze_total_lines():
    lines = [
        "INFO: Application started",
        "ERROR: Connection failed",
        "WARNING: High memory usage",
    ]

    report = analyze_lines(lines)

    assert report["total_lines"] == 3


def test_analyze_log_levels():
    lines = [
        "INFO: Started",
        "INFO: Running",
        "ERROR: Failed",
        "WARNING: Memory warning",
    ]

    report = analyze_lines(lines)

    assert report["levels"]["INFO"] == 2
    assert report["levels"]["ERROR"] == 1
    assert report["levels"]["WARN"] == 1


def test_analyze_error_counts():
    lines = [
        "ERROR: Database failed",
        "ERROR: Database failed",
        "CRITICAL: System crashed",
    ]

    report = analyze_lines(lines)

    assert report["errors"] == 2
    assert report["critical"] == 1


def test_analyze_top_errors():
    lines = [
        "ERROR: Connection failed",
        "ERROR: Connection failed",
        "ERROR: File missing",
        "CRITICAL: System crashed",
    ]

    report = analyze_lines(lines)

    assert report["top_errors"][0] == {
        "message": "Connection failed",
        "count": 2
    }


def test_analyze_empty_input():
    report = analyze_lines([])

    assert report["total_lines"] == 0
    assert report["errors"] == 0
    assert report["critical"] == 0
    assert report["top_errors"] == []


def test_analyze_ignores_empty_lines():
    lines = [
        "INFO: Started",
        "",
        "   ",
        "ERROR: Failed",
    ]

    report = analyze_lines(lines)

    assert report["total_lines"] == 2


def test_analyze_unknown_entries():
    report = analyze_lines([
        "Application initialized"
    ])

    assert report["levels"]["UNKNOWN"] == 1


def test_analyze_top_errors_limit():
    lines = [
        f"ERROR: Error number {number}"
        for number in range(10)
    ]

    report = analyze_lines(lines)

    assert len(report["top_errors"]) == 5