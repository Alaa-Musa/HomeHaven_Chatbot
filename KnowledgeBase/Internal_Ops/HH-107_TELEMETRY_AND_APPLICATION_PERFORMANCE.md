doc_id: HH-107
title: Telemetry & Application Performance — Metrics
doc_type: guideline
version: 1.0
last_updated: 2026-03-07
---

## 1. Overview
To ensure a seamless digital shopping experience, this guideline defines the core Service Level Indicators (SLIs) for our mobile and web applications. Continuous monitoring of these telemetry points allows the engineering team to proactively address bottlenecks before they impact conversion rates.

## 2. Core Performance Metrics
App Load Times & Responsiveness
Time to First Byte (TTFB): Goal < 200ms. Measures the responsiveness of the web server or API gateway.
Largest Contentful Paint (LCP): Goal < 2.5s. Measures the time it takes for the primary product image or hero banner to become visible.
First Input Delay (FID): Goal < 100ms. Tracks the time from when a user first interacts (e.g., taps "Add to Cart") to when the browser begins processing the handler.
Stability & Reliability
Crash-Free User Sessions: Target: 99.9%. Percentage of unique user sessions that do not end in a fatal application crash.
API Error Rate: Monitoring of 4xx (Client) and 5xx (Server) response codes across checkout and search microservices.
Memory Footprint: Tracking of heap usage on mobile devices to prevent background kills on low-end hardware.
Feature Adoption & Engagement
Feature Discovery Rate: Percentage of users who interact with a new feature (e.g., "AR Room Visualizer") within 48 hours of release.
Conversion Funnel Drop-off: Real-time telemetry on telemetry events at each stage of the checkout flow.
Active Session Duration: Analysis of high-value paths versus "dead-end" navigation where users exit the app.

## 3. Monitoring & Alerting
Critical Thresholds: Any metric falling into the "P95" (95th percentile) lag category for more than 5 minutes triggers an automated Tier 2 Engineer alert.
Reporting: Weekly performance dashboards are reviewed by the Product and UX teams to prioritize the technical debt backlog.