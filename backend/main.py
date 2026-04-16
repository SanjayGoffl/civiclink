"""
Opportunity OS — FastAPI Backend
Single backend serving both webapp and mobile app
"""
import csv, json, re, os
from pathlib import Path
from typing import Optional, List
from fastapi import FastAPI, Query, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
import httpx

app = FastAPI(title="Opportunity OS API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# ─── Dataset path ───
BASE = Path(__file__).parent.parent / "dataset"
DATA_FILE = BASE / "updated_data.csv"

# ─── Aadhaar simulation DB ───
AADHAAR_DB = {
    "123456789012": {
        "name": "Arun Kumar", "dob": "1981-05-15", "age": 45, "gender": "Male",
        "address": "No 42, Pillayar Kovil St, Melmaruvathur", "pincode": "603319",
        "state": "Tamil Nadu", "phone": "9845012345", "occupation": "Farmer",
        "income": 85000, "caste": "OBC"
    },
    "987654321098": {
        "name": "Priya Subramanian", "dob": "1994-11-20", "age": 32, "gender": "Female",
        "address": "Door 12B, West Mada St, Mylapore, Chennai", "pincode": "600004",
        "state": "Tamil Nadu", "phone": "9962054321", "occupation": "Small Business Owner",
        "income": 120000, "caste": "General"
    },
    "456789012345": {
        "name": "Rajesh V", "dob": "2005-08-10", "age": 21, "gender": "Male",
        "address": "4/156, Middle Street, Vadipatti", "pincode": "625218",
        "state": "Tamil Nadu", "phone": "9500011223", "occupation": "Student",
        "income": 40000, "caste": "SC"
    },
    "567812349012": {
        "name": "Kavitha R", "dob": "1976-03-25", "age": 50, "gender": "Female",
        "address": "Plot 8, Annai Sathya Nagar, Hosur", "pincode": "635109",
        "state": "Tamil Nadu", "phone": "9443044556", "occupation": "Housewife",
        "income": 30000, "caste": "OBC"
    },
    "321098765432": {
        "name": "Selvam M", "dob": "1966-07-30", "age": 60, "gender": "Male",
        "address": "21, Market Road, Polur", "pincode": "606803",
        "state": "Tamil Nadu", "phone": "9865077889", "occupation": "Mason",
        "income": 95000, "caste": "MBC", "disability": "yes"
    },
}

# ─── Load dataset ───
_schemes_cache: Optional[List[dict]] = None

def load_schemes() -> List[dict]:
    global _schemes_cache
    if _schemes_cache is not None:
        return _schemes_cache

    schemes = []
    try:
        with open(DATA_FILE, encoding="utf-8", errors="replace") as f:
            reader = csv.DictReader(f)
            for i, row in enumerate(reader):
                name = row.get("scheme_name", "").strip().strip('"')
                cat  = row.get("schemeCategory", "").strip()
                level = row.get("level", "").strip()
                benefits = row.get("benefits", "").strip()
                eligibility = row.get("eligibility", "").strip()
                details = row.get("details", "").strip()
                tags_raw = row.get("tags", "")

                if not name:
                    continue

                # Parse tags
                tags = [t.strip().strip('"') for t in tags_raw.split(",") if t.strip()]

                # Extract age hints from eligibility text
                min_age, max_age = _parse_age(eligibility)
                gender = _parse_gender(eligibility + " " + name)
                income = _parse_income(eligibility)
                state_match = _parse_state(level + " " + eligibility + " " + cat)

                schemes.append({
                    "id": i + 1,
                    "name": name,
                    "category": cat,
                    "level": level,
                    "benefit": benefits[:150] if benefits else "See eligibility details",
                    "eligibility": eligibility[:300] if eligibility else "",
                    "description": details[:500] if details else eligibility[:300],
                    "tags": tags[:6],
                    "min_age": min_age,
                    "max_age": max_age,
                    "gender": gender,
                    "income_limit": income,
                    "state": state_match,
                    "apply_url": "",
                })

        _schemes_cache = schemes
        print(f"✅ Loaded {len(schemes)} schemes from dataset")
    except Exception as e:
        print(f"⚠️  Dataset load error: {e}")
        _schemes_cache = []
    return _schemes_cache


def _parse_age(text: str):
    t = text.lower()
    match = re.search(r'(\d+)\s*(?:to|-)\s*(\d+)\s*(?:year|yr|age)', t)
    if match:
        return int(match.group(1)), int(match.group(2))
    match = re.search(r'age(?:d)?\s*(?:above|over|minimum|min)?\s*(\d+)', t)
    if match:
        return int(match.group(1)), 100
    match = re.search(r'below\s*(\d+)\s*(?:year|yr|age)', t)
    if match:
        return 0, int(match.group(1))
    return 0, 100


def _parse_gender(text: str):
    t = text.lower()
    if "women" in t or "female" in t or "girl" in t:
        return "female"
    if "men" in t and "women" not in t:
        return "male"
    return "any"


def _parse_income(text: str):
    t = text.lower()
    match = re.search(r'income.*?(?:below|less than|under|not exceed(?:ing)?|upto|up to)\s*(?:rs\.?|inr|₹)?\s*([\d,]+)', t)
    if match:
        return int(match.group(1).replace(",", ""))
    match = re.search(r'(?:rs\.?|inr|₹)\s*([\d,]+)\s*(?:per year|p\.a|annual)', t)
    if match:
        return int(match.group(1).replace(",", ""))
    return 0  # 0 = no income limit


def _parse_state(text: str):
    states = [
        "Tamil Nadu", "Karnataka", "Kerala", "Andhra Pradesh", "Telangana",
        "Maharashtra", "Rajasthan", "Delhi", "West Bengal", "Uttar Pradesh",
        "Gujarat", "Punjab", "Haryana", "Bihar", "Jharkhand", "Odisha",
        "Madhya Pradesh", "Chhattisgarh", "Assam", "Himachal Pradesh",
    ]
    for s in states:
        if s.lower() in text.lower():
            return s
    return ""  # Central / any


# ─── MODELS ───
class AadhaarRequest(BaseModel):
    aadhaar: str

class OTPVerify(BaseModel):
    aadhaar: str
    otp: str

class UserProfile(BaseModel):
    aadhaar: str
    name: str
    age: int
    gender: str
    state: str
    pincode: str = ""
    occupation: str = ""
    income: int = 0
    caste: str = "General"
    education: str = ""
    disability: str = "no"
    is_student: str = "no"
    marital: str = "Single"
    residence: str = "Rural"
    minority: str = "Majority"
    govt_employee: str = "no"

class AIRequest(BaseModel):
    scheme_id: int
    profile: UserProfile

class MatchRequest(BaseModel):
    profile: UserProfile
    limit: int = 50
    offset: int = 0
    category: str = ""
    search: str = ""


# ─── HELPERS ───
def elig_score(scheme: dict, profile: UserProfile) -> str:
    score, total = 0, 0
    age = profile.age or 0
    inc = profile.income or 999999

    if scheme.get("min_age") or scheme.get("max_age"):
        total += 1
        if scheme["min_age"] <= age <= scheme["max_age"]:
            score += 1

    if scheme.get("gender") and scheme["gender"] != "any":
        total += 1
        if profile.gender.lower() == scheme["gender"].lower():
            score += 1

    if scheme.get("state") and scheme["state"] != "":
        total += 1
        if scheme["level"].lower() in ("central", "local"):
            score += 1
        elif profile.state == scheme["state"]:
            score += 1

    if scheme.get("income_limit", 0) > 0:
        total += 1
        if inc <= scheme["income_limit"]:
            score += 1

    if total == 0:
        return "maybe"
    r = score / total
    if r >= 0.85:
        return "yes"
    if r >= 0.5:
        return "maybe"
    return "no"


# ─── ROUTES ───
@app.get("/")
def root():
    return {"status": "ok", "service": "Opportunity OS API", "version": "1.0.0"}

@app.get("/api/health")
def health():
    schemes = load_schemes()
    return {"status": "healthy", "schemes_loaded": len(schemes)}


# ── Auth ──
@app.post("/api/auth/verify-aadhaar")
def verify_aadhaar(req: AadhaarRequest):
    raw = re.sub(r"\D", "", req.aadhaar)
    if len(raw) != 12:
        raise HTTPException(400, "Invalid Aadhaar number")
    found = AADHAAR_DB.get(raw)
    if found:
        return {"status": "found", "data": found, "phone_tail": found["phone"][-4:]}
    # Generate fallback for unknown numbers
    names = ["Ramesh Kumar", "Sunita Devi", "Vijay Singh", "Ananya Sharma", "Mohan Das"]
    states = ["Tamil Nadu", "Maharashtra", "West Bengal", "Karnataka", "Delhi"]
    idx = int(raw[0]) % 5
    fallback = {
        "name": names[idx], "dob": "1990-01-01", "age": 35,
        "gender": "Male" if idx % 2 == 0 else "Female",
        "address": f"{raw[-3:]} MG Road, City", "pincode": "600001",
        "state": states[idx], "phone": "98" + raw[-8:],
        "occupation": "", "income": 0, "caste": "General",
    }
    return {"status": "generated", "data": fallback, "phone_tail": fallback["phone"][-4:]}


@app.post("/api/auth/verify-otp")
def verify_otp(req: OTPVerify):
    # Simulate OTP verification — any 4+ digit OTP passes
    if len(re.sub(r"\D", "", req.otp)) >= 4:
        return {"status": "verified", "message": "OTP verified successfully"}
    raise HTTPException(400, "Invalid OTP")


# ── Schemes ──
@app.get("/api/schemes")
def get_schemes(
    search: str = Query(""),
    category: str = Query(""),
    level: str = Query(""),
    limit: int = Query(50, le=200),
    offset: int = Query(0),
):
    schemes = load_schemes()
    q = search.lower()
    filtered = [
        s for s in schemes
        if (not q or q in s["name"].lower() or q in s["category"].lower()
            or q in " ".join(s["tags"]).lower() or q in s["eligibility"].lower())
        and (not category or category.lower() in s["category"].lower())
        and (not level or s["level"].lower() == level.lower())
    ]
    total = len(filtered)
    return {
        "total": total,
        "offset": offset,
        "limit": limit,
        "results": filtered[offset : offset + limit],
    }


@app.get("/api/schemes/{scheme_id}")
def get_scheme(scheme_id: int):
    schemes = load_schemes()
    s = next((x for x in schemes if x["id"] == scheme_id), None)
    if not s:
        raise HTTPException(404, "Scheme not found")
    return s


@app.get("/api/categories")
def get_categories():
    schemes = load_schemes()
    cats = set()
    for s in schemes:
        for c in s["category"].split(","):
            c = c.strip()
            if c:
                cats.add(c)
    return sorted(cats)


# ── Match ──
@app.post("/api/match")
def match_schemes(req: MatchRequest):
    schemes = load_schemes()
    q = req.search.lower()

    filtered = [
        s for s in schemes
        if (not q or q in s["name"].lower() or q in s["category"].lower()
            or q in " ".join(s["tags"]).lower())
        and (not req.category or req.category.lower() in s["category"].lower())
    ]

    # Score each scheme
    scored = []
    for s in filtered:
        e = elig_score(s, req.profile)
        scored.append({**s, "eligibility_status": e})

    # Sort: yes → maybe → no
    order = {"yes": 0, "maybe": 1, "no": 2}
    scored.sort(key=lambda x: order.get(x["eligibility_status"], 2))

    total = len(scored)
    results = scored[req.offset : req.offset + req.limit]
    eligible_count = sum(1 for s in scored if s["eligibility_status"] == "yes")

    return {
        "total": total,
        "eligible_count": eligible_count,
        "offset": req.offset,
        "limit": req.limit,
        "results": results,
    }


# ── AI Explain (Ollama · qwen3:8b) ──
@app.post("/api/ai/explain")
async def ai_explain(req: AIRequest):
    schemes = load_schemes()
    s = next((x for x in schemes if x["id"] == req.scheme_id), None)
    if not s:
        raise HTTPException(404, "Scheme not found")

    p = req.profile
    prompt = (
        f"You are a helpful assistant for rural Indian citizens. "
        f"Explain this government scheme in 2-3 simple sentences in plain English (no jargon). "
        f"Scheme: {s['name']}. "
        f"Benefit: {s['benefit']}. "
        f"Eligibility: {s['eligibility'][:200]}. "
        f"User: Age {p.age}, {p.gender}, {p.occupation}, {p.state}, Caste {p.caste}. "
        f"Also say in 1 line if this person likely qualifies. "
        f"Reply only with the explanation, no headings."
    )

    try:
        async with httpx.AsyncClient(timeout=30) as client:
            resp = await client.post(
                "http://localhost:11434/api/generate",
                json={"model": "qwen3:8b", "prompt": prompt, "stream": False},
            )
            resp.raise_for_status()
            data = resp.json()
            text = data.get("response", "")
            # Strip <think> blocks from qwen3
            text = re.sub(r"<think>.*?</think>", "", text, flags=re.DOTALL).strip()
            return {"summary": text, "model": "qwen3:8b"}
    except httpx.ConnectError:
        return {
            "summary": "⚠ Ollama not running. Start with: ollama run qwen3:8b",
            "model": "offline",
        }
    except Exception as e:
        return {"summary": f"AI unavailable: {str(e)}", "model": "error"}
