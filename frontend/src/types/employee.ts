export interface EmployeeProfile {
  id: string;
  name: string;
  role: string | null;
  department_id: string | null;
  level: string | null;
  position_level: number | null;
  points_current: number;
  hire_date: string | null;
}

export interface EmployeeSession {
  issued_at: string;
}

export interface EmployeeLoginSuccess {
  employee: EmployeeProfile;
  session: EmployeeSession;
}

export interface EmployeeDirectoryEntry extends EmployeeProfile {
  skills?: Record<string, number>;
  goals?: string[];
  courses_enrolled?: Record<string, string>;
}
