import re
from dataclasses import dataclass
from datetime import datetime
from typing import Optional


@dataclass
class LogEntry:
    timestamp: Optional[str]
    level: str
    message: str
    raw: str


TIMESTAMP_PATTERN = re.compile(
    r"\d{4}-\d{2}-\d{2}[ T]\d{2}:\d{2}:\d{2}"
)

LEVEL_PATTERN = re.compile(
    r"\b(DEBUG|INFO|WARN|WARNING|ERROR|CRITICAL|FATAL)\b",
    re.IGNORECASE
)

LEVEL_ALIASES = {
    "WARNING": "WARN",
    "FATAL": "CRITICAL",
}


def parse_line(line: str) -> Optional[LogEntry]:
    raw = line.rstrip("\n")
    stripped = raw.strip()

    if not stripped:
        return None

    timestamp_match = TIMESTAMP_PATTERN.search(stripped)
    timestamp = None

    if timestamp_match:
        timestamp = timestamp_match.group()

        try:
            datetime.fromisoformat(timestamp)
        except ValueError:
            timestamp = None

    level_match = LEVEL_PATTERN.search(stripped)

    if level_match:
        level = level_match.group().upper()
        level = LEVEL_ALIASES.get(level, level)
        message = stripped[level_match.end():].strip()
        message = message.lstrip(":|-[] ")
    else:
        level = "UNKNOWN"
        message = stripped

    return LogEntry(
        timestamp=timestamp,
        level=level,
        message=message,
        raw=raw
    )