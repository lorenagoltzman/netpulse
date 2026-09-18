from __future__ import annotations

from collections import defaultdict
from html import escape
from pathlib import Path
from statistics import mean

from .models import CheckResult


def summarize(results: list[CheckResult]) -> list[dict[str, object]]:
    grouped: dict[str, list[CheckResult]] = defaultdict(list)
    for result in results:
        grouped[result.name].append(result)

    summaries: list[dict[str, object]] = []
    for name, samples in grouped.items():
        online = [item for item in samples if item.status != "OFFLINE"]
        latencies = [item.latency_ms for item in online if item.latency_ms is not None]
        last = samples[-1]
        summaries.append(
            {
                "name": name,
                "endpoint": f"{last.host}:{last.port}",
                "status": last.status,
                "availability": round(len(online) / len(samples) * 100, 1),
                "average_latency": round(mean(latencies), 1) if latencies else None,
                "samples": len(samples),
            }
        )
    return summaries


def build_dashboard(results: list[CheckResult], output: Path) -> None:
    items = summarize(results)
    available = sum(1 for item in items if item["status"] != "OFFLINE")
    availability = round(available / len(items) * 100, 1) if items else 0
    latencies = [float(item["average_latency"]) for item in items if item["average_latency"] is not None]
    avg_latency = round(mean(latencies), 1) if latencies else 0
    incidents = sum(1 for result in results if result.status in {"OFFLINE", "CRITICO"})

    rows = "".join(
        f"""
        <tr>
          <td><strong>{escape(str(item['name']))}</strong><span>{escape(str(item['endpoint']))}</span></td>
          <td><span class="status {str(item['status']).lower()}">{item['status']}</span></td>
          <td>{item['availability']}%</td>
          <td>{item['average_latency'] if item['average_latency'] is not None else '-'} ms</td>
          <td>{item['samples']}</td>
        </tr>"""
        for item in items
    )

    html = f"""<!doctype html>
<html lang="pt-BR">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>NetPulse Dashboard</title>
  <style>
    :root {{ --bg:#07111f; --panel:#101d2e; --line:#24364d; --text:#eaf2ff; --muted:#90a4bf; --cyan:#38bdf8; --green:#34d399; --yellow:#fbbf24; --red:#fb7185; }}
    * {{ box-sizing:border-box; }}
    body {{ margin:0; font-family:Inter,Segoe UI,sans-serif; background:radial-gradient(circle at top right,#12304d 0,var(--bg) 38%); color:var(--text); min-height:100vh; }}
    main {{ width:min(1100px,92%); margin:0 auto; padding:54px 0; }}
    header {{ display:flex; align-items:end; justify-content:space-between; gap:24px; margin-bottom:28px; }}
    h1 {{ margin:0; font-size:clamp(2rem,5vw,3.3rem); letter-spacing:-.05em; }}
    header p, td span {{ color:var(--muted); }}
    .accent {{ color:var(--cyan); }}
    .cards {{ display:grid; grid-template-columns:repeat(3,1fr); gap:16px; margin-bottom:24px; }}
    .card,.table-wrap {{ background:rgba(16,29,46,.88); border:1px solid var(--line); border-radius:18px; box-shadow:0 18px 55px rgba(0,0,0,.2); }}
    .card {{ padding:22px; }} .label {{ color:var(--muted); font-size:.8rem; text-transform:uppercase; letter-spacing:.12em; }}
    .value {{ display:block; margin-top:8px; font-size:2rem; font-weight:750; }}
    .table-wrap {{ overflow:auto; }} table {{ width:100%; border-collapse:collapse; }}
    th,td {{ padding:18px 20px; text-align:left; border-bottom:1px solid var(--line); white-space:nowrap; }} th {{ color:var(--muted); font-size:.78rem; text-transform:uppercase; letter-spacing:.08em; }}
    td:first-child span {{ display:block; margin-top:4px; font-size:.82rem; }} tr:last-child td {{ border-bottom:0; }}
    .status {{ display:inline-block; padding:6px 10px; border-radius:999px; font-size:.75rem; font-weight:800; }}
    .online {{ color:var(--green); background:#34d39918; }} .atencao {{ color:var(--yellow); background:#fbbf2418; }} .critico,.offline {{ color:var(--red); background:#fb718518; }}
    footer {{ color:var(--muted); margin-top:18px; font-size:.82rem; }}
    @media (max-width:720px) {{ header {{ align-items:start; flex-direction:column; }} .cards {{ grid-template-columns:1fr; }} }}
  </style>
</head>
<body>
<main>
  <header><div><div class="label">Monitoramento de rede</div><h1>Net<span class="accent">Pulse</span></h1></div><p>Visao consolidada dos endpoints configurados</p></header>
  <section class="cards">
    <article class="card"><span class="label">Endpoints disponiveis</span><span class="value">{availability}%</span></article>
    <article class="card"><span class="label">Latencia media</span><span class="value">{avg_latency} ms</span></article>
    <article class="card"><span class="label">Incidentes registrados</span><span class="value">{incidents}</span></article>
  </section>
  <section class="table-wrap"><table><thead><tr><th>Servico</th><th>Status</th><th>Disponibilidade</th><th>Latencia media</th><th>Amostras</th></tr></thead><tbody>{rows}</tbody></table></section>
  <footer>Gerado pelo NetPulse. Horarios registrados em UTC.</footer>
</main>
</body>
</html>"""
    output.write_text(html, encoding="utf-8")
