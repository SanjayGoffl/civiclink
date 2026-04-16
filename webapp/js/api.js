// Opportunity OS — API Service
// All calls go to the single FastAPI backend

const API_BASE = window.location.hostname === 'localhost' || window.location.hostname === '127.0.0.1' 
  ? 'http://localhost:8000' 
  : ''; // Use relative path in production

const api = {
  // Auth
  async verifyAadhaar(aadhaar) {
    return _post('/api/auth/verify-aadhaar', { aadhaar });
  },
  async verifyOTP(aadhaar, otp) {
    return _post('/api/auth/verify-otp', { aadhaar, otp });
  },

  // Schemes
  async getSchemes({ search = '', category = '', level = '', limit = 50, offset = 0 } = {}) {
    const p = new URLSearchParams({ search, category, level, limit, offset });
    return _get(`/api/schemes?${p}`);
  },
  async getScheme(id) {
    return _get(`/api/schemes/${id}`);
  },
  async getCategories() {
    return _get('/api/categories');
  },

  // Match (personalized)
  async match(profile, { limit = 50, offset = 0, category = '', search = '' } = {}) {
    return _post('/api/match', { profile, limit, offset, category, search });
  },

  // AI
  async explain(schemeId, profile) {
    return _post('/api/ai/explain', { scheme_id: schemeId, profile });
  },

  // Health check
  async health() { return _get('/api/health'); }
};

async function _get(path) {
  try {
    const r = await fetch(API_BASE + path);
    if (!r.ok) throw new Error(`${r.status} ${r.statusText}`);
    return await r.json();
  } catch (e) {
    throw new Error('Cannot reach backend. Is it running on port 8000?');
  }
}

async function _post(path, body) {
  try {
    const r = await fetch(API_BASE + path, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(body),
    });
    if (!r.ok) {
      const err = await r.json().catch(() => ({}));
      throw new Error(err.detail || `${r.status}`);
    }
    return await r.json();
  } catch (e) {
    if (e.message.includes('fetch')) throw new Error('Backend not reachable at port 8000');
    throw e;
  }
}

// Profile helpers
const Profile = {
  save(p) { localStorage.setItem('oos_profile', JSON.stringify(p)); },
  load() {
    try { return JSON.parse(localStorage.getItem('oos_profile')); }
    catch { return null; }
  },
  clear() { localStorage.removeItem('oos_profile'); }
};

// Toast notification
function toast(msg, type = 'info') {
  const el = document.getElementById('toast');
  if (!el) return;
  el.textContent = msg;
  el.className = `toast toast-${type} show`;
  setTimeout(() => el.classList.remove('show'), 3000);
}
