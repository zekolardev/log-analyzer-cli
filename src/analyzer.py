from collections import Counter
from typing import Iterable

from src.parser import LogEntry, parse_line


def analyze_lines(lines: Iterable[str]) -> dict:
    entries = []
    level_counts = Counter()
    error_messages = Counter()

    for line in lines:
        entry = parse_line(line)

        if entry is None:
            continue

        entries.append(entry)
        level_counts[entry.level] += 1

        if entry.level in ("ERROR", "CRITICAL"):
            error_messages[entry.message] += 1

    return {
        "total_lines": len(entries),
        "levels": dict(sorted(level_counts.items())),
        "errors": level_counts["ERROR"],
        "critical": level_counts["CRITICAL"],
        "warnings": level_counts["WARN"],
        "top_errors": [
            {
                "message": message,
                "count": count
            }
            for message, count in error_messages.most_common(5)
        ],
        "entries": [
            {
                "timestamp": entry.timestamp,
                "level": entry.level,
                "message": entry.message
            }
            for entry in entries
        ]
    }


def analyze_file(file_path: str) -> dict:
    with open(file_path, "r", encoding="utf-8", errors="replace") as file:
        return analyze_lines(file)