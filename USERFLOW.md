# Opportunity OS — User Flows

All the people who interact with the system and exactly what they experience.

---

## The 4 User Types

| User Type | Device | Literacy | How They Interact |
|-----------|--------|----------|-------------------|
| App User | Smartphone | Medium–High | Opens the web app |
| Booth User | No device | Low / None | Goes to milk booth or ration shop |
| SMS User | Basic phone | Low–Medium | Receives SMS alerts |
| Operator | Desktop/Tablet | Medium | Runs the operator dashboard |

---

## Flow 1 — App User (Smartphone)

> Someone with a phone who can use a basic web app.

```
FIRST TIME
──────────
User opens the app (browser link or shared link)
  ↓
Sees: "Enter your 12-digit Aadhaar number"
  ↓
Gets a simulated OTP (any 4 digits)
  ↓
System auto-fetches: Name, Age, Gender, State, Pincode (from Synthetic Aadhaar DB)
User enters: Occupation, Mobile Number
  ↓
Lands on: Dashboard — "Today's Opportunities"
  ↓
Sees ranked cards:
  [ PM Kisan Scheme — Urgent ]
  [ MGNREGA Work — Normal    ]
  [ Eye Checkup Camp — Today ]
  ↓
Taps any card
  ↓
Sees: Opportunity Detail
  - simplified description (2–3 lines)
  - who is eligible
  - what to do next
  ↓
Options:
  [ Generate Receipt ]  →  Opens receipt view (printable)
  [ Play Audio       ]  →  Reads the card aloud (TTS)
  [ Back             ]  →  Returns to dashboard

RETURNING
──────────
User opens app → auto logs in by phone number → sees updated feed
```

---

## Flow 2 — Illiterate User at Milk Booth / Ration Shop

> Person walks in. Has no phone. Relies on the booth operator.

```
Person walks into milk booth or ration shop
  ↓
Says to operator:
  "I heard there is some government help. Can you check?"
  ↓
Operator asks:
  "Do you have your Aadhaar number?"
  ↓
Operator types Aadhaar into the Operator Dashboard
System auto-fetches: Age, Gender, Address
Operator asks and types: Occupation
  ↓
System shows:
  - matched opportunities for that profile
  - ranked by urgency
  ↓
Operator clicks: [ Print Receipt ]
  ↓
Printer outputs a receipt (like a bill):

  ┌────────────────────────────────────┐
  │  OPPORTUNITY RECEIPT               │
  │  PM Kisan Samman Yojana            │
  │  ─────────────────────────────     │
  │  For: Farmers aged 25–65           │
  │  Benefit: Rs. 6000 per year        │
  │  Apply at: Nearest CSC / e-Sevai   │
  │  Expires: 30 June 2025             │
  │  Source: agriculture.gov.in        │
  └────────────────────────────────────┘

  ┌────────────────────────────────────┐
  │  MGNREGA Work Available            │
  │  ─────────────────────────────     │
  │  For: Any adult, local area        │
  │  Work: 100 days guaranteed wages   │
  │  Contact: Panchayat office         │
  └────────────────────────────────────┘

  ↓
Person takes the receipt home
  ↓
Family member or neighbor helps them act on it
```

**Why this works:**
- Person never needs a phone
- Receipt is in their language (Tamil)
- Simple enough for someone else to read to them

---

## Flow 3 — SMS User (Basic Phone)

> Has a phone but uses only calls and SMS. No apps, no internet.

```
One-time registration (done by operator or family member via web):
  - phone number, age, occupation, pincode stored in system
  ↓
System runs a scheduled job (daily or on new opportunity):
  - finds new matches for each user
  - sends SMS to matched users
  ↓
User receives SMS:

  ──────────────────────────────────
  OpportunityOS Alert:
  1. PM Kisan - Free for farmers
     Visit nearest CSC
  2. Free Eye Camp - Tomorrow 10am
     Venue: Panchayat Hall
  Reply STOP to unsubscribe
  ──────────────────────────────────

  ↓
User calls family / neighbor / goes to booth
  ↓
Action taken
```

**SMS format rules:**
- Max 160 characters per message
- Plain language
- No links (useless on basic phones)
- At most 2 opportunities per SMS to avoid confusion

---

## Flow 4 — Operator (e-Sevai / Milk Booth / NGO Worker)

> The human bridge between the system and offline users.

```
Operator logs into Operator Dashboard
  ↓
Main view:
  ┌──────────────────────────────────────────────────┐
  │  OPERATOR DASHBOARD                              │
  │                                                  │
  │  All Active Opportunities           [ + Add New ]│
  │  ──────────────────────────────────────────────  │
  │  PM Kisan Scheme         Matched: 34 users  📋   │
  │  MGNREGA Work            Matched: 89 users  📋   │
  │  Digital Literacy Course Matched: 12 users  📋   │
  └──────────────────────────────────────────────────┘

  ↓
Operator can:
  A. [ Search User ]     →  Enter phone/age/pincode → see their matches
  B. [ Print Receipt ]   →  Print matched opportunities for that person
  C. [ Add Opportunity ] →  Enter new local job or notice into the system
  D. [ View All Matches ]→  See who was matched with what

Adding a new opportunity:
  ↓
Operator fills form:
  - Title
  - Description (free text, can be rough)
  - Type (scheme / job / training / alert)
  - Pincode / location
  - Expiry date
  - Source name
  ↓
System AI processes it:
  - classifies the type
  - extracts eligibility
  - simplifies the text
  ↓
Opportunity goes live → matches run again → SMS alerts sent
```

---

## Complete System Flow (All Users Together)

```
        [ OPERATOR / ADMIN ]
               │
               ▼
    Adds opportunity to system
               │
               ▼
        [ AI PROCESSING ]
    classify → extract → simplify
               │
               ▼
        [ SUPABASE DB ]
    stored with eligibility,
    pincode, expiry, source
               │
         ┌─────┴──────┐
         ▼            ▼
   [ MATCHING ]   [ SMS JOB ]
   user profiles  finds new matches
   checked        sends SMS alerts
         │            │
    ┌────┴────┐   ┌───┴───┐
    │         │   │       │
    ▼         ▼   ▼       ▼
  APP      RECEIPT  SMS   AUDIO
  USER     (booth   USER  OUTPUT
  (web)    print)   (basic (TTS)
           ↓        phone) ↓
         ILLITERATE       READ ALOUD
         USER             AT BOOTH
```

---

## Key Design Principles Per User

| User | Must Work Without | Key Experience |
|------|-------------------|----------------|
| App User | Operator help | Self-serve, fast, clean feed |
| Booth User | Phone, literacy | Operator helps, gets a receipt |
| SMS User | Internet, apps | Gets 2-line alert on any phone |
| Operator | Being an expert | Simple dashboard, one-click receipt |

---

## What We Build for the Demo

| Flow | What we show |
|------|-------------|
| App User | Register → dashboard → card detail → receipt + audio |
| Booth User | Operator searches user → prints receipt (printable HTML) |
| SMS User | Show a mock SMS in the demo (simple UI simulation) |
| Operator | Dashboard with opportunities + match counts + add form |
