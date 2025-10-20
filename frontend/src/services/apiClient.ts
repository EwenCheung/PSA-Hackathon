const API_BASE = import.meta.env.VITE_API_BASE_URL ?? 'http://localhost:8000';

export class ApiError extends Error {
  status: number;

  constructor(message: string, status: number) {
    super(message);
    this.status = status;
  }
}

async function request<T>(path: string, init?: RequestInit): Promise<T> {
  const response = await fetch(`${API_BASE}${path}`, {
    headers: {
      'Content-Type': 'application/json',
      ...init?.headers,
    },
    ...init,
  });

  if (!response.ok) {
    let message = `Request failed with status ${response.status}`;
    const contentType = response.headers.get('content-type');
    if (contentType && contentType.includes('application/json')) {
      try {
        const body = await response.json();
        message = body?.detail || JSON.stringify(body);
      } catch (error) {
        message = await response.text();
      }
    } else {
      message = await response.text();
    }
    throw new ApiError(message || `Request failed with status ${response.status}`, response.status);
  }

  if (response.status === 204) {
    return undefined as T;
  }

  return (await response.json()) as T;
}

export const apiClient = {
  get<T>(path: string): Promise<T> {
    return request<T>(path, { method: 'GET' });
  },
  post<T>(path: string, body: unknown): Promise<T> {
    return request<T>(path, { method: 'POST', body: JSON.stringify(body) });
  },
  delete(path: string): Promise<void> {
    return request<void>(path, { method: 'DELETE' });
  },
};

export { API_BASE };
