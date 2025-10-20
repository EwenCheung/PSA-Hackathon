import { apiClient } from './apiClient';

export interface WellbeingMessage {
  sender: 'user' | 'ai';
  content: string;
  timestamp: string;
  isAnonymous: boolean;
  anonSessionId: string | null;
}

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
  const data = await apiClient.get<any[]>(
    `/api/v1/wellbeing/${employeeId}/messages_past_10_history`
  );
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
  const payload = await apiClient.post<any>(
    `/api/v1/wellbeing/${employeeId}/messages`,
    {
      message: content,
      is_anonymous: options.isAnonymous,
      isAnonymous: options.isAnonymous,
      anon_session_id: options.anonSessionId,
      anonSessionId: options.anonSessionId,
    }
  );
  return deserializeMessage(payload);
};
