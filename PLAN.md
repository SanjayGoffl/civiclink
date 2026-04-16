# Opportunity OS — Implementation Plan

> **Hackathon build plan. Simple. Realistic. Shippable.**

---

## Stack

| Layer    | Tool         |
|----------|--------------|
| Frontend | Next.js      |
| Backend  | FastAPI      |
| Database | Supabase     |
| AI       | Ollama       |
| TTS      | Coqui TTS (optional) |

---

## Data Models

### Users
```
id, phone, age, occupation, pincode, language (default: "en")
```

### Opportunities
```
id, title, type (scheme/job/training/alert), description,
simplified_desc, location, pincode, eligibility (json),
source, source_type, expiry_date, verified (bool)
```

### Matches
```
user_id, opportunity_id, score, created_at
```

---

## Phase 1 — Project Setup

**Goal:** Running skeleton with empty pages.

- [ ] Init Next.js frontend (`npx create-next-app@latest frontend`)
- [ ] Init FastAPI backend (`backend/main.py`) with CORS
- [ ] Connect Supabase — create 3 tables (Users, Opportunities, Matches)
- [ ] Verify frontend ↔ backend can talk (ping endpoint)
- [ ] Seed 5–10 mock opportunities in Supabase

---

## Phase 2 — Opportunity Ingestion

**Goal:** Admin can add opportunities via API or simple form.

Backend (`POST /opportunity`):
- Accept: title, raw_description, type, location, pincode, eligibility (free text), source, expiry_date
- Call AI module → classify + simplify
- Store structured record in Supabase

Frontend (Admin/Operator page):
- Simple form: title, description, type dropdown, location, pincode, expiry
- Submit → call POST /opportunity → show success

---

## Phase 3 — AI Processing Module

**Goal:** LLM (Ollama) processes raw opportunity text.

Steps per opportunity:
1. Classify type (scheme / job / training / alert)
2. Extract eligibility fields (age range, occupation, location)
3. Simplify description to 2–3 plain sentences

Use `ollama` Python client, model: `llama3` or `mistral`.

```python
# backend/ai.py
def process_opportunity(raw_text):
    prompt = f"""
    Given this opportunity: {raw_text}
    Return JSON with:
    - type: scheme|job|training|alert
    - eligibility: {{ age_min, age_max, occupations[], pincodes[] }}
    - simplified: "2-3 plain sentence summary"
    """
    # call ollama, parse JSON response
```

---

## Phase 4 — User Profiles (Aadhaar Sandbox Mock)

**Goal:** Users register by typing an Aadhaar number. System auto-fetches demographic data using synthetic UIDAI test data.

Backend:
- `POST /user/auth` — Takes synthetic Aadhaar, returns mock demographic profile (Name, Age, DOB, Gender, Pincode/State).
- `POST /user` — Save complete profile.
- `GET /user/{id}` — fetch profile.

Frontend (User page):
- Simple form: Enter 12-digit Aadhaar
- OTP is simulated (accepts any 4-digit code)
- Auto-fills data: Name, Age, Gender, State, Pincode
- User explicitly selects: Occupation, Category (e.g., General, OBC, SC/ST, Farmer, etc. to match myscheme filters).
- Store profile in Supabase

---

## Phase 5 — Matching Engine

**Goal:** Find which opportunities match a user.

Backend (`GET /matches/{user_id}`):

```python
def match(user, opportunities):
    results = []
    for opp in opportunities:
        if not is_expired(opp): continue  # skip expired
        eligibility = opp["eligibility"]
        location_match = user["pincode"] == opp["pincode"]
        age_match = eligibility["age_min"] <= user["age"] <= eligibility["age_max"]
        occ_match = user["occupation"] in eligibility["occupations"]
        if location_match and age_match and occ_match:
            results.append(opp)
    return results
```

Store matches in `Matches` table.

---

## Phase 6 — Ranking Engine

**Goal:** Sort matched opportunities dynamically using the Custom **O-Rank Algorithm**.

```
O-Rank = (Local Proximity × 0.4) + (Time Urgency × 0.4) + (Impact Multiplier × 0.2)
```
*(Only calculates if Eligibility == 1 in Phase 5 Matching)*

- **Local Proximity**: Pincode exact match = 100, Same district = 50, State = 10.
- **Time Urgency**: Expiring in < 48hrs = 100, < 7 days = 70, < 30 days = 30, No expiry = 10.
- **Impact Multiplier**: Verified Govt Scheme or High-wage Job = 100, General Training = 50.

Sort matches descending by total O-Rank score, return top 10.

---

## Phase 7 — Delivery Layer

**Goal:** Show output in 3 ways.

### A. Feed Dashboard
`GET /matches/{user_id}` → display ranked cards.

Each card shows:
- title
- type badge (scheme / job / training)
- urgency badge (urgent / normal)
- 2-line simplified description

### B. Receipt View
`GET /receipt/{user_id}` → one opportunity per page, print-ready HTML.

Shows: title, simplified description, eligibility, next steps, source.

### C. Voice Output (simulated)
`GET /audio/{user_id}` → TTS using Coqui or browser `speechSynthesis`.

Reads: opportunity title + simplified description.

### D. Operator Dashboard
Separate view: list all opportunities + how many users matched each.

---

## Phase 8 — UI Polish

**Goal:** Clean, readable, professional UI.

Colors:
- Background: `#F8FAFC`
- Primary text: `#1E293B`
- Secondary: `#64748B`
- Accent: `#3B82F6`

Font: Inter (Google Fonts)

Screens to build:
1. `/` — Dashboard (ranked opportunity feed)
2. `/opportunity/[id]` — Detail + receipt + audio buttons
3. `/register` — User registration
4. `/admin` — Opportunity input form
5. `/operator` — Operator view

---

## API Summary

| Method | Endpoint              | Description                |
|--------|-----------------------|----------------------------|
| POST   | /opportunity          | Add new opportunity        |
| GET    | /opportunities        | List all opportunities     |
| POST   | /user                 | Create user profile        |
| GET    | /user/{id}            | Get user profile           |
| GET    | /matches/{user_id}    | Ranked matches for user    |
| GET    | /receipt/{user_id}    | Receipt-style output       |
| GET    | /audio/{user_id}      | Audio output trigger       |

---

## Folder Structure

```
anti/
├── frontend/          # Next.js app
│   ├── pages/
│   │   ├── index.js          # Dashboard
│   │   ├── register.js       # User registration
│   │   ├── admin.js          # Add opportunity
│   │   ├── operator.js       # Operator view
│   │   └── opportunity/[id].js  # Detail + receipt + audio
│   └── components/
│       ├── OpportunityCard.js
│       ├── Badge.js
│       └── ReceiptView.js
│
├── backend/           # FastAPI app
│   ├── main.py               # Routes
│   ├── ai.py                 # Ollama AI module
│   ├── matching.py           # Matching + ranking logic
│   ├── models.py             # Pydantic models
│   └── db.py                 # Supabase client
│
└── PLAN.md            # This file
```

---

## Build Order (Priority)

1. ✅ Setup (Phase 1)
2. ✅ Opportunity ingestion + AI (Phases 2 & 3)
3. ✅ User profile + matching + ranking (Phases 4, 5 & 6)
4. ✅ Delivery — feed + receipt + voice (Phase 7)
5. ✅ UI polish (Phase 8)

---

## What We Simulate (Not Real)

- Aadhaar (Simulated e-KYC using Synthetic UIDAI Data: e.g. 999941057058)
- OTP login (accept any 4-digit code)
- WhatsApp/SMS (show a mock "message sent" screen)
- Government DB (use our Supabase mock data, simulating myscheme.gov.in filters)

---

## Mock Data to Seed

Add these 5 records to Supabase before the demo:

| Title | Type | Pincode | Eligibility |
|-------|------|---------|-------------|
| PM Kisan Samman | scheme | 600001 | age 25-65, farmer |
| MGNREGA Work | job | 600001 | age 18-60, any |
| Digital Literacy Training | training | 600002 | age 18-40, any |
| Free Eye Checkup Camp | alert | 600001 | age 40+, any |
| Tailoring Skill Course | training | 600003 | age 20-50, women |

---

## Done = Demo Ready

The demo flow:
1. Admin adds an opportunity → AI processes it
2. User registers with phone + profile
3. Dashboard shows ranked, matched opportunities
4. Click any card → receipt view + play audio
5. Operator sees all opps + match counts
