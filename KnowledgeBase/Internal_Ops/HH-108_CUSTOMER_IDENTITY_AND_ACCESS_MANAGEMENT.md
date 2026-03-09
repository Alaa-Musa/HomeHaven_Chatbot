---
doc_id: HH-108
title: Customer Identity & Access Management (CIAM)
doc_type: guideline
version: 1.0
last_updated: 2026-03-08
---

## 1. Overview
This guideline establishes the framework for managing customer identities across all retail touchpoints. The goal is to provide a frictionless login experience while maintaining rigorous security standards to protect customer accounts and sensitive personal data.

## 2. User Provisioning & Lifecycle
Account Creation: Support for Just-In-Time (JIT) provisioning. Users may register via traditional email/password or verified Social Login (OIDC/SAML).
Progressive Profiling: To minimize friction, only essential data (Email/Name) is collected at signup. Extended profile data (Address/Preferences) is gathered incrementally as the customer interacts with the platform.
Account Deactivation: Automated workflows for handling "Right to be Forgotten" requests, ensuring data is purged from identity providers and downstream marketing systems simultaneously.

## 3. Authentication & Authorization
Multi-Factor Authentication (MFA): Risk-based MFA is triggered for high-value actions, such as changing shipping addresses, viewing saved payment methods, or loyalty point redemptions.
Password Policy: Minimum 12 characters with complexity requirements. Passwords must be checked against known "Pwned" databases at the time of creation.
Single Sign-On (SSO): Seamless transition between the mobile app, web store, and in-store kiosk services using a unified identity token.

## 4. Session Security
Token Management: Use of short-lived Access Tokens and secure Refresh Tokens.
Session Timeouts:
Inactive: Web sessions expire after 30 minutes of inactivity.
Absolute: All sessions require re-authentication after 14 days.
Concurrent Session Control: Limits the number of active logins per customer to prevent account sharing or credential stuffing attacks.
Secure Cookies: All session cookies must be flagged as HttpOnly, Secure, and SameSite=Strict.
