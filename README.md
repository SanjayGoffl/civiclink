# Opportunity OS — Master Concept & Rules

This document consolidates the final idea, the system logic, and the strategic decisions made during our discussions. It serves as the single source of truth for how the project directly answers the hackathon's problem statement.

---

## 1. The Core Idea

**The Problem:** In rural/semi-urban areas, government schemes, local jobs, training, and subsidies go unnoticed due to complex platforms, poor maintenance, and low digital literacy.
**The Solution:** Next-Gen Opportunity Intelligence. 

**Opportunity OS** is not just an app—it's an intelligent gateway. It uses AI and Web Scraping to consolidate messy local opportunities into structured data, and then actively bridges the digital divide by delivering them via personalized dashboards, offline receipts at local booths, and SMS. 

Powered by **Pincode Intelligence** and **Demand-Supply Matching**, it doesn't just show data—it maps local workers to immediate local needs.

*We don’t just find schemes. We surface any local opportunity and deliver it to the right person at the right time, even if they can't read or own a smartphone.*

---

## 2. How User Profiles Work (The "Aadhaar + 1" Method)

To avoid forcing users into 20-field government forms, we utilize an **Aadhaar-First Setup**:

### Step 1: Simulated Aadhaar Fetch (The Heavy Lifting)
- The user (or booth operator) types in a 12-digit Aadhaar number + OTP.
- The system automatically triggers an e-KYC flow (simulated via UIDAI Sandbox Test UIDs).
- **Auto-fetches:** Name, Age/DOB, Gender, State, and Pincode.

### Step 2: The Supplement (Quick Selects)
Because Aadhaar legally does not store sensitive profiles (Caste, Income, Occupation), the UI presents 3 to 4 massive, simple buttons.
- **Operator asks or User taps:** Occupation (Farmer/Student/etc.) and Category (General/OBC/SC-ST).
- *(Note on Scope: We are simulating family details and family income. In the actual real-world scope, this will happen through direct government tie-ups and PDS database integrations).*

*Result: A perfectly matched user profile generated in 10 seconds with zero typing.*

---

## 3. Where Does The Data Come From? (Ingestion Rules)

To bridge the hyper-local information gap (local jobs, temporary work, targeted local subsidies), the system mixes **Automated Scraping** and **Trusted Gatekeepers**.

1. **State/National Schemes:** Pulled via web scraping mechanisms and API integrations from standard government sources (like myscheme).
2. **Local Panchayat / e-Sevai Operators:** When a local contractor needs 50 workers, or the block office has a seed subsidy, the operator logs in to the dashboard. They paste a messy, raw text message.
3. **AI structuring:** The AI (Ollama) reads the raw text:
   - Identifies if it's a `job`, `training`, `scheme`, or `alert`.
   - Extracts eligibility (e.g., "Age 18-40, Pincode 600001").
   - Simplifies the text into 2 sentences.

*Rule: Data from Trusted Gatekeepers gets a `Verified ✅` badge.*

---

## 4. The 4 User Flows (Accessibility For All)

Our system ensures no one is left behind, regardless of their device or digital literacy:

1. **The Smartphone User:** Logs in securely, browses a clean categorized feed of ranked matches.
2. **The Illiterate User:** Walks into the ration shop/milk booth. Gives Aadhaar to the operator. The operator prints a **Tamil Opportunity Receipt** (like a grocery bill) showing what the person is eligible for.
3. **The SMS User:** Once registered at a booth, the backend continuously scans for new matches and sends an automated 160-character plain text SMS alert to their basic feature phone.
4. **The Operator:** Uses a desktop dashboard to manage community members, add local opportunities, and print receipts.

---

## 5. Development Rules & Hackathon Boundaries

*What we are building vs. what we are simulating to keep the scope realistic.*

1. **One Unified Backend:** A single FastAPI + Supabase backend serving all UI views.
2. **Offline-Friendly AI:** Ollama running locally ensures we don't rely heavily on paid external APIs for the ingestion intelligence.
3. **Synthetic Data:**
   - Aadhaar API is mocked using official UIDAI Test UID formats (e.g., `999941057058`).
   - OTPs will accept any 4-digit code.
   - We will seed 5-10 hyper-specific local opportunities for the demo.
4. **The Instagram-like Feed Algorithm (O-Rank):** We do not display random lists. Matches are dynamically scored using our custom **Opportunity Rank (O-Rank)** formula to generate a tailored feed. 
   - `O-Rank = Eligibility Gating * [ (Local Proximity * 0.4) + (Time Urgency * 0.4) + (Impact Multiplier * 0.2) ]`
   - *Eligibility Gating:* Acts as a strict filter (0 or 1)—if they don't qualify, score is 0.
   - *Local Proximity:* Exact pincode match gets max points.
   - *Time Urgency:* Opportunities expiring in 48 hours spike to the top.
   - *Impact Multiplier:* High-value opportunities (like long-term jobs or high-payout subsidies) get a slight boost.

---
**Status:** Architecture is finalized. Next step: Begin implementation.
