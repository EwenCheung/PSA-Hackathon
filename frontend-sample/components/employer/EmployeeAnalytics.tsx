import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '../ui/card';
import { Badge } from '../ui/badge';
import { Progress } from '../ui/progress';
import { 
  Users, TrendingUp, Award, AlertTriangle, 
  CheckCircle2, Clock, Target, Smile, Meh, Frown 
} from 'lucide-react';

const employeeData = [
  {
    id: 'EMP001',
    name: 'Alex Johnson',
    role: 'Software Developer',
    department: 'Engineering',
    coursesCompleted: 3,
    coursesInProgress: 1,
    points: 1250,
    sentiment: 'positive',
    lastActive: '2 hours ago',
    careerProgress: 65,
  },
  {
    id: 'EMP002',
    name: 'Sarah Chen',
    role: 'Product Manager',
    department: 'Product',
    coursesCompleted: 5,
    coursesInProgress: 2,
    points: 1800,
    sentiment: 'neutral',
    lastActive: '1 day ago',
    careerProgress: 80,
  },
  {
    id: 'EMP003',
    name: 'Michael Brown',
    role: 'Designer',
    department: 'Design',
    coursesCompleted: 2,
    coursesInProgress: 1,
    points: 850,
    sentiment: 'negative',
    lastActive: '3 hours ago',
    careerProgress: 45,
  },
  {
    id: 'EMP004',
    name: 'Emily Davis',
    role: 'Data Analyst',
    department: 'Analytics',
    coursesCompleted: 4,
    coursesInProgress: 2,
    points: 1500,
    sentiment: 'positive',
    lastActive: '30 minutes ago',
    careerProgress: 70,
  },
];

const departmentStats = [
  { name: 'Engineering', employees: 45, avgProgress: 68, sentiment: 'positive' },
  { name: 'Product', employees: 20, avgProgress: 72, sentiment: 'positive' },
  { name: 'Design', employees: 15, avgProgress: 58, sentiment: 'neutral' },
  { name: 'Analytics', employees: 12, avgProgress: 75, sentiment: 'positive' },
  { name: 'Marketing', employees: 18, avgProgress: 62, sentiment: 'neutral' },
];

export default function EmployeeAnalytics() {
  const getSentimentIcon = (sentiment: string) => {
    switch (sentiment) {
      case 'positive':
        return <Smile className="w-4 h-4 text-green-600" />;
      case 'negative':
        return <Frown className="w-4 h-4 text-red-600" />;
      default:
        return <Meh className="w-4 h-4 text-gray-600" />;
    }
  };

  const getSentimentBadge = (sentiment: string) => {
    const colors = {
      positive: 'bg-green-50 text-green-700 border-green-200',
      negative: 'bg-red-50 text-red-700 border-red-200',
      neutral: 'bg-[#DEF0F9] text-[#1B1F23] border-[#D0E8F5]',
    };
    return colors[sentiment as keyof typeof colors] || colors.neutral;
  };

  return (
    <div className="space-y-6">
      {/* Overview Stats */}
      <div className="grid md:grid-cols-4 gap-4">
        <Card className="border border-[#D0E8F5]">
          <CardHeader className="pb-3">
            <CardTitle className="text-sm text-muted-foreground flex items-center gap-2">
              <Users className="w-4 h-4" />
              Total Employees
            </CardTitle>
          </CardHeader>
          <CardContent>
            <div className="text-3xl text-foreground">110</div>
            <p className="text-sm text-muted-foreground">Across 5 departments</p>
          </CardContent>
        </Card>

        <Card className="border border-[#D0E8F5]">
          <CardHeader className="pb-3">
            <CardTitle className="text-sm text-muted-foreground flex items-center gap-2">
              <CheckCircle2 className="w-4 h-4" />
              Courses Completed
            </CardTitle>
          </CardHeader>
          <CardContent>
            <div className="text-3xl text-foreground">342</div>
            <p className="text-sm text-green-600">↑ 12% this month</p>
          </CardContent>
        </Card>

        <Card className="border border-[#D0E8F5]">
          <CardHeader className="pb-3">
            <CardTitle className="text-sm text-muted-foreground flex items-center gap-2">
              <TrendingUp className="w-4 h-4" />
              Avg Career Progress
            </CardTitle>
          </CardHeader>
          <CardContent>
            <div className="text-3xl text-foreground">67%</div>
            <p className="text-sm text-muted-foreground">Company-wide average</p>
          </CardContent>
        </Card>

        <Card className="border border-[#D0E8F5]">
          <CardHeader className="pb-3">
            <CardTitle className="text-sm text-muted-foreground flex items-center gap-2">
              <AlertTriangle className="w-4 h-4" />
              Needs Attention
            </CardTitle>
          </CardHeader>
          <CardContent>
            <div className="text-3xl text-foreground">8</div>
            <p className="text-sm text-secondary">Low sentiment detected</p>
          </CardContent>
        </Card>
      </div>

      {/* Department Overview */}
      <Card className="border border-[#D0E8F5]">
        <CardHeader className="border-b border-[#E8F3F9]">
          <CardTitle>Department Overview</CardTitle>
          <CardDescription>Performance and sentiment across departments</CardDescription>
        </CardHeader>
        <CardContent>
          <div className="space-y-4">
            {departmentStats.map((dept) => (
              <div key={dept.name} className="space-y-2">
                <div className="flex items-center justify-between">
                  <div className="flex items-center gap-3">
                    <span>{dept.name}</span>
                    <Badge variant="outline">{dept.employees} employees</Badge>
                    <Badge className={getSentimentBadge(dept.sentiment)} variant="secondary">
                      {dept.sentiment}
                    </Badge>
                  </div>
                  <span className="text-sm">{dept.avgProgress}%</span>
                </div>
                <Progress value={dept.avgProgress} />
              </div>
            ))}
          </div>
        </CardContent>
      </Card>

      {/* Employee Details */}
      <Card className="border border-[#D0E8F5]">
        <CardHeader className="border-b border-[#E8F3F9]">
          <CardTitle>Employee Details</CardTitle>
          <CardDescription>Individual progress and wellbeing indicators</CardDescription>
        </CardHeader>
        <CardContent className="pt-6">
          <div className="space-y-4">
            {employeeData.map((employee) => (
              <Card key={employee.id} className="border border-[#D0E8F5]">
                <CardContent className="pt-6">
                  <div className="flex items-start justify-between mb-4">
                    <div>
                      <div className="flex items-center gap-2 mb-1">
                        <h3 className="text-lg">{employee.name}</h3>
                        {employee.sentiment === 'negative' && (
                          <Badge variant="destructive" className="gap-1">
                            <AlertTriangle className="w-3 h-3" />
                            Needs Support
                          </Badge>
                        )}
                      </div>
                      <p className="text-sm text-gray-600">
                        {employee.role} • {employee.department} • {employee.id}
                      </p>
                    </div>
                    <div className="flex items-center gap-4 text-sm">
                      <div className="text-right">
                        <p className="text-gray-600">Points</p>
                        <p>{employee.points}</p>
                      </div>
                      <div className="text-right">
                        <p className="text-gray-600">Sentiment</p>
                        <div className="flex items-center gap-1 justify-end">
                          {getSentimentIcon(employee.sentiment)}
                        </div>
                      </div>
                    </div>
                  </div>

                  <div className="grid grid-cols-3 gap-4 mb-4 text-sm">
                    <div className="flex items-center gap-2">
                      <CheckCircle2 className="w-4 h-4 text-green-600" />
                      <div>
                        <p className="text-gray-600">Completed</p>
                        <p>{employee.coursesCompleted} courses</p>
                      </div>
                    </div>
                    <div className="flex items-center gap-2">
                      <Clock className="w-4 h-4 text-[#4167B1]" />
                      <div>
                        <p className="text-gray-600">In Progress</p>
                        <p>{employee.coursesInProgress} courses</p>
                      </div>
                    </div>
                    <div className="flex items-center gap-2">
                      <Target className="w-4 h-4 text-purple-600" />
                      <div>
                        <p className="text-gray-600">Last Active</p>
                        <p>{employee.lastActive}</p>
                      </div>
                    </div>
                  </div>

                  <div className="space-y-2">
                    <div className="flex items-center justify-between text-sm">
                      <span className="text-gray-600">Career Progress</span>
                      <span>{employee.careerProgress}%</span>
                    </div>
                    <Progress value={employee.careerProgress} />
                  </div>
                </CardContent>
              </Card>
            ))}
          </div>
        </CardContent>
      </Card>
    </div>
  );
}
