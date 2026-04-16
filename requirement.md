# Requirements

## Functional Requirements

### FR1: Opportunity Management

* Add opportunity (job/scheme/training)
* Store structured data

### FR2: AI Processing

* Classify opportunity
* Extract structured fields
* Simplify description

### FR3: User Management

* Create user profile
* Store:

  * phone number
  * age
  * occupation
  * pincode

### FR4: Matching Engine

* Match opportunities to users
* Filter by:

  * eligibility
  * location

### FR5: Ranking Engine

* Assign score to each opportunity
* Sort results per user

### FR6: Output Generation

* Generate receipt view
* Generate audio output
* Display operator dashboard

---

## Non-Functional Requirements

### NFR1: Performance

* Response time < 2 seconds for matching

### NFR2: Simplicity

* Minimal dependencies
* Easy to run locally

### NFR3: Scalability (basic)

* Modular backend design

### NFR4: Reliability

* Handle invalid inputs gracefully

---

## Technical Requirements

* Frontend: Next.js
* Backend: FastAPI
* Database: Supabase
* AI: Ollama
* Optional:

  * Whisper (STT)
  * Coqui TTS (audio)

---

## Data Requirements

Each opportunity must include:

* type
* location
* eligibility
* source
* expiry_date

Each user must include:

* age
* occupation
* pincode
