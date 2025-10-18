import { useState } from 'react';
import { Tabs, TabsContent, TabsList, TabsTrigger } from '../ui/tabs';
import { Button } from '../ui/button';
import { LogOut, GraduationCap, MessageCircle, ShoppingBag, User } from 'lucide-react';
import CareerPath from './CareerPath';
import ChatSupport from './ChatSupport';
import Marketplace from './Marketplace';
import { Badge } from '../ui/badge';

interface EmployeeDashboardProps {
  employeeId: string;
  onLogout: () => void;
}

// Mock employee data
const mockEmployeeData = {
  name: 'Alex Johnson',
  role: 'Software Developer',
  department: 'Engineering',
  points: 1250,
  level: 'Mid-Level',
  joinDate: '2023-01-15',
};

export default function EmployeeDashboard({ employeeId, onLogout }: EmployeeDashboardProps) {
  const [currentTab, setCurrentTab] = useState('career');
  const [points, setPoints] = useState(mockEmployeeData.points);

  const handlePointsUpdate = (newPoints: number) => {
    setPoints(newPoints);
  };

  return (
    <div className="min-h-screen bg-background">
      {/* Header */}
      <header className="bg-card border-b sticky top-0 z-10">
        <div className="container mx-auto px-4 py-4">
          <div className="flex items-center justify-between">
            <div className="flex items-center gap-4">
              <div className="w-10 h-10 bg-[#4167B1] rounded-full flex items-center justify-center">
                <User className="w-6 h-6 text-white" />
              </div>
              <div>
                <h1 className="text-xl">{mockEmployeeData.name}</h1>
                <p className="text-sm text-gray-600">
                  {mockEmployeeData.role} • ID: {employeeId}
                </p>
              </div>
            </div>
            <div className="flex items-center gap-4">
              <div className="text-right">
                <p className="text-sm text-gray-600">Your Points</p>
                <Badge variant="secondary" className="text-lg">
                  {points} pts
                </Badge>
              </div>
              <Button variant="outline" onClick={onLogout}>
                <LogOut className="w-4 h-4 mr-2" />
                Logout
              </Button>
            </div>
          </div>
        </div>
      </header>

      {/* Main Content */}
      <div className="container mx-auto px-4 py-8">
        <Tabs value={currentTab} onValueChange={setCurrentTab} className="space-y-6">
          <TabsList className="grid w-full grid-cols-3 max-w-2xl mx-auto">
            <TabsTrigger value="career" className="gap-2">
              <GraduationCap className="w-4 h-4" />
              Career Path
            </TabsTrigger>
            <TabsTrigger value="wellbeing" className="gap-2">
              <MessageCircle className="w-4 h-4" />
              Wellbeing Support
            </TabsTrigger>
            <TabsTrigger value="marketplace" className="gap-2">
              <ShoppingBag className="w-4 h-4" />
              Marketplace
            </TabsTrigger>
          </TabsList>

          <TabsContent value="career">
            <CareerPath 
              employeeId={employeeId} 
              employeeData={mockEmployeeData}
              points={points}
              onPointsUpdate={handlePointsUpdate}
            />
          </TabsContent>

          <TabsContent value="wellbeing">
            <ChatSupport employeeId={employeeId} />
          </TabsContent>

          <TabsContent value="marketplace">
            <Marketplace points={points} onPointsUpdate={handlePointsUpdate} />
          </TabsContent>
        </Tabs>
      </div>
    </div>
  );
}
