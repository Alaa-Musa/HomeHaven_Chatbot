---
doc_id: HH-70
title: Data Security — Best Practices for POS Systems
doc_type: guideline
version: 1.0
last_updated: 2026-01-29
---

## Scope
Covers point-of-sale devices, payment terminals, and related backend services used in stores.

## Core Controls
- PCI-DSS compliant handling of cardholder data; avoid storing sensitive data on devices unless required.
- End-to-end encryption (E2EE) for card data, shielded PIN entry, and tamper-evident seals.
- Strong password policies: minimum 12 characters, multi-factor authentication where possible.
- Device hardening: disable default accounts, limit remote access, keep firmware up-to-date.

## Physical Security
- Secure checkout counters with access restricted to authorized personnel.
- Use tamper-evident packaging for terminals and peripherals.
- Screen privacy measures to prevent shoulder-surfing.

## Incident Response
- Immediate isolation of compromised devices; reset credentials; perform forensic review.
- Notify customers if their data may have been exposed; document timelines and actions.

## Training
- Regular security awareness training for store staff.
- Annual certification on PCI-DSS basics and phishing awareness.

## Compliance
- Align with UAE data protection guidelines and international best practices.