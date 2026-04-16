# System Design

## Architecture Overview

Frontend (Next.js)
↓
Backend (FastAPI)
↓
Database (Supabase)
↓
AI Layer (Ollama)

---

## Core Components

### 1. API Layer (FastAPI)

Endpoints:

* POST /opportunity
* GET /opportunities
* POST /user
* GET /matches/{user_id}
* GET /receipt/{user_id}
* GET /audio/{user_id}

---

### 2. AI Processing Module

Steps:

1. Input text
2. Classify type
3. Extract structured data
4. Simplify description

---

### 3. Matching Engine

Logic:

* Filter by:

  * age
  * occupation
  * location
* Output list of eligible users

---

### 4. Ranking Engine

Score calculation:
score =
(relevance * 0.4) +
(urgency * 0.3) +
(location * 0.2)

---

### 5. Data Model

Tables:

Users:

* id
* phone
* age
* occupation
* pincode

Opportunities:

* id
* type
* description
* location
* eligibility
* expiry_date

Matches:

* user_id
* opportunity_id
* score

---

### 6. Output Layer

* Receipt Generator (HTML template)
* Audio Generator (TTS)
* Dashboard View

---

## Flow

1. Add opportunity
2. AI processes input
3. Store structured data
4. Match users
5. Rank results
6. Generate outputs
