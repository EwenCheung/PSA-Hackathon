import { useState } from 'react';
import { Tabs, TabsContent, TabsList, TabsTrigger } from '../ui/tabs';
import { Button } from '../ui/button';
import { LogOut, BarChart3, Users, TrendingUp, GitMerge } from 'lucide-react';
import CompanyInsights from './CompanyInsights';
import MentorMatching from './MentorMatching';
import EmployeeAnalytics from './EmployeeAnalytics';

interface EmployerDashboardProps {
  onLogout: () => void;
}

export default function EmployerDashboard({ onLogout }: EmployerDashboardProps) {
  const [currentTab, setCurrentTab] = useState('analytics');

  return (
    <div className="min-h-screen bg-background">
      {/* Header */}
      <header className="bg-card border-b sticky top-0 z-10">
        <div className="container mx-auto px-4 py-4">
          <div className="flex items-center justify-between">
            <div>
              <h1 className="text-2xl">Employer Dashboard</h1>
              <p className="text-sm text-gray-600">
                Company-wide insights and employee growth management
              </p>
            </div>
            <Button variant="outline" onClick={onLogout}>
              <LogOut className="w-4 h-4 mr-2" />
              Logout
            </Button>
          </div>
        </div>
      </header>

      {/* Main Content */}
      <div className="container mx-auto px-4 py-8">
        <Tabs value={currentTab} onValueChange={setCurrentTab} className="space-y-6">
          <TabsList className="grid w-full grid-cols-3 max-w-2xl mx-auto">
            <TabsTrigger value="analytics" className="gap-2">
              <BarChart3 className="w-4 h-4" />
              Employee Analytics
            </TabsTrigger>
            <TabsTrigger value="insights" className="gap-2">
              <TrendingUp className="w-4 h-4" />
              Company Insights
            </TabsTrigger>
            <TabsTrigger value="matching" className="gap-2">
              <GitMerge className="w-4 h-4" />
              Mentor Matching
            </TabsTrigger>
          </TabsList>

          <TabsContent value="analytics">
            <EmployeeAnalytics />
          </TabsContent>

          <TabsContent value="insights">
            <CompanyInsights />
          </TabsContent>

          <TabsContent value="matching">
            <MentorMatching />
          </TabsContent>
        </Tabs>
      </div>
    </div>
  );
}
