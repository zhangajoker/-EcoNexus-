// Single source of truth for the backend address used by all views.
// VITE_API_BASE_URL comes from frontend/.env.development.
export const API_BASE = import.meta.env.VITE_API_BASE_URL || 'http://127.0.0.1:8000';
