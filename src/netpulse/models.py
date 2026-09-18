from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timezone


@dataclass(frozen=True)
class CheckResult:
    name: str
    host: str
    port: int
    status: str
    latency_ms: float | None
    checked_at: str
    detail: str = ""

    @classmethod
    def create(
        cls,
        *,
        name: str,
        host: str,
        port: int,
        status: str,
        latency_ms: float | None,
        detail: str = "",
    ) -> "CheckResult":
        return cls(
            name=name,
            host=host,
            port=port,
            status=status,
            latency_ms=latency_ms,
            checked_at=datetime.now(timezone.utc).isoformat(timespec="seconds"),
            detail=detail,
        )


def classify_latency(latency_ms: float | None, reachable: bool) -> str:
    if not reachable or latency_ms is None:
        return "OFFLINE"
    if latency_ms >= 250:
        return "CRITICO"
    if latency_ms >= 120:
        return "ATENCAO"
    return "ONLINE"
