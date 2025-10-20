import { useState } from 'react';
import FrontPage from './components/FrontPage';
import EmployeeDashboard from './components/employee/EmployeeDashboard';
import EmployerDashboard from './components/employer/EmployerDashboard';
import type { EmployeeLoginSuccess } from './src/types/employee';

export default function App() {
  const [userType, setUserType] = useState<'employee' | 'employer' | null>(null);
  const [employeeLogin, setEmployeeLogin] = useState<EmployeeLoginSuccess | null>(null);

  const handleEmployeeAuthenticated = (payload: EmployeeLoginSuccess) => {
    setUserType('employee');
    setEmployeeLogin(payload);
  };

  const handleEmployerSelected = () => {
    setUserType('employer');
  };

  const handleLogout = () => {
    setUserType(null);
    setEmployeeLogin(null);
  };

  if (!userType) {
    return (
      <FrontPage
        onEmployeeAuthenticated={handleEmployeeAuthenticated}
        onEmployerSelected={handleEmployerSelected}
      />
    );
  }

  if (userType === 'employee') {
    if (!employeeLogin) {
      return null;
    }

    return (
      <EmployeeDashboard
        employee={employeeLogin.employee}
        session={employeeLogin.session}
        onLogout={handleLogout}
      />
    );
  }

  return <EmployerDashboard onLogout={handleLogout} />;
}
