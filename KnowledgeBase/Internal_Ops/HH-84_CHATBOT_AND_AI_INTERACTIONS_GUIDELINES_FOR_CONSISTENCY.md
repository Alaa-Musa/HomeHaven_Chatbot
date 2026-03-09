---
doc_id: HH-84
title: Chatbot & AI Interactions — Guidelines for Consistency
doc_type: guidelines
version: 1.0
last_updated: 2026-02-12
---

# Chatbot & AI Interactions — Guidelines for Consistency (HH-84)

## 1. Overview
As HomeHaven integrates automated assistance into the UAE shopping experience, these guidelines ensure that our AI-driven touchpoints—including the "HavenBot" and automated email triaging—reflect our brand’s commitment to reliability, local cultural nuance, and technical accuracy.

## 2. Interaction Principles
To maintain a premium "Home-First" service standard, all AI interactions must adhere to the following:
*   **Tone and Language:** Maintain a polite, helpful, and professional persona. Avoid overly robotic phrasing; instead, use clear, conversational English (and Arabic where localized) that aligns with our **Customer Care Standards (HH-01)**.
*   **Consistency:** AI must provide identical information to our web-based FAQs. For example, if a user asks about the **CrispWave CW-AF55** capacity, the AI must consistently cite **5.5L** as per the official product sheet (**HH-31**).
*   **Proactive Escalation:** If a query remains unresolved after two automated attempts, or if the user uses keywords like "Human," "Manager," or "Complaint," the system must trigger an immediate transfer to a **Live Specialist (HH-30)** during operational hours (09:00–21:00 GST).

## 3. Safety & Data Privacy
The protection of HomeHaven customer data is paramount during automated sessions:
*   **Sensitive Data Masking:** AI interfaces are prohibited from requesting or displaying full Credit Card numbers, CVVs, or account passwords. Any such data entered by a user must be automatically redacted in logs.
*   **Verified Knowledge Base:** Responses must be pulled exclusively from the **Verified Document Library** (HH-Series). AI is forbidden from "hallucinating" or speculating on future product releases or undocumented discount codes.
*   **Identity Verification:** Before disclosing order-specific details (e.g., tracking a **DustDash** delivery), the AI must confirm the user’s identity via a one-time passcode (OTP) or authenticated app session.

## 4. Monitoring & Quality Assurance
*   **Tone Audits:** The Customer Experience (CX) team performs weekly reviews of 5% of all chatbot transcripts to ensure the AI remains empathetic and culturally appropriate for the UAE market.
*   **Accuracy Training:** When new policies are released (e.g., **Refund Timing HH-53**), the AI’s underlying data model must be updated within **4 hours** of the document's "Last Updated" timestamp.
*   **Feedback Loop:** Every AI interaction must conclude with a 1-click "Was this helpful?" survey. Any "No" response with a negative sentiment score is automatically flagged for manual review by a Tier 2 Lead.

## 5. Technical Constraints
*   **Out-of-Scope Queries:** If a user asks for non-retail advice (e.g., medical or legal), the AI must politely decline and redirect the user back to HomeHaven-related topics such as product specs, shipping, or **HavenPlus** rewards.
*   **Latency Standards:** Responses should be generated within **2 seconds** to maintain a frictionless user experience on mobile networks.
