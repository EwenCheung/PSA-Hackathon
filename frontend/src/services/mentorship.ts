import { apiClient, ApiError } from './apiClient';
import type {
  MentorMatch,
  CreateMentorMatchPayload,
} from '../types/mentorship';
import type { EmployeeDirectoryEntry } from '../types/employee';

export const fetchMentors = (): Promise<EmployeeDirectoryEntry[]> => {
  return apiClient.get<EmployeeDirectoryEntry[]>('/api/v1/matching/mentors');
};

export const fetchMentees = (): Promise<EmployeeDirectoryEntry[]> => {
  return apiClient.get<EmployeeDirectoryEntry[]>('/api/v1/matching/mentees');
};

export const fetchMentorMatch = async (menteeId: string): Promise<MentorMatch | null> => {
  try {
    return await apiClient.get<MentorMatch>(`/api/v1/matching/request/${menteeId}`);
  } catch (error) {
    if (error instanceof ApiError && error.status === 404) {
      return null;
    }
    throw error;
  }
};

export const applyForMentor = (payload: CreateMentorMatchPayload): Promise<MentorMatch> => {
  return apiClient.post<MentorMatch>('/api/v1/matching/request', payload);
};

export const cancelMentorMatch = (menteeId: string): Promise<void> => {
  return apiClient.delete(`/api/v1/matching/request/${menteeId}`);
};
