import { apiClient } from './apiClient';
import type { EmployeeLoginSuccess } from '../types/employee';

export const loginEmployee = async (employeeId: string): Promise<EmployeeLoginSuccess> => {
  return apiClient.post<EmployeeLoginSuccess>('/api/v1/auth/employee-login', {
    employee_id: employeeId,
  });
};
