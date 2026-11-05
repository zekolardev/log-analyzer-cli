import json
import subprocess
import sys
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]


def run_cli(*args):
    return subprocess.run(
        [
            sys.executable,
            "-m",
            "src.cli",
            *map(str, args)
        ],
        capture_output=True,
        text=True,
        cwd=PROJECT_ROOT
    )


def create_log_file(tmp_path):
    log_file = tmp_path / "sample.log"

    log_file.write_text(
        "INFO: Application started\n"
        "ERROR: Database connection failed\n"
        "WARNING: High memory usage\n",
        encoding="utf-8"
    )

    return log_file


def test_cli_text_output(tmp_path):
    log_file = create_log_file(tmp_path)

    result = run_cli(log_file)

    assert result.returncode == 0
    assert "LOG ANALYZER REPORT" in result.stdout
    assert "Total entries : 3" in result.stdout


def test_cli_json_output(tmp_path):
    log_file = create_log_file(tmp_path)

    result = run_cli(log_file, "--json")

    assert result.returncode == 0

    report = json.loads(result.stdout)

    assert report["total_lines"] == 3
    assert report["errors"] == 1
    assert report["warnings"] == 1


def test_cli_output_file(tmp_path):
    log_file = create_log_file(tmp_path)
    output_file = tmp_path / "report.txt"

    result = run_cli(log_file, "--output", output_file)

    assert result.returncode == 0
    assert output_file.exists()
    assert "LOG ANALYZER REPORT" in output_file.read_text(
        encoding="utf-8"
    )


def test_cli_missing_file():
    result = run_cli("nonexistent.log")

    assert result.returncode == 1
    assert "File not found" in result.stderr


def test_cli_directory_instead_of_file(tmp_path):
    result = run_cli(tmp_path)

    assert result.returncode == 1
    assert "Not a file" in result.stderr


def test_cli_help():
    result = run_cli("--help")

    assert result.returncode == 0
    assert "--json" in result.stdout
    assert "--output" in result.stdout