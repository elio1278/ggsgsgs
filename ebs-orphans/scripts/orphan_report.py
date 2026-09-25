"""Code Mode helper (runs in the TrueForge sandbox): unattached volumes + orphaned snapshots, priced.

    python /opt/tfy/skills/ebs-orphans/scripts/orphan_report.py [--server undertaker-aws] [--region us-east-1]
"""

import argparse
import asyncio

from mcp_client import call_tool


async def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--server", default="undertaker-aws")
    ap.add_argument("--region", action="append")
    a = ap.parse_args()
    res = await call_tool(a.server, "find_waste", body={"regions": a.region or ["all"],
                                                         "types": ["ebs_volume", "ebs_snapshot"], "max_results": 100})
    rows = [f for f in res["findings"] if f["rule"] in ("ebs_unattached", "snapshot_orphaned")]
    total_inr = sum(f["monthly"]["inr"] or 0 for f in rows)
    print(f"{len(rows)} EBS findings, ~Rs {total_inr:,}/mo at list price")
    for f in rows:
        flag = " [instruction-like tag!]" if f["injection_suspect"] else ""
        print(f"  {f['resource_id']:22s} {f['rule']:17s} {f['verdict']:18s} "
              f"Rs {f['monthly']['inr'] or 0:>7,}/mo  iac={f['iac']:14s} actionable={f['actionable']}{flag}")


asyncio.run(main())
