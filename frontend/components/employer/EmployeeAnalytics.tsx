// import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '../ui/card';
// import { Badge } from '../ui/badge';
// import { Progress } from '../ui/progress';
// import { 
//   Users, TrendingUp, Award, AlertTriangle, 
//   CheckCircle2, Clock, Target, Smile, Meh, Frown 
// } from 'lucide-react';

// const employeeData = [
//   {
//     id: 'EMP001',
//     name: 'Alex Johnson',
//     role: 'Software Developer',
//     department: 'Engineering',
//     coursesCompleted: 3,
//     coursesInProgress: 1,
//     points: 1250,
//     sentiment: 'positive',
//     lastActive: '2 hours ago',
//     careerProgress: 65,
//   },
//   {
//     id: 'EMP002',
//     name: 'Sarah Chen',
//     role: 'Product Manager',
//     department: 'Product',
//     coursesCompleted: 5,
//     coursesInProgress: 2,
//     points: 1800,
//     sentiment: 'neutral',
//     lastActive: '1 day ago',
//     careerProgress: 80,
//   },
//   {
//     id: 'EMP003',
//     name: 'Michael Brown',
//     role: 'Designer',
//     department: 'Design',
//     coursesCompleted: 2,
//     coursesInProgress: 1,
//     points: 850,
//     sentiment: 'negative',
//     lastActive: '3 hours ago',
//     careerProgress: 45,
//   },
//   {
//     id: 'EMP004',
//     name: 'Emily Davis',
//     role: 'Data Analyst',
//     department: 'Analytics',
//     coursesCompleted: 4,
//     coursesInProgress: 2,
//     points: 1500,
//     sentiment: 'positive',
//     lastActive: '30 minutes ago',
//     careerProgress: 70,
//   },
// ];

// const departmentStats = [
//   { name: 'Engineering', employees: 45, avgProgress: 68, sentiment: 'positive' },
//   { name: 'Product', employees: 20, avgProgress: 72, sentiment: 'positive' },
//   { name: 'Design', employees: 15, avgProgress: 58, sentiment: 'neutral' },
//   { name: 'Analytics', employees: 12, avgProgress: 75, sentiment: 'positive' },
//   { name: 'Marketing', employees: 18, avgProgress: 62, sentiment: 'neutral' },
// ];

// export default function EmployeeAnalytics() {
//   const getSentimentIcon = (sentiment: string) => {
//     switch (sentiment) {
//       case 'positive':
//         return <Smile className="w-4 h-4 text-green-600" />;
//       case 'negative':
//         return <Frown className="w-4 h-4 text-red-600" />;
//       default:
//         return <Meh className="w-4 h-4 text-gray-600" />;
//     }
//   };

//   const getSentimentBadge = (sentiment: string) => {
//     const colors = {
//       positive: 'bg-green-50 text-green-700 border-green-200',
//       negative: 'bg-red-50 text-red-700 border-red-200',
//       neutral: 'bg-[#DEF0F9] text-[#1B1F23] border-[#D0E8F5]',
//     };
//     return colors[sentiment as keyof typeof colors] || colors.neutral;
//   };

//   return (
//     <div className="space-y-6">
//       {/* Overview Stats */}
//       <div className="grid md:grid-cols-4 gap-4">
//         <Card className="border border-[#D0E8F5]">
//           <CardHeader className="pb-3">
//             <CardTitle className="text-sm text-muted-foreground flex items-center gap-2">
//               <Users className="w-4 h-4" />
//               Total Employees
//             </CardTitle>
//           </CardHeader>
//           <CardContent>
//             <div className="text-3xl text-foreground">110</div>
//             <p className="text-sm text-muted-foreground">Across 5 departments</p>
//           </CardContent>
//         </Card>

//         <Card className="border border-[#D0E8F5]">
//           <CardHeader className="pb-3">
//             <CardTitle className="text-sm text-muted-foreground flex items-center gap-2">
//               <CheckCircle2 className="w-4 h-4" />
//               Courses Completed
//             </CardTitle>
//           </CardHeader>
//           <CardContent>
//             <div className="text-3xl text-foreground">342</div>
//             <p className="text-sm text-green-600">↑ 12% this month</p>
//           </CardContent>
//         </Card>

//         <Card className="border border-[#D0E8F5]">
//           <CardHeader className="pb-3">
//             <CardTitle className="text-sm text-muted-foreground flex items-center gap-2">
//               <TrendingUp className="w-4 h-4" />
//               Avg Career Progress
//             </CardTitle>
//           </CardHeader>
//           <CardContent>
//             <div className="text-3xl text-foreground">67%</div>
//             <p className="text-sm text-muted-foreground">Company-wide average</p>
//           </CardContent>
//         </Card>

//         <Card className="border border-[#D0E8F5]">
//           <CardHeader className="pb-3">
//             <CardTitle className="text-sm text-muted-foreground flex items-center gap-2">
//               <AlertTriangle className="w-4 h-4" />
//               Needs Attention
//             </CardTitle>
//           </CardHeader>
//           <CardContent>
//             <div className="text-3xl text-foreground">8</div>
//             <p className="text-sm text-secondary">Low sentiment detected</p>
//           </CardContent>
//         </Card>
//       </div>

//       {/* Department Overview */}
//       <Card className="border border-[#D0E8F5]">
//         <CardHeader className="border-b border-[#E8F3F9]">
//           <CardTitle>Department Overview</CardTitle>
//           <CardDescription>Performance and sentiment across departments</CardDescription>
//         </CardHeader>
//         <CardContent>
//           <div className="space-y-4">
//             {departmentStats.map((dept) => (
//               <div key={dept.name} className="space-y-2">
//                 <div className="flex items-center justify-between">
//                   <div className="flex items-center gap-3">
//                     <span>{dept.name}</span>
//                     <Badge variant="outline">{dept.employees} employees</Badge>
//                     <Badge className={getSentimentBadge(dept.sentiment)} variant="secondary">
//                       {dept.sentiment}
//                     </Badge>
//                   </div>
//                   <span className="text-sm">{dept.avgProgress}%</span>
//                 </div>
//                 <Progress value={dept.avgProgress} />
//               </div>
//             ))}
//           </div>
//         </CardContent>
//       </Card>

//       {/* Employee Details */}
//       <Card className="border border-[#D0E8F5]">
//         <CardHeader className="border-b border-[#E8F3F9]">
//           <CardTitle>Employee Details</CardTitle>
//           <CardDescription>Individual progress and wellbeing indicators</CardDescription>
//         </CardHeader>
//         <CardContent className="pt-6">
//           <div className="space-y-4">
//             {employeeData.map((employee) => (
//               <Card key={employee.id} className="border border-[#D0E8F5]">
//                 <CardContent className="pt-6">
//                   <div className="flex items-start justify-between mb-4">
//                     <div>
//                       <div className="flex items-center gap-2 mb-1">
//                         <h3 className="text-lg">{employee.name}</h3>
//                         {employee.sentiment === 'negative' && (
//                           <Badge variant="destructive" className="gap-1">
//                             <AlertTriangle className="w-3 h-3" />
//                             Needs Support
//                           </Badge>
//                         )}
//                       </div>
//                       <p className="text-sm text-gray-600">
//                         {employee.role} • {employee.department} • {employee.id}
//                       </p>
//                     </div>
//                     <div className="flex items-center gap-4 text-sm">
//                       <div className="text-right">
//                         <p className="text-gray-600">Points</p>
//                         <p>{employee.points}</p>
//                       </div>
//                       <div className="text-right">
//                         <p className="text-gray-600">Sentiment</p>
//                         <div className="flex items-center gap-1 justify-end">
//                           {getSentimentIcon(employee.sentiment)}
//                         </div>
//                       </div>
//                     </div>
//                   </div>

//                   <div className="grid grid-cols-3 gap-4 mb-4 text-sm">
//                     <div className="flex items-center gap-2">
//                       <CheckCircle2 className="w-4 h-4 text-green-600" />
//                       <div>
//                         <p className="text-gray-600">Completed</p>
//                         <p>{employee.coursesCompleted} courses</p>
//                       </div>
//                     </div>
//                     <div className="flex items-center gap-2">
//                       <Clock className="w-4 h-4 text-[#4167B1]" />
//                       <div>
//                         <p className="text-gray-600">In Progress</p>
//                         <p>{employee.coursesInProgress} courses</p>
//                       </div>
//                     </div>
//                     <div className="flex items-center gap-2">
//                       <Target className="w-4 h-4 text-purple-600" />
//                       <div>
//                         <p className="text-gray-600">Last Active</p>
//                         <p>{employee.lastActive}</p>
//                       </div>
//                     </div>
//                   </div>

//                   <div className="space-y-2">
//                     <div className="flex items-center justify-between text-sm">
//                       <span className="text-gray-600">Career Progress</span>
//                       <span>{employee.careerProgress}%</span>
//                     </div>
//                     <Progress value={employee.careerProgress} />
//                   </div>
//                 </CardContent>
//               </Card>
//             ))}
//           </div>
//         </CardContent>
//       </Card>
//     </div>
//   );
// }

import { useState, useEffect } from 'react';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '../ui/card';
import { Badge } from '../ui/badge';
import { Progress } from '../ui/progress';
import { Button } from '../ui/button';
import { 
  Users, TrendingUp, Award, BookOpen, 
  Target, Briefcase, Building2, GraduationCap, Crown, Search
} from 'lucide-react';
import { Tabs, TabsContent, TabsList, TabsTrigger } from '../ui/tabs';
import { Input } from '../ui/input';

interface AnalyticsData {
  total_employees: number;
  roles_count: Record<string, number>;
  department_count: Record<string, number>;
  level_count: Record<string, number>;
  top_skills: [string, number][];
  top_goals: [string, number][];
  top_enrolled_courses: [string, number][];
  top_recommended_courses: any[][];
  leadership_distribution: Record<string, number>;
  high_potential_employees: any[];
  most_senior: any[];
  role_analytics: any[];
  roles_lacking_skills: any[];
}

interface Employee {
  id: string;
  name: string;
  department_id: string;
  role: string;
  level: string;
  years_with_company: number;
  skills: string[];
  goals: string[];
  leadership_summary: string;
}

export default function EmployeeAnalytics() {
  const [analyticsData, setAnalyticsData] = useState<AnalyticsData | null>(null);
  const [employees, setEmployees] = useState<Employee[]>([]);
  const [filteredEmployees, setFilteredEmployees] = useState<Employee[]>([]);
  const [searchTerm, setSearchTerm] = useState('');
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    fetchAnalytics();
    fetchEmployees();
  }, []);

  useEffect(() => {
    if (searchTerm === '') {
      setFilteredEmployees(employees);
    } else {
      const filtered = employees.filter(emp => 
        emp.name.toLowerCase().includes(searchTerm.toLowerCase()) ||
        emp.role.toLowerCase().includes(searchTerm.toLowerCase()) ||
        emp.id.toLowerCase().includes(searchTerm.toLowerCase())
      );
      setFilteredEmployees(filtered);
    }
  }, [searchTerm, employees]);

  const fetchAnalytics = async () => {
    setLoading(true);
    try {
      const res = await fetch('http://localhost:8000/api/v1/analytics/overview');
      const data = await res.json();
      setAnalyticsData(data);
    } catch (err) {
      console.error('Error fetching analytics:', err);
    } finally {
      setLoading(false);
    }
  };

  const fetchEmployees = async () => {
    try {
      const res = await fetch('http://localhost:8000/api/v1/analytics/employees');
      const data = await res.json();
      setEmployees(data);
      setFilteredEmployees(data);
    } catch (err) {
      console.error('Error fetching employees:', err);
    }
  };

  const getLeadershipLevel = (summary: string) => {
    if (!summary) return 'Unknown';
    const lower = summary.toLowerCase();
    if (lower.includes('high') && (lower.includes('high level') || lower.includes('high-level'))) return 'High';
    if (lower.includes('mid') || lower.includes('moderate')) return 'Mid';
    if (lower.includes('low')) return 'Low';
    return 'Mid';
  };

  const getLeadershipColor = (level: string) => {
    switch (level) {
      case 'High': return 'bg-green-100 text-green-800 border-green-200';
      case 'Mid': return 'bg-yellow-100 text-yellow-800 border-yellow-200';
      case 'Low': return 'bg-orange-100 text-orange-800 border-orange-200';
      default: return 'bg-gray-100 text-gray-800 border-gray-200';
    }
  };

  if (loading || !analyticsData) {
    return (
      <div className="p-6">
        <Card className="border border-[#D0E8F5]">
          <CardContent className="p-12 text-center">
            <p>Loading analytics...</p>
          </CardContent>
        </Card>
      </div>
    );
  }

  const totalCoursesEnrolled = analyticsData.top_enrolled_courses.reduce((sum, [_, count]) => sum + count, 0);
  const avgLeadershipScore = analyticsData.role_analytics
    .filter(role => role.avg_leadership_score !== null)
    .reduce((sum, role) => sum + (role.avg_leadership_score || 0), 0) / 
    analyticsData.role_analytics.filter(role => role.avg_leadership_score !== null).length;

  return (
    <div className="space-y-6 p-6 max-w-7xl mx-auto">
      <div className="flex items-center justify-between mb-6">
        <div>
          <h1 className="text-3xl font-bold text-[#4167B1]">Employee Analytics Dashboard</h1>
          <p className="text-muted-foreground">Comprehensive view of workforce development and potential</p>
        </div>
        <Button onClick={() => { fetchAnalytics(); fetchEmployees(); }} disabled={loading}>
          {loading ? 'Refreshing...' : 'Refresh Data'}
        </Button>
      </div>

      {/* Overview Stats */}
      <div className="grid md:grid-cols-4 gap-4">
        <Card className="border-2 border-[#4167B1] bg-gradient-to-br from-white to-[#DEF0F9]/30">
          <CardHeader className="pb-3">
            <CardTitle className="text-sm text-muted-foreground flex items-center gap-2">
              <Users className="w-4 h-4" />
              Total Employees
            </CardTitle>
          </CardHeader>
          <CardContent>
            <div className="text-3xl font-bold text-[#4167B1]">{analyticsData.total_employees}</div>
            <p className="text-sm text-muted-foreground">Across {Object.keys(analyticsData.department_count).length} departments</p>
          </CardContent>
        </Card>

        <Card className="border border-[#D0E8F5]">
          <CardHeader className="pb-3">
            <CardTitle className="text-sm text-muted-foreground flex items-center gap-2">
              <BookOpen className="w-4 h-4" />
              Courses Enrolled
            </CardTitle>
          </CardHeader>
          <CardContent>
            <div className="text-3xl font-bold text-foreground">{totalCoursesEnrolled}</div>
            <p className="text-sm text-muted-foreground">{analyticsData.top_enrolled_courses.length} unique courses</p>
          </CardContent>
        </Card>

        <Card className="border border-[#D0E8F5]">
          <CardHeader className="pb-3">
            <CardTitle className="text-sm text-muted-foreground flex items-center gap-2">
              <TrendingUp className="w-4 h-4" />
              Avg Leadership Score
            </CardTitle>
          </CardHeader>
          <CardContent>
            <div className="text-3xl font-bold text-foreground">{avgLeadershipScore.toFixed(1)}</div>
            <p className="text-sm text-muted-foreground">Across all roles</p>
          </CardContent>
        </Card>

        <Card className="border border-[#D0E8F5]">
          <CardHeader className="pb-3">
            <CardTitle className="text-sm text-muted-foreground flex items-center gap-2">
              <Crown className="w-4 h-4" />
              High Potential
            </CardTitle>
          </CardHeader>
          <CardContent>
            <div className="text-3xl font-bold text-foreground">{analyticsData.high_potential_employees.length}</div>
            <p className="text-sm text-green-600">Leadership candidates</p>
          </CardContent>
        </Card>
      </div>

      {/* Main Tabs */}
      <Tabs defaultValue="overview" className="space-y-6">
        <TabsList className="grid w-full grid-cols-6">
          <TabsTrigger value="overview">Overview</TabsTrigger>
          <TabsTrigger value="departments">Departments</TabsTrigger>
          <TabsTrigger value="roles">Roles</TabsTrigger>
          <TabsTrigger value="skills">Skills & Goals</TabsTrigger>
          <TabsTrigger value="leadership">Leadership</TabsTrigger>
          <TabsTrigger value="employees">Employees</TabsTrigger>
        </TabsList>

        {/* Overview Tab */}
        <TabsContent value="overview" className="space-y-4">
          <Card className="border border-[#D0E8F5]">
            <CardHeader>
              <CardTitle>Employee Level Distribution</CardTitle>
              <CardDescription>Breakdown by seniority level</CardDescription>
            </CardHeader>
            <CardContent>
              <div className="space-y-4">
                {Object.entries(analyticsData.level_count).map(([level, count]) => {
                  const percentage = (count / analyticsData.total_employees) * 100;
                  return (
                    <div key={level} className="space-y-2">
                      <div className="flex items-center justify-between">
                        <div className="flex items-center gap-3">
                          <span className="font-medium">{level}</span>
                          <Badge variant="outline">{count} employees</Badge>
                        </div>
                        <span className="text-sm font-medium">{percentage.toFixed(1)}%</span>
                      </div>
                      <Progress value={percentage} />
                    </div>
                  );
                })}
              </div>
            </CardContent>
          </Card>

          <div className="grid md:grid-cols-2 gap-4">
            <Card className="border border-[#D0E8F5]">
              <CardHeader>
                <CardTitle className="flex items-center gap-2">
                  <BookOpen className="w-5 h-5" />
                  Top Enrolled Courses
                </CardTitle>
                <CardDescription>Most popular courses among employees</CardDescription>
              </CardHeader>
              <CardContent>
                <div className="space-y-2">
                  {analyticsData.top_enrolled_courses.slice(0, 6).map(([course, count]) => (
                    <div key={course} className="flex items-center justify-between p-2 bg-blue-50 rounded">
                      <span className="text-sm font-medium">{course}</span>
                      <Badge variant="secondary">{count} enrolled</Badge>
                    </div>
                  ))}
                </div>
              </CardContent>
            </Card>

            <Card className="border border-[#D0E8F5]">
              <CardHeader>
                <CardTitle className="flex items-center gap-2">
                  <GraduationCap className="w-5 h-5" />
                  Top Recommended Courses
                </CardTitle>
                <CardDescription>AI-suggested learning paths</CardDescription>
              </CardHeader>
              <CardContent>
                <div className="space-y-2">
                  {analyticsData.top_recommended_courses.slice(0, 6).map(([course, count], idx) => (
                    <div key={idx} className="flex items-center justify-between p-2 bg-green-50 rounded">
                      <span className="text-sm font-medium truncate flex-1">{course.title || course}</span>
                      <Badge className="bg-green-600 ml-2">{count}</Badge>
                    </div>
                  ))}
                </div>
              </CardContent>
            </Card>
          </div>
        </TabsContent>

        {/* Departments Tab */}
        <TabsContent value="departments" className="space-y-4">
          <Card className="border border-[#D0E8F5]">
            <CardHeader>
              <CardTitle className="flex items-center gap-2">
                <Building2 className="w-5 h-5" />
                Department Overview
              </CardTitle>
              <CardDescription>Employee distribution across departments</CardDescription>
            </CardHeader>
            <CardContent>
              <div className="space-y-4">
                {Object.entries(analyticsData.department_count).map(([dept, count]) => {
                  const percentage = (count / analyticsData.total_employees) * 100;
                  return (
                    <div key={dept} className="space-y-2">
                      <div className="flex items-center justify-between">
                        <div className="flex items-center gap-3">
                          <span className="font-medium">{dept}</span>
                          <Badge variant="outline">{count} employees</Badge>
                        </div>
                        <span className="text-sm font-medium">{percentage.toFixed(1)}%</span>
                      </div>
                      <Progress value={percentage} className="h-3" />
                    </div>
                  );
                })}
              </div>
            </CardContent>
          </Card>
        </TabsContent>

        {/* Roles Tab */}
        <TabsContent value="roles" className="space-y-4">
          <Card className="border border-[#D0E8F5]">
            <CardHeader>
              <CardTitle className="flex items-center gap-2">
                <Briefcase className="w-5 h-5" />
                Role Analytics
              </CardTitle>
              <CardDescription>Skills, tenure, and leadership by role</CardDescription>
            </CardHeader>
            <CardContent>
              <div className="space-y-3">
                {analyticsData.role_analytics.map((role) => (
                  <Card key={role.role} className="border border-[#D0E8F5]">
                    <CardContent className="p-4">
                      <div className="flex items-start justify-between mb-3">
                        <div>
                          <h3 className="font-semibold">{role.role}</h3>
                          <p className="text-sm text-muted-foreground">{role.count} {role.count === 1 ? 'employee' : 'employees'}</p>
                        </div>
                        {role.avg_leadership_score && (
                          <Badge className="bg-[#4167B1]">
                            {role.avg_leadership_score.toFixed(1)} Leadership
                          </Badge>
                        )}
                      </div>
                      <div className="grid grid-cols-3 gap-4 text-sm">
                        <div>
                          <p className="text-muted-foreground">Avg Skills</p>
                          <p className="font-medium">{role.avg_skills.toFixed(1)}</p>
                        </div>
                        <div>
                          <p className="text-muted-foreground">Avg Tenure</p>
                          <p className="font-medium">{role.avg_years.toFixed(1)} yrs</p>
                        </div>
                        <div>
                          <p className="text-muted-foreground">Leadership</p>
                          <p className="font-medium">{role.avg_leadership_score ? role.avg_leadership_score.toFixed(1) : 'N/A'}</p>
                        </div>
                      </div>
                    </CardContent>
                  </Card>
                ))}
              </div>
            </CardContent>
          </Card>

          {analyticsData.roles_lacking_skills.length > 0 && (
            <Card className="border-2 border-amber-200 bg-amber-50/50">
              <CardHeader>
                <CardTitle className="flex items-center gap-2 text-amber-900">
                  <Award className="w-5 h-5" />
                  Roles Needing Skill Development
                </CardTitle>
                <CardDescription>Roles with average skills ≤ 3.0</CardDescription>
              </CardHeader>
              <CardContent>
                <div className="flex flex-wrap gap-2">
                  {analyticsData.roles_lacking_skills.map((role) => (
                    <Badge key={role.role} variant="outline" className="bg-white">
                      {role.role} ({role.count})
                    </Badge>
                  ))}
                </div>
              </CardContent>
            </Card>
          )}
        </TabsContent>

        {/* Skills & Goals Tab */}
        <TabsContent value="skills" className="space-y-4">
          <div className="grid md:grid-cols-2 gap-4">
            <Card className="border border-[#D0E8F5]">
              <CardHeader>
                <CardTitle className="flex items-center gap-2">
                  <Award className="w-5 h-5" />
                  Top Skills
                </CardTitle>
                <CardDescription>Most common skills across the company</CardDescription>
              </CardHeader>
              <CardContent>
                <div className="space-y-3">
                  {analyticsData.top_skills.map(([skill, count]) => (
                    <div key={skill} className="flex items-center justify-between">
                      <span className="text-sm">{skill}</span>
                      <div className="flex items-center gap-2">
                        <Progress value={(count / analyticsData.total_employees) * 100} className="w-24 h-2" />
                        <Badge variant="secondary">{count}</Badge>
                      </div>
                    </div>
                  ))}
                </div>
              </CardContent>
            </Card>

            <Card className="border border-[#D0E8F5]">
              <CardHeader>
                <CardTitle className="flex items-center gap-2">
                  <Target className="w-5 h-5" />
                  Top Goals
                </CardTitle>
                <CardDescription>Most common career goals</CardDescription>
              </CardHeader>
              <CardContent>
                <div className="space-y-3">
                  {analyticsData.top_goals.slice(0, 15).map(([goal, count]) => (
                    <div key={goal} className="flex items-center justify-between">
                      <span className="text-sm">{goal}</span>
                      <Badge className="bg-[#4167B1]">{count}</Badge>
                    </div>
                  ))}
                </div>
              </CardContent>
            </Card>
          </div>
        </TabsContent>

        {/* Leadership Tab */}
        <TabsContent value="leadership" className="space-y-4">
          <Card className="border border-[#D0E8F5]">
            <CardHeader>
              <CardTitle className="flex items-center gap-2">
                <Crown className="w-5 h-5" />
                Leadership Potential Distribution
              </CardTitle>
              <CardDescription>Company-wide leadership assessment</CardDescription>
            </CardHeader>
            <CardContent>
              <div className="space-y-4">
                {Object.entries(analyticsData.leadership_distribution).sort((a, b) => {
                  const order = { 'High': 0, 'Mid': 1, 'Low': 2 };
                  return (order[a[0] as keyof typeof order] || 99) - (order[b[0] as keyof typeof order] || 99);
                }).map(([level, count]) => {
                  const percentage = (count / analyticsData.total_employees) * 100;
                  return (
                    <div key={level} className="space-y-2">
                      <div className="flex items-center justify-between">
                        <div className="flex items-center gap-3">
                          <span className="font-medium">{level} Potential</span>
                          <Badge variant="outline">{count} employees</Badge>
                        </div>
                        <span className="text-sm font-medium">{percentage.toFixed(1)}%</span>
                      </div>
                      <Progress value={percentage} />
                    </div>
                  );
                })}
              </div>
            </CardContent>
          </Card>

          <Card className="border-2 border-green-200 bg-green-50/50">
            <CardHeader>
              <CardTitle className="flex items-center gap-2 text-green-900">
                <Crown className="w-5 h-5" />
                High Potential Employees
              </CardTitle>
              <CardDescription>Top {analyticsData.high_potential_employees.length} leadership candidates</CardDescription>
            </CardHeader>
            <CardContent>
              <div className="grid md:grid-cols-2 gap-3">
                {analyticsData.high_potential_employees.map((emp) => (
                  <Card key={emp.id} className="border border-green-200">
                    <CardContent className="p-4">
                      <div className="flex items-start justify-between mb-2">
                        <div>
                          <h3 className="font-semibold">{emp.name}</h3>
                          <p className="text-sm text-muted-foreground">{emp.role} • {emp.level}</p>
                        </div>
                        {emp.leadership_score && (
                          <Badge className="bg-green-600">
                            {emp.leadership_score}
                          </Badge>
                        )}
                      </div>
                      <div className="grid grid-cols-2 gap-2 text-sm mt-3">
                        <div>
                          <p className="text-muted-foreground">Department</p>
                          <p className="font-medium">{emp.department_id}</p>
                        </div>
                        <div>
                          <p className="text-muted-foreground">Tenure</p>
                          <p className="font-medium">{emp.years_with_company.toFixed(1)} yrs</p>
                        </div>
                      </div>
                    </CardContent>
                  </Card>
                ))}
              </div>
            </CardContent>
          </Card>

          <Card className="border border-[#D0E8F5]">
            <CardHeader>
              <CardTitle>Most Senior Employees</CardTitle>
              <CardDescription>Top 10 by tenure</CardDescription>
            </CardHeader>
            <CardContent>
              <div className="space-y-2">
                {analyticsData.most_senior.map((emp, idx) => (
                  <div key={emp.id} className="flex items-center justify-between p-3 bg-[#DEF0F9] rounded">
                    <div className="flex items-center gap-3">
                      <Badge className="bg-[#4167B1]">{idx + 1}</Badge>
                      <div>
                        <p className="font-medium">{emp.name}</p>
                        <p className="text-sm text-muted-foreground">{emp.role} • {emp.department_id}</p>
                      </div>
                    </div>
                    <Badge variant="outline">{emp.years_with_company.toFixed(1)} yrs</Badge>
                  </div>
                ))}
              </div>
            </CardContent>
          </Card>
        </TabsContent>

        {/* Employees Tab */}
        <TabsContent value="employees" className="space-y-4">
          <Card className="border border-[#D0E8F5]">
            <CardHeader>
              <CardTitle>All Employees</CardTitle>
              <CardDescription>Complete employee directory with skills and goals</CardDescription>
              <div className="mt-4">
                <div className="relative">
                  <Search className="absolute left-3 top-1/2 -translate-y-1/2 w-4 h-4 text-muted-foreground" />
                  <Input
                    placeholder="Search by name, role, or ID..."
                    value={searchTerm}
                    onChange={(e) => setSearchTerm(e.target.value)}
                    className="pl-10"
                  />
                </div>
              </div>
            </CardHeader>
            <CardContent>
              <div className="space-y-3 max-h-[600px] overflow-y-auto">
                {filteredEmployees.map((emp) => {
                  const leadershipLevel = getLeadershipLevel(emp.leadership_summary);
                  return (
                    <Card key={emp.id} className="border border-[#D0E8F5]">
                      <CardContent className="p-4">
                        <div className="flex items-start justify-between mb-3">
                          <div>
                            <h3 className="font-semibold">{emp.name}</h3>
                            <p className="text-sm text-muted-foreground">{emp.role} • {emp.level}</p>
                            <p className="text-xs text-muted-foreground mt-1">{emp.id} • {emp.department_id}</p>
                          </div>
                          <div className="flex flex-col items-end gap-2">
                            <Badge className={getLeadershipColor(leadershipLevel)}>
                              {leadershipLevel} Leadership
                            </Badge>
                            <span className="text-sm text-muted-foreground">{emp.years_with_company.toFixed(1)} yrs</span>
                          </div>
                        </div>
                        
                        <div className="space-y-3">
                          <div>
                            <p className="text-xs text-muted-foreground mb-2">Skills</p>
                            <div className="flex flex-wrap gap-1">
                              {emp.skills.map((skill) => (
                                <Badge key={skill} variant="outline" className="text-xs">{skill}</Badge>
                              ))}
                            </div>
                          </div>
                          
                          <div>
                            <p className="text-xs text-muted-foreground mb-2">Goals</p>
                            <div className="flex flex-wrap gap-1">
                              {emp.goals.map((goal) => (
                                <Badge key={goal} variant="secondary" className="text-xs">{goal}</Badge>
                              ))}
                            </div>
                          </div>
                        </div>
                      </CardContent>
                    </Card>
                  );
                })}
              </div>
            </CardContent>
          </Card>
        </TabsContent>
      </Tabs>
    </div>
  );
}