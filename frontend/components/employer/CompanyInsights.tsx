import { useState, useEffect } from 'react';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '../ui/card';
import { Badge } from '../ui/badge';
import { Progress } from '../ui/progress';
import { Alert, AlertDescription } from '../ui/alert';
import { Button } from '../ui/button';
import { 
  TrendingUp, AlertTriangle, Lightbulb, 
  Users, Award, Target, ArrowUp,
  Brain, Activity, BarChart3, PieChart, Shield, BookOpen
} from 'lucide-react';
import { 
  BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, 
  ResponsiveContainer, Cell, PieChart as RePieChart, Pie, Legend
} from 'recharts';

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

export default function CompanyInsights() {
  const [analyticsData, setAnalyticsData] = useState<AnalyticsData | null>(null);
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    fetchAnalytics();
  }, []);

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

  if (loading || !analyticsData) {
    return (
      <div className="p-6">
        <Card className="border border-[#D0E8F5]">
          <CardContent className="p-12 text-center">
            <p>Loading insights...</p>
          </CardContent>
        </Card>
      </div>
    );
  }

  // Prepare chart data
  const talentDistribution = Object.entries(analyticsData.leadership_distribution).map(([name, value]) => ({
    name: `${name} Potential`,
    value,
    color: name === 'High' ? '#10B981' : name === 'Mid' ? '#F59E0B' : '#EF4444'
  }));

  const departmentData = Object.entries(analyticsData.department_count).map(([dept, count]) => ({
    department: dept,
    employees: count
  }));

  const levelData = Object.entries(analyticsData.level_count).map(([level, count]) => ({
    level,
    count
  }));

  const skillsData = analyticsData.top_skills.slice(0, 10).map(([skill, count]) => ({
    skill: skill.length > 20 ? skill.substring(0, 20) + '...' : skill,
    count
  }));

  const avgLeadershipScore = analyticsData.role_analytics
    .filter(role => role.avg_leadership_score !== null)
    .reduce((sum, role) => sum + (role.avg_leadership_score || 0), 0) / 
    analyticsData.role_analytics.filter(role => role.avg_leadership_score !== null).length;

  const totalCoursesEnrolled = analyticsData.top_enrolled_courses.reduce((sum, [_, count]) => sum + count, 0);

  // Generate insights
  const insights = [
    {
      id: 1,
      title: `${analyticsData.high_potential_employees.length} High Potential Employees`,
      description: `${((analyticsData.high_potential_employees.length / analyticsData.total_employees) * 100).toFixed(1)}% of workforce showing exceptional leadership potential`,
      type: 'positive',
      priority: 'high',
      action: 'Consider for leadership development programs and mentorship roles',
      metric: analyticsData.high_potential_employees.length.toString(),
      icon: Award,
    },
    {
      id: 2,
      title: 'Skills Development Opportunities',
      description: `${analyticsData.roles_lacking_skills.length} roles have average skills ≤ 3.0`,
      type: 'warning',
      priority: 'high',
      action: 'Implement targeted training programs and skill development initiatives',
      metric: analyticsData.roles_lacking_skills.length.toString(),
      icon: Brain,
    },
    {
      id: 3,
      title: 'Course Enrollment Success',
      description: `${totalCoursesEnrolled} total course enrollments across ${analyticsData.top_enrolled_courses.length} courses`,
      type: 'positive',
      priority: 'medium',
      action: 'Continue promoting learning culture and recognize top learners',
      metric: totalCoursesEnrolled.toString(),
      icon: BookOpen,
    },
    {
      id: 4,
      title: 'Leadership Pipeline',
      description: `${analyticsData.leadership_distribution['Low'] || 0} employees at Low leadership level need development`,
      type: 'warning',
      priority: 'medium',
      action: 'Create mentorship programs and provide leadership training opportunities',
      metric: `${analyticsData.leadership_distribution['Low'] || 0}`,
      icon: Users,
    },
  ];

  const getInsightIcon = (type: string) => {
    switch (type) {
      case 'positive':
        return 'text-[#4167B1] bg-[#DEF0F9]';
      case 'warning':
        return 'text-orange-600 bg-orange-50';
      default:
        return 'text-[#4167B1] bg-[#DEF0F9]';
    }
  };

  const getPotentialBadge = (potential: string) => {
    switch (potential) {
      case 'High':
        return 'bg-green-600 text-white';
      case 'Mid':
        return 'bg-yellow-600 text-white';
      default:
        return 'bg-orange-600 text-white';
    }
  };

  return (
    <div className="space-y-6 p-6 max-w-7xl mx-auto">
      <div className="flex items-center justify-between mb-6">
        <div>
          <h1 className="text-3xl font-bold text-[#4167B1]">Company Insights Dashboard</h1>
          <p className="text-muted-foreground">AI-powered analysis of organizational potential and growth opportunities</p>
        </div>
        <Button onClick={fetchAnalytics} disabled={loading}>
          {loading ? 'Refreshing...' : 'Refresh Data'}
        </Button>
      </div>

      {/* Overview Stats */}
      <div className="grid md:grid-cols-4 gap-4">
        <Card className="border border-[#D0E8F5]">
          <CardContent className="pt-6">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm text-muted-foreground mb-1">Top Performers</p>
                <p className="text-3xl font-bold text-foreground">{analyticsData.high_potential_employees.length}</p>
                <p className="text-xs text-green-600 mt-1">High potential employees</p>
              </div>
              <div className="p-3 bg-[#DEF0F9] rounded-lg">
                <Award className="w-6 h-6 text-[#4167B1]" />
              </div>
            </div>
          </CardContent>
        </Card>

        <Card className="border border-[#D0E8F5]">
          <CardContent className="pt-6">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm text-muted-foreground mb-1">Avg Leadership Score</p>
                <p className="text-3xl font-bold text-foreground">{avgLeadershipScore.toFixed(1)}</p>
                <p className="text-xs text-muted-foreground mt-1">Across all roles</p>
              </div>
              <div className="p-3 bg-green-50 rounded-lg">
                <TrendingUp className="w-6 h-6 text-green-600" />
              </div>
            </div>
          </CardContent>
        </Card>

        <Card className="border border-[#D0E8F5]">
          <CardContent className="pt-6">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm text-muted-foreground mb-1">Total Enrollments</p>
                <p className="text-3xl font-bold text-foreground">{totalCoursesEnrolled}</p>
                <p className="text-xs text-muted-foreground mt-1">Course participation</p>
              </div>
              <div className="p-3 bg-[#DEF0F9] rounded-lg">
                <Activity className="w-6 h-6 text-[#4167B1]" />
              </div>
            </div>
          </CardContent>
        </Card>

        <Card className="border border-[#D0E8F5]">
          <CardContent className="pt-6">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm text-muted-foreground mb-1">Avg Tenure</p>
                <p className="text-3xl font-bold text-foreground">
                  {(analyticsData.role_analytics.reduce((sum, r) => sum + r.avg_years, 0) / analyticsData.role_analytics.length).toFixed(1)}
                </p>
                <p className="text-xs text-muted-foreground mt-1">Years with company</p>
              </div>
              <div className="p-3 bg-green-50 rounded-lg">
                <Shield className="w-6 h-6 text-green-600" />
              </div>
            </div>
          </CardContent>
        </Card>
      </div>

      {/* Key Insights */}
      <Card className="border border-[#D0E8F5]">
        <CardHeader className="border-b border-[#E8F3F9] bg-white">
          <CardTitle>Key Insights & Recommendations</CardTitle>
          <CardDescription>AI-powered analysis of company potential and growth opportunities</CardDescription>
        </CardHeader>
        <CardContent className="pt-6">
          <div className="grid md:grid-cols-2 gap-4">
            {insights.map((insight) => {
              const Icon = insight.icon;
              const iconClass = getInsightIcon(insight.type);
              return (
                <div key={insight.id} className="p-4 border border-[#D0E8F5] rounded-lg hover:border-[#4167B1]/50 transition-colors">
                  <div className="flex items-start gap-4">
                    <div className={`p-3 rounded-lg ${iconClass}`}>
                      <Icon className="w-5 h-5" />
                    </div>
                    <div className="flex-1 min-w-0">
                      <div className="flex items-start justify-between gap-2 mb-2">
                        <h4 className="font-semibold">{insight.title}</h4>
                        <Badge variant="outline" className="shrink-0">{insight.priority}</Badge>
                      </div>
                      <p className="text-sm text-muted-foreground mb-3">{insight.description}</p>
                      <div className="flex items-start gap-2 text-sm bg-[#DEF0F9] p-3 rounded-lg border border-[#D0E8F5]">
                        <Lightbulb className="w-4 h-4 mt-0.5 text-[#4167B1] shrink-0" />
                        <p className="text-foreground">{insight.action}</p>
                      </div>
                    </div>
                  </div>
                </div>
              );
            })}
          </div>
        </CardContent>
      </Card>

      {/* Charts Section */}
      <div className="grid md:grid-cols-2 gap-6">
        {/* Department Distribution */}
        <Card className="border border-[#D0E8F5]">
          <CardHeader className="border-b border-[#E8F3F9]">
            <CardTitle className="flex items-center gap-2 text-base">
              <BarChart3 className="w-5 h-5 text-[#4167B1]" />
              Department Distribution
            </CardTitle>
            <CardDescription>Employee count by department</CardDescription>
          </CardHeader>
          <CardContent className="pt-6">
            <ResponsiveContainer width="100%" height={280}>
              <BarChart data={departmentData}>
                <CartesianGrid strokeDasharray="3 3" stroke="#E5E7EB" vertical={false} />
                <XAxis 
                  dataKey="department" 
                  stroke="#6B7280"
                  tick={{ fontSize: 12 }}
                  axisLine={false}
                />
                <YAxis 
                  stroke="#6B7280"
                  tick={{ fontSize: 12 }}
                  axisLine={false}
                />
                <Tooltip 
                  contentStyle={{ 
                    backgroundColor: 'white', 
                    border: '1px solid #E5E7EB',
                    borderRadius: '8px',
                    fontSize: '12px'
                  }} 
                />
                <Bar dataKey="employees" fill="#4167B1" radius={[4, 4, 0, 0]} />
              </BarChart>
            </ResponsiveContainer>
          </CardContent>
        </Card>

        {/* Talent Distribution */}
        <Card className="border border-[#D0E8F5]">
          <CardHeader className="border-b border-[#E8F3F9]">
            <CardTitle className="flex items-center gap-2 text-base">
              <PieChart className="w-5 h-5 text-[#4167B1]" />
              Leadership Potential Distribution
            </CardTitle>
            <CardDescription>Employee potential across organization</CardDescription>
          </CardHeader>
          <CardContent className="pt-6">
            <ResponsiveContainer width="100%" height={280}>
              <RePieChart>
                <Pie
                  data={talentDistribution}
                  cx="50%"
                  cy="50%"
                  labelLine={false}
                  label={({ name, value }) => `${name}: ${value}`}
                  outerRadius={90}
                  fill="#8884d8"
                  dataKey="value"
                >
                  {talentDistribution.map((entry, index) => (
                    <Cell key={`cell-${index}`} fill={entry.color} />
                  ))}
                </Pie>
                <Tooltip contentStyle={{ fontSize: '12px', borderRadius: '8px' }} />
                <Legend wrapperStyle={{ fontSize: '12px' }} />
              </RePieChart>
            </ResponsiveContainer>
          </CardContent>
        </Card>
      </div>

      {/* Skills Analysis */}
      <div className="grid md:grid-cols-2 gap-6">
        <Card className="border border-[#D0E8F5]">
          <CardHeader className="border-b border-[#E8F3F9]">
            <CardTitle className="flex items-center gap-2 text-base">
              <Brain className="w-5 h-5 text-[#4167B1]" />
              Top Skills Distribution
            </CardTitle>
            <CardDescription>Most common skills across workforce</CardDescription>
          </CardHeader>
          <CardContent className="pt-6">
            <ResponsiveContainer width="100%" height={280}>
              <BarChart data={skillsData} layout="vertical">
                <CartesianGrid strokeDasharray="3 3" stroke="#E5E7EB" horizontal={false} />
                <XAxis 
                  type="number"
                  stroke="#6B7280"
                  tick={{ fontSize: 12 }}
                  axisLine={false}
                />
                <YAxis 
                  dataKey="skill"
                  type="category"
                  stroke="#6B7280"
                  tick={{ fontSize: 11 }}
                  axisLine={false}
                  width={150}
                />
                <Tooltip 
                  contentStyle={{ 
                    backgroundColor: 'white', 
                    border: '1px solid #E5E7EB',
                    borderRadius: '8px',
                    fontSize: '12px'
                  }} 
                />
                <Bar dataKey="count" fill="#10B981" radius={[0, 4, 4, 0]} />
              </BarChart>
            </ResponsiveContainer>
          </CardContent>
        </Card>

        {/* Level Distribution */}
        <Card className="border border-[#D0E8F5]">
          <CardHeader className="border-b border-[#E8F3F9]">
            <CardTitle className="flex items-center gap-2 text-base">
              <Target className="w-5 h-5 text-[#4167B1]" />
              Seniority Level Distribution
            </CardTitle>
            <CardDescription>Employee breakdown by level</CardDescription>
          </CardHeader>
          <CardContent className="pt-6">
            <ResponsiveContainer width="100%" height={280}>
              <RePieChart>
                <Pie
                  data={levelData}
                  cx="50%"
                  cy="50%"
                  labelLine={false}
                  label={({ level, count }) => `${level}: ${count}`}
                  outerRadius={90}
                  fill="#8884d8"
                  dataKey="count"
                >
                  {levelData.map((entry, index) => (
                    <Cell key={`cell-${index}`} fill={['#4167B1', '#60A5FA', '#93C5FD'][index % 3]} />
                  ))}
                </Pie>
                <Tooltip contentStyle={{ fontSize: '12px', borderRadius: '8px' }} />
                <Legend wrapperStyle={{ fontSize: '12px' }} />
              </RePieChart>
            </ResponsiveContainer>
          </CardContent>
        </Card>
      </div>

      {/* High Potential Employees */}
      <Card className="border border-[#D0E8F5]">
        <CardHeader className="border-b border-[#E8F3F9]">
          <CardTitle className="flex items-center gap-2">
            <Award className="w-5 h-5 text-[#4167B1]" />
            High Potential Employees
          </CardTitle>
          <CardDescription>
            Top {analyticsData.high_potential_employees.length} talent showing exceptional growth potential
          </CardDescription>
        </CardHeader>
        <CardContent className="pt-6">
          <div className="grid md:grid-cols-3 gap-4">
            {analyticsData.high_potential_employees.map((employee) => (
              <Card key={employee.id} className="border border-[#D0E8F5]">
                <CardContent className="pt-6">
                  <div className="flex items-start justify-between mb-4">
                    <div className="flex-1">
                      <h3 className="font-semibold mb-1">{employee.name}</h3>
                      <p className="text-sm text-muted-foreground mb-2">{employee.role}</p>
                      <Badge className="bg-green-600">
                        {employee.leadership_category} Potential
                      </Badge>
                    </div>
                    {employee.leadership_score && (
                      <div className="text-right">
                        <p className="text-xs text-muted-foreground">Score</p>
                        <div className="flex items-center gap-1 text-green-600">
                          <ArrowUp className="w-4 h-4" />
                          <span className="text-lg font-bold">{employee.leadership_score}</span>
                        </div>
                      </div>
                    )}
                  </div>

                  <div className="grid grid-cols-2 gap-3 text-sm">
                    <div>
                      <p className="text-muted-foreground">Level</p>
                      <p className="font-medium">{employee.level}</p>
                    </div>
                    <div>
                      <p className="text-muted-foreground">Tenure</p>
                      <p className="font-medium">{employee.years_with_company.toFixed(1)} yrs</p>
                    </div>
                    <div className="col-span-2">
                      <p className="text-muted-foreground">Department</p>
                      <p className="font-medium">{employee.department_id}</p>
                    </div>
                  </div>

                  <div className="mt-4 p-3 bg-green-50 rounded-lg border border-green-200">
                    <p className="text-xs text-green-900 font-medium mb-1">Recommended Actions</p>
                    <ul className="text-xs text-green-800 space-y-1">
                      <li>• Consider for leadership development</li>
                      <li>• Assign mentorship opportunities</li>
                      <li>• Include in succession planning</li>
                    </ul>
                  </div>
                </CardContent>
              </Card>
            ))}
          </div>
        </CardContent>
      </Card>

      {/* Skills Gaps & Improvement Areas */}
      <Card className="border border-[#D0E8F5]">
        <CardHeader className="border-b border-[#E8F3F9]">
          <CardTitle>Roles Needing Skill Development</CardTitle>
          <CardDescription>Strategic areas for workforce development (Avg Skills ≤ 3.0)</CardDescription>
        </CardHeader>
        <CardContent className="pt-6 space-y-4">
          {analyticsData.roles_lacking_skills.slice(0, 6).map((role, idx) => (
            <div key={idx} className="border border-[#D0E8F5] rounded-lg p-5">
              <div className="flex items-start justify-between mb-4">
                <div>
                  <h4 className="font-semibold mb-1">{role.role}</h4>
                  <p className="text-sm text-muted-foreground">{role.count} {role.count === 1 ? 'employee' : 'employees'}</p>
                </div>
                <Badge variant="outline" className="border-orange-400 text-orange-600">
                  Priority
                </Badge>
              </div>

              <div className="mb-4">
                <div className="flex items-center justify-between text-sm mb-2">
                  <span className="text-muted-foreground">Average Skills</span>
                  <span className="font-medium">{role.avg_skills.toFixed(1)} / 5.0</span>
                </div>
                <Progress value={(role.avg_skills / 5) * 100} className="h-2" />
              </div>

              {role.avg_leadership_score && (
                <div className="mb-4">
                  <div className="flex items-center justify-between text-sm mb-2">
                    <span className="text-muted-foreground">Leadership Score</span>
                    <span className="font-medium">{role.avg_leadership_score.toFixed(1)} / 10</span>
                  </div>
                  <Progress value={(role.avg_leadership_score / 10) * 100} className="h-2" />
                </div>
              )}

              <Alert className="border-[#4167B1]/20 bg-[#DEF0F9]">
                <Lightbulb className="w-4 h-4 text-[#4167B1]" />
                <AlertDescription>
                  <p className="text-sm text-foreground">
                    <strong className="text-[#4167B1]">Recommended: </strong>
                    Implement targeted skill development programs and provide mentorship opportunities
                  </p>
                </AlertDescription>
              </Alert>
            </div>
          ))}
        </CardContent>
      </Card>
    </div>
  );
}