// CivicLink — External Configuration
// This file acts as a bridge for environment variables in static HTML
window.CIVIC_CONFIG = {
  // Replace with your actual Groq API key
  GROQ_API_KEY: "YOUR_GROQ_API_KEY_HERE",
  
  // Backend API Base (if using the FastAPI backend)
  API_BASE: "http://localhost:8000",
  
  // Ollama Configuration (Local AI)
  OLLAMA_URL: "http://localhost:11434/api/generate",
  OLLAMA_MODEL: "qwen3:8b"
};
