import argparse
import json
import sys
from pathlib import Path

from src.analyzer import analyze_file


def format_report(report: dict) -> str:
    lines = [
        "=" * 45,
        "LOG ANALYZER REPORT",
        "=" * 45,
        f"Total entries : {report['total_lines']}",
        f"Errors        : {report['errors']}",
        f"Critical      : {report['critical']}",
        f"Warnings      : {report['warnings']}",
        "",
        "LOG LEVELS",
        "-" * 45,
    ]

    for level, count in report["levels"].items():
        lines.append(f"{level:<15} {count}")

    lines.extend([
        "",
        "TOP ERRORS",
        "-" * 45,
    ])

    if report["top_errors"]:
        for item in report["top_errors"]:
            lines.append(
                f"[{item['count']}] {item['message']}"
            )
    else:
        lines.append("No errors found.")

    lines.append("=" * 45)

    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(
        prog="log-analyzer",
        description="Analyze log files and generate structured reports."
    )

    parser.add_argument(
        "file",
        help="Path to the log file"
    )

    parser.add_argument(
        "--json",
        action="store_true",
        help="Display report in JSON format"
    )

    parser.add_argument(
        "--output",
        "-o",
        help="Save report to a file"
    )

    args = parser.parse_args()

    file_path = Path(args.file)

    if not file_path.exists():
        print(f"Error: File not found: {file_path}", file=sys.stderr)
        sys.exit(1)

    if not file_path.is_file():
        print(f"Error: Not a file: {file_path}", file=sys.stderr)
        sys.exit(1)

    try:
        report = analyze_file(str(file_path))

        output = (
            json.dumps(report, indent=4, ensure_ascii=False)
            if args.json
            else format_report(report)
        )

        print(output)

        if args.output:
            Path(args.output).write_text(
                output + "\n",
                encoding="utf-8"
            )
            print(f"\nReport saved to: {args.output}")

    except (OSError, UnicodeError) as error:
        print(f"Error: {error}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()