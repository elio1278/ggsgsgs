---
name: elb-forgotten
description: Forgotten load balancers (ALB, NLB, Classic) - how to prove nothing uses them (targets, traffic, DNS, deletion protection), what they cost, and why their way back is a recreation with a NEW DNS name.
---

# Forgotten load balancers

**Signals.** No healthy targets in any target group, and/or zero requests (ALB/CLB) or zero new flows (NLB) over the
window. CloudWatch publishes no datapoints for zero-request ALBs, so "no data" means zero traffic.

**Blockers (keep / ask owner).** Live targets, a Route 53 record (alias or CNAME) pointing at its DNS name, or
**deletion protection** enabled (someone deliberately protected it).

**Price.** ALB and NLB ~$0.0225/h (~$16.43/mo) in us-east-1; Classic $0.025/h. Idle LCU charges are ~0 and excluded.

**Safe removal.**
1. Quarantine: export the full config (listeners, rules, target groups, attributes, tags) to `local/backups`, then
   tag `undertaker:state=quarantined`.
2. Delete (second approval): DeleteLoadBalancer.
3. Way back: recreate from the saved config. **The DNS name will change**, so any CNAMEs or clients must be updated.
   Say this clearly in the Death Certificate.

IaC-managed load balancers (CloudFormation tag or stack list) get "fix it in the template", never an API delete.
