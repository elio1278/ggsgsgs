---
name: ec2-idle
description: Decide whether running EC2 instances are idle (CPU p95, network), what stopping vs deleting really saves, and which instances must never be touched (ASG, EKS/ECS, spot, protected). Includes a Code Mode utilization script.
---

# Idle EC2 instances

**Signal.** CPU p95 below 5% **and** network below 5 MB/day over the observation window (both configurable).
No datapoints means "can't judge": never call an instance idle without metrics.

**Exclusions.** Auto Scaling group members (they'd be replaced), EKS/ECS/Beanstalk hosts, spot instances, anything
tagged `undertaker:keep=true` or production.

**Keep / ask owner if.** Stop or termination protection is on, it's a registered load-balancer target, or a CloudWatch
alarm watches it (someone cares).

**Money, honestly.**
- Stopping saves **compute** (plus an auto-assigned public IPv4). Attached EBS volumes and any Elastic IP keep billing.
- A Savings Plan or Reserved Instance may already cover it, in which case stopping saves nothing. Say so.
- Quarantine = stop (scream test). Terminate is not part of this version.

**Code Mode helper**: summarize many instances without pulling raw metrics into the chat:

```
python /opt/tfy/skills/ec2-idle/scripts/utilization_report.py i-0abc i-0def
```
