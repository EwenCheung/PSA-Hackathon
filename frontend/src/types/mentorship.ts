import type { EmployeeDirectoryEntry } from './employee';

export interface MentorMatch {
  mentee_id: string;
  mentor_id: string;
  match_score: number;
  explanation: string;
  status: string;
  created_at: string;
}

export interface CreateMentorMatchPayload {
  mentee_id: string;
  mentor_id: string;
}

export interface MentorshipBrowseData {
  mentors: EmployeeDirectoryEntry[];
  mentees: EmployeeDirectoryEntry[];
}
