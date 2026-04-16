// Opportunity OS — API Service (Mobile)
// Points to the shared FastAPI backend

const API_BASE = process.env.EXPO_PUBLIC_API_URL || 'http://10.0.2.2:8000';

export const api = {
  async verifyAadhaar(aadhaar) {
    return _post('/api/auth/verify-aadhaar', { aadhaar });
  },
  async verifyOTP(aadhaar, otp) {
    return _post('/api/auth/verify-otp', { aadhaar, otp });
  },
  async match(profile, opts = {}) {
    return _post('/api/match', {
      profile,
      limit: opts.limit || 30,
      offset: opts.offset || 0,
      category: opts.category || '',
      search: opts.search || '',
    });
  },
  async getScheme(id) {
    return _get(`/api/schemes/${id}`);
  },
  async getCategories() {
    return _get('/api/categories');
  },
  async explain(schemeId, profile) {
    return _post('/api/ai/explain', { scheme_id: schemeId, profile });
  },
  async health() {
    return _get('/api/health');
  },
};

async function _get(path) {
  const r = await fetch(API_BASE + path);
  if (!r.ok) throw new Error(`API error ${r.status}`);
  return r.json();
}

async function _post(path, body) {
  const r = await fetch(API_BASE + path, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(body),
  });
  if (!r.ok) {
    const err = await r.json().catch(() => ({}));
    throw new Error(err.detail || `API error ${r.status}`);
  }
  return r.json();
}
