from __future__ import annotations

import itertools
import socket
from time import perf_counter
from typing import Any

from .models import CheckResult, classify_latency


class TcpChecker:
    def check(self, target: dict[str, Any]) -> CheckResult:
        name = str(target["name"])
        host = str(target["host"])
        port = int(target["port"])
        timeout = float(target.get("timeout", 2.0))
        started = perf_counter()

        try:
            with socket.create_connection((host, port), timeout=timeout):
                latency_ms = (perf_counter() - started) * 1000
                status = classify_latency(latency_ms, reachable=True)
                detail = "Conexao TCP estabelecida"
        except OSError as error:
            latency_ms = None
            status = classify_latency(None, reachable=False)
            detail = str(error)

        return CheckResult.create(
            name=name,
            host=host,
            port=port,
            status=status,
            latency_ms=latency_ms,
            detail=detail,
        )


class DemoChecker:
    """Deterministic checker used to demonstrate the complete workflow."""

    def __init__(self) -> None:
        self._samples = itertools.cycle((34.0, 86.0, 148.0, None))

    def check(self, target: dict[str, Any]) -> CheckResult:
        latency_ms = next(self._samples)
        reachable = latency_ms is not None
        return CheckResult.create(
            name=str(target["name"]),
            host=str(target["host"]),
            port=int(target["port"]),
            status=classify_latency(latency_ms, reachable),
            latency_ms=latency_ms,
            detail="Amostra simulada para demonstracao",
        )
