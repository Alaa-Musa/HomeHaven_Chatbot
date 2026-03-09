---
doc_id: HH-71
title: Merchant Integrations — API & Webhooks Overview
doc_type: reference
version: 1.0
last_updated: 2026-01-30
---

## Purpose
Provide a stable, secure gateway for merchant integrations with HomeHaven catalog and order management systems.

## API Model
- RESTful endpoints for product catalog, pricing, and stock sync.
- Webhook events for order status changes, shipments, and refunds.

## Authentication
- API keys with per-environment scopes.
- Rotation policy and secure storage recommended.

## Rate Limits & Throttling
- Typical 1,000 requests per minute per API key; bursts managed with exponential backoff.
- Webhook retries on failure with exponential backoff.

## Data Mapping
- Catalog: product_id, name, category, price, stock_level, attributes.
- Orders: order_id, status, items, totals, customer_id.

## Error Handling
- Standard HTTP status codes; detailed error messages for troubleshooting.

## Security
- TLS 1.2+; mutual TLS recommended for sensitive operations.
- Audit logging of all API interactions.