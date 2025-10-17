import { useState } from 'react';
import FrontPage from './components/FrontPage';
import EmployeeDashboard from './components/employee/EmployeeDashboard';
import EmployerDashboard from './components/employer/EmployerDashboard';

export default function App() {
  const [userType, setUserType] = useState<'employee' | 'employer' | null>(null);
  const [employeeId, setEmployeeId] = useState<string>('');

  const handleLogin = (type: 'employee' | 'employer', id?: string) => {
    setUserType(type);
    if (id) setEmployeeId(id);
  };

  const handleLogout = () => {
    setUserType(null);
    setEmployeeId('');
  };

  if (!userType) {
    return <FrontPage onLogin={handleLogin} />;
  }

  if (userType === 'employee') {
    return <EmployeeDashboard employeeId={employeeId} onLogout={handleLogout} />;
  }

  return <EmployerDashboard onLogout={handleLogout} />;
}
