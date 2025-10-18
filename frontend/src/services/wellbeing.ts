const API_BASE = import.meta.env.VITE_API_BASE_URL ?? 'http://localhost:8000';

export interface WellbeingMessage {
  sender: 'user' | 'ai';
  content: string;
  timestamp: string;
  isAnonymous: boolean;
  anonSessionId: string | null;
}

const withBase = (path: string) => `${API_BASE}${path}`;

const deserializeMessage = (payload: any): WellbeingMessage => {
  const rawSender = typeof payload?.sender === 'string' ? payload.sender : 'ai';
  const normalizedSender: 'user' | 'ai' = rawSender === 'user' ? 'user' : 'ai';

  return {
    sender: normalizedSender,
    content: payload?.content ?? '',
    timestamp: typeof payload?.timestamp === 'string' ? payload.timestamp : new Date().toISOString(),
    isAnonymous: Boolean(payload?.is_anonymous ?? payload?.isAnonymous),
    anonSessionId: payload?.anon_session_id ?? payload?.anonSessionId ?? null,
  };
};

export const fetchWellbeingMessages = async (employeeId: string): Promise<WellbeingMessage[]> => {
  const response = await fetch(withBase(`/api/v1/wellbeing/${employeeId}/messages_past_10_history`));
  if (!response.ok) {
    throw new Error('Failed to load wellbeing messages');
  }
  const data = await response.json();
  return Array.isArray(data) ? data.map(deserializeMessage) : [];
};

interface SendOptions {
  isAnonymous: boolean;
  anonSessionId: string | null;
}

export const sendWellbeingMessage = async (
  employeeId: string,
  content: string,
  options: SendOptions,
): Promise<WellbeingMessage> => {
  const response = await fetch(withBase(`/api/v1/wellbeing/${employeeId}/messages`), {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({
      message: content,
      is_anonymous: options.isAnonymous,
      isAnonymous: options.isAnonymous,
      anon_session_id: options.anonSessionId,
      anonSessionId: options.anonSessionId,
    }),
  });

  if (!response.ok) {
    throw new Error('Failed to send wellbeing message');
  }

  const payload = await response.json();
  return deserializeMessage(payload);
};
