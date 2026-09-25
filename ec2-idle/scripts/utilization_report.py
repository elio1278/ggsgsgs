"""Code Mode helper (runs in the TrueForge sandbox): one line of utilization per instance.

    python /opt/tfy/skills/ec2-idle/scripts/utilization_report.py [--server undertaker-aws] i-0abc i-0def ...

Calls the read-only get_metrics tool through the harness bridge (no credentials in the sandbox) and prints a
compact summary, so raw metric series never enter the chat.
"""

import argparse
import asyncio

from mcp_client import call_tool


async def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--server", default="undertaker-aws")
    ap.add_argument("--hours", type=int, default=336)
    ap.add_argument("ids", nargs="+")
    a = ap.parse_args()
    res = await call_tool(a.server, "get_metrics", body={"resource_ids": a.ids, "lookback_hours": a.hours})
    for rid, u in sorted((res.get("utilization") or {}).items()):
        m = u.get("metrics", {})
        cpu = m.get("cpu", {})
        net = (m.get("net_in", {}).get("sum") or 0) + (m.get("net_out", {}).get("sum") or 0)
        window = u.get("window_hours") or 0
        per_day = net / 1e6 / max(window / 24, 1 / 24)
        verdict = "IDLE" if (cpu.get("p95") is not None and cpu["p95"] < 5 and per_day < 5) else "busy/unknown"
        print(f"{rid}: {verdict:12s} cpu p95={cpu.get('p95')}% max={cpu.get('max')}% "
              f"points={cpu.get('points')} net={per_day:.2f} MB/day window={window} h")
    for rid in res.get("missing", []):
        print(f"{rid}: not found")


asyncio.run(main())
