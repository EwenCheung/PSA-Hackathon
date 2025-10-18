const normalizeBaseUrl = (value?: string) => {
  if (!value) return 'http://localhost:8000';
  return value.endsWith('/') ? value.slice(0, -1) : value;
};

export const API_BASE_URL = normalizeBaseUrl(import.meta.env.VITE_BACKEND_BASE_URL);
