---
doc_id: HH-82
title: Data Retention & Deletion — Guidance
doc_type: guideline
version: 1.1
last_updated: 2026-03-07
---

## Retention Periods
- Keep order history and transactional data for analysis and compliance (7 years for UAE FTA requirements).
- Apply data minimization and privacy-by-design principles to all marketing and telemetry data.

## Deletion Requests & Timelines
- **Resolution Guarantee:** All verified user data deletion requests must be processed and confirmed to the customer within **30 calendar days**, as per Policy HH-105.
- **Eradication Scope:** Data must be purged from all active production systems, including third-party logistics and marketing platforms.
- **Backup Rotation:** While active data is erased within 30 days, residual data in encrypted backups will be fully overwritten within a maximum of **60 days** through standard rotation cycles. 

## Security
- Use AES-256 encryption at rest and TLS 1.2+ in transit.
- Enforce Role-Based Access Control (RBAC) for all sensitive PII access.
