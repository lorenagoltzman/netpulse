from __future__ import annotations

import argparse
import json
from pathlib import Path

from src.netpulse.checker import DemoChecker, TcpChecker
from src.netpulse.report import build_dashboard
from src.netpulse.storage import append_results, load_results


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Verifica serviços TCP e gera um painel de disponibilidade."
    )
    parser.add_argument("--config", default="hosts.example.json")
    parser.add_argument("--output", default="data/checks.csv")
    parser.add_argument("--report", default="dashboard.html")
    parser.add_argument("--demo", action="store_true", help="Usa resultados simulados.")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    config_path = Path(args.config)
    hosts = json.loads(config_path.read_text(encoding="utf-8"))
    checker = DemoChecker() if args.demo else TcpChecker()

    results = [checker.check(item) for item in hosts]
    append_results(Path(args.output), results)
    history = load_results(Path(args.output))
    build_dashboard(history, Path(args.report))

    for result in results:
        latency = f"{result.latency_ms:.1f} ms" if result.latency_ms is not None else "-"
        print(f"{result.name:<20} {result.status:<8} {latency}")
    print(f"\nPainel gerado em {Path(args.report).resolve()}")


if __name__ == "__main__":
    main()
