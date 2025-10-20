// Mentoring API Service
// This file provides functions to interact with the mentoring backend API

const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';

// Types matching backend schemas
export interface MentorProfile {
  employeeId: string;
  name: string;
  role: string;
  department: string;
  expertiseAreas: string[];
  rating: number;
  menteesCount: number;
  maxMentees: number;
  isAvailable: boolean;
  bio: string;
  yearsOfExperience: number;
  achievements: string[];
}

export interface MentorRecommendation {
  mentorId: string;
  mentorName: string;
  role: string;
  matchScore: number;
  reason: string;
  focusAreas: string[];
}

export interface MentorshipRequest {
  requestId: string;
  menteeId: string;
  menteeName: string;
  menteeRole: string;
  mentorId: string;
  mentorName: string;
  message: string;
  goals: string[];
  status: 'pending' | 'accepted' | 'declined';
  createdAt: string;
  respondedAt?: string | null;
}

export interface MentorshipPair {
  pairId: string;
  mentorId: string;
  mentorName: string;
  mentorRole: string;
  menteeId: string;
  menteeName: string;
  menteeRole: string;
  startDate: string;
  focusAreas: string[];
  status: string;
  progressPercentage: number;
  sessionsCompleted: number;
  lastMeetingDate: string | null;
  nextMeetingDate: string | null;
}

export interface MentorshipStatistics {
  totalActivePairs: number;
  totalMentors: number;
  totalMenteesSeeking: number;
  availableMentors: number;
  averageMatchScore: number;
  completionRate: number;
  underservedSkills: string[];
}

// API Functions

export interface FetchMentorsOptions {
  skillArea?: string;
  department?: string;
  menteeId?: string;
}

export async function fetchMentors(
  options: FetchMentorsOptions = {}
): Promise<MentorProfile[]> {
  const params = new URLSearchParams();
  if (options.skillArea) params.append('skill_area', options.skillArea);
  if (options.department) params.append('department', options.department);
  if (options.menteeId) params.append('mentee_id', options.menteeId);

  const query = params.toString();
  const url = query
    ? `${API_BASE_URL}/api/v1/mentoring/mentors?${query}`
    : `${API_BASE_URL}/api/v1/mentoring/mentors`;
  const response = await fetch(url);
  
  if (!response.ok) {
    throw new Error('Failed to fetch mentors');
  }
  
  return response.json();
}

export async function fetchMentorById(employeeId: string): Promise<MentorProfile> {
  const url = `${API_BASE_URL}/api/v1/mentoring/mentors/${employeeId}`;
  const response = await fetch(url);
  
  if (!response.ok) {
    throw new Error('Mentor not found');
  }
  
  return response.json();
}

export async function getMentorRecommendations(
  employeeId: string,
  careerGoals: string[],
  desiredSkills: string[],
  maxResults: number = 5
): Promise<MentorRecommendation[]> {
  const url = `${API_BASE_URL}/api/v1/mentoring/recommend`;
  const response = await fetch(url, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({
      employeeId,
      careerGoals,
      desiredSkills,
      maxResults,
    }),
  });
  
  if (!response.ok) {
    throw new Error('Failed to get recommendations');
  }
  
  return response.json();
}

export async function createMentorshipRequest(
  menteeId: string,
  mentorId: string,
  message: string,
  goals: string[]
): Promise<MentorshipRequest> {
  const url = `${API_BASE_URL}/api/v1/mentoring/request`;
  const response = await fetch(url, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({
      menteeId,
      mentorId,
      message,
      goals,
    }),
  });
  
  if (!response.ok) {
    throw new Error('Failed to create mentorship request');
  }
  
  return response.json();
}

export async function fetchMentorshipRequests(
  mentorId?: string,
  menteeId?: string
): Promise<MentorshipRequest[]> {
  const params = new URLSearchParams();
  if (mentorId) params.append('mentor_id', mentorId);
  if (menteeId) params.append('mentee_id', menteeId);
  
  const url = `${API_BASE_URL}/api/v1/mentoring/requests?${params}`;
  const response = await fetch(url);
  
  if (!response.ok) {
    throw new Error('Failed to fetch requests');
  }
  
  return response.json();
}

export async function updateMentorshipRequest(
  requestId: string,
  status: 'accepted' | 'declined',
  responseMessage?: string
): Promise<MentorshipRequest> {
  const url = `${API_BASE_URL}/api/v1/mentoring/requests/${requestId}`;
  const response = await fetch(url, {
    method: 'PUT',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({
      status,
      responseMessage,
    }),
  });
  
  if (!response.ok) {
    throw new Error('Failed to update request');
  }
  
  return response.json();
}

export async function fetchMentorshipPairs(
  mentorId?: string,
  menteeId?: string
): Promise<MentorshipPair[]> {
  const params = new URLSearchParams();
  if (mentorId) params.append('mentor_id', mentorId);
  if (menteeId) params.append('mentee_id', menteeId);
  
  const url = `${API_BASE_URL}/api/v1/mentoring/pairs?${params}`;
  const response = await fetch(url);
  
  if (!response.ok) {
    throw new Error('Failed to fetch pairs');
  }
  
  return response.json();
}

export async function fetchMentorshipStatistics(): Promise<MentorshipStatistics> {
  const url = `${API_BASE_URL}/api/v1/mentoring/statistics`;
  const response = await fetch(url);
  
  if (!response.ok) {
    throw new Error('Failed to fetch statistics');
  }
  
  return response.json();
}

export async function deleteMentorshipRequest(
  requestId: string,
  menteeId: string
): Promise<void> {
  const params = new URLSearchParams();
  params.append('mentee_id', menteeId);

  const url = `${API_BASE_URL}/api/v1/mentoring/requests/${requestId}?${params}`;
  const response = await fetch(url, {
    method: 'DELETE',
  });

  if (!response.ok) {
    const message = await response.text();
    throw new Error(message || 'Failed to delete mentorship request');
  }
}
