---
name: ebs-orphans
description: Unattached EBS volumes and orphaned snapshots - how to prove they're waste, price them (gp2 vs gp3, IOPS, incremental snapshots) and the safe way to remove them (snapshot, quarantine, Recycle Bin). Includes a Code Mode report script.
---

# Unattached EBS volumes and orphaned snapshots

**Volumes.** State `available` = attached to nothing. Check CloudTrail for when it was detached and who created it.
Recent volumes (hours old) may be about to be attached: lower the confidence.

**Price.** Size × per-GB rate for its type (gp3 $0.08, gp2 $0.10 per GB-month in us-east-1), plus gp3 IOPS above
3,000 and throughput above 125 MB/s, or io1/io2 provisioned IOPS. A 500 GB disk is ~$40/mo on gp3, ~$50 on gp2.

**Safe removal.**
1. Quarantine: a safety snapshot (tagged `undertaker:backup=true`), then the tag `undertaker:state=quarantined`.
2. Delete (second approval): the volume goes to the **Recycle Bin** (tag-level rule), restorable with the **same
   volume ID** for the retention period. The snapshot stays as the long-term way back (new volume ID).

**Snapshots.** Orphaned = the source volume is gone, no AMI uses it, and it's older than 30 days. Cost is an **upper
bound** (snapshots are incremental). AWS Backup / DLM snapshots are deliberate: never propose them. Report-only in
this version.

**Code Mode helper**:
```
python /opt/tfy/skills/ebs-orphans/scripts/orphan_report.py --region us-east-1
```
