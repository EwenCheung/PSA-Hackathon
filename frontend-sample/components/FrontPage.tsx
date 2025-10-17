import { useState } from 'react';
import { Button } from './ui/button';
import { Input } from './ui/input';
import { Label } from './ui/label';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from './ui/card';
import { Briefcase, Users } from 'lucide-react';

interface FrontPageProps {
  onLogin: (type: 'employee' | 'employer', id?: string) => void;
}

export default function FrontPage({ onLogin }: FrontPageProps) {
  const [employeeId, setEmployeeId] = useState('');

  const handleEmployeeLogin = () => {
    if (employeeId.trim()) {
      onLogin('employee', employeeId);
    }
  };

  return (
    <div className="min-h-screen bg-background flex items-center justify-center p-4">
      <div className="w-full max-w-6xl">
        <div className="text-center mb-12">
          <h1 className="text-4xl mb-3 text-foreground">Employee Growth Platform</h1>
          <p className="text-muted-foreground">
            Empowering careers, supporting wellbeing, building connections
          </p>
        </div>

        <div className="grid md:grid-cols-2 gap-8">
          {/* Employee Login */}
          <Card className="border border-[#D0E8F5] hover:border-[#4167B1]/50 transition-colors">
            <CardHeader className="text-center">
              <div className="mx-auto mb-4 w-14 h-14 bg-[#DEF0F9] rounded-lg flex items-center justify-center">
                <Users className="w-7 h-7 text-[#4167B1]" />
              </div>
              <CardTitle>Employee Portal</CardTitle>
              <CardDescription>
                Access your career path, wellbeing support, and rewards
              </CardDescription>
            </CardHeader>
            <CardContent className="space-y-4">
              <div className="space-y-2">
                <Label htmlFor="employee-id" className="text-sm">Employee ID</Label>
                <Input
                  id="employee-id"
                  placeholder="e.g., EMP001"
                  value={employeeId}
                  onChange={(e) => setEmployeeId(e.target.value)}
                  onKeyPress={(e) => e.key === 'Enter' && handleEmployeeLogin()}
                  className="border-2 border-[#4167B1]/30 focus-visible:border-[#4167B1] focus-visible:ring-[#4167B1]/20 h-12 text-base"
                />
              </div>
              <Button 
                className="w-full" 
                size="lg"
                onClick={handleEmployeeLogin}
              >
                Login as Employee
              </Button>
              <p className="text-xs text-muted-foreground text-center">
                No password required - use your employee ID
              </p>
            </CardContent>
          </Card>

          {/* Employer Access */}
          <Card className="border border-[#D0E8F5] hover:border-[#4167B1]/50 transition-colors">
            <CardHeader className="text-center">
              <div className="mx-auto mb-4 w-14 h-14 bg-[#DEF0F9] rounded-lg flex items-center justify-center">
                <Briefcase className="w-7 h-7 text-[#4167B1]" />
              </div>
              <CardTitle>Employer Dashboard</CardTitle>
              <CardDescription>
                View analytics, insights, and manage mentor matching
              </CardDescription>
            </CardHeader>
            <CardContent className="space-y-4">
              <div className="space-y-2 text-sm text-muted-foreground py-4">
                <p>✓ Company potential analysis</p>
                <p>✓ Employee growth tracking</p>
                <p>✓ Mentor-mentee matching</p>
                <p>✓ Sentiment insights</p>
              </div>
              <Button 
                className="w-full" 
                size="lg"
                onClick={() => onLogin('employer')}
              >
                Access Employer Dashboard
              </Button>
              <p className="text-xs text-muted-foreground text-center">
                No login required
              </p>
            </CardContent>
          </Card>
        </div>
      </div>
    </div>
  );
}
