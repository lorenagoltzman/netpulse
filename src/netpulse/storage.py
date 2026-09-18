from __future__ import annotations

import csv
from dataclasses import asdict
from pathlib import Path
from typing import Iterable

from .models import CheckResult


FIELDS = ["name", "host", "port", "status", "latency_ms", "checked_at", "detail"]


def append_results(path: Path, results: Iterable[CheckResult]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    has_content = path.exists() and path.stat().st_size > 0
    with path.open("a", newline="", encoding="utf-8") as stream:
        writer = csv.DictWriter(stream, fieldnames=FIELDS)
        if not has_content:
            writer.writeheader()
        for result in results:
            writer.writerow(asdict(result))


def load_results(path: Path) -> list[CheckResult]:
    if not path.exists():
        return []
    items: list[CheckResult] = []
    with path.open(newline="", encoding="utf-8") as stream:
        for row in csv.DictReader(stream):
            raw_latency = row["latency_ms"]
            items.append(
                CheckResult(
                    name=row["name"],
                    host=row["host"],
                    port=int(row["port"]),
                    status=row["status"],
                    latency_ms=float(raw_latency) if raw_latency else None,
                    checked_at=row["checked_at"],
                    detail=row["detail"],
                )
            )
    return items
