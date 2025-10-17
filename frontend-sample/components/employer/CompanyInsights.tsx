import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '../ui/card';
import { Badge } from '../ui/badge';
import { Progress } from '../ui/progress';
import { Alert, AlertDescription } from '../ui/alert';
import { 
  TrendingUp, TrendingDown, AlertTriangle, Lightbulb, 
  Users, Award, Target, ArrowUp, ArrowDown,
  Brain, Activity, BarChart3, PieChart, Shield
} from 'lucide-react';
import { 
  BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, 
  ResponsiveContainer, Cell, PieChart as RePieChart, Pie, 
  LineChart, Line, Legend, RadarChart, PolarGrid, 
  PolarAngleAxis, PolarRadiusAxis, Radar
} from 'recharts';

const insights = [
  {
    id: 1,
    title: 'High Potential Employees',
    description: '15 employees showing exceptional growth trajectory',
    type: 'positive',
    priority: 'high',
    action: 'Consider for leadership development programs',
    metric: '15',
    icon: Award,
  },
  {
    id: 2,
    title: 'Skills Gap in Cloud Technologies',
    description: '60% of engineering team lacks cloud certifications',
    type: 'warning',
    priority: 'high',
    action: 'Recommend AWS/Azure training courses company-wide',
    metric: '60%',
    icon: Brain,
  },
  {
    id: 3,
    title: 'Wellbeing Support Usage',
    description: 'Anonymous chat usage increased 25% this month',
    type: 'neutral',
    priority: 'medium',
    action: 'Monitor sentiment trends and provide additional resources',
    metric: '+25%',
    icon: Activity,
  },
  {
    id: 4,
    title: 'Mentor Shortage',
    description: 'Mentee-to-mentor ratio is 5:1, recommend 3:1',
    type: 'warning',
    priority: 'medium',
    action: 'Incentivize senior employees to become mentors',
    metric: '5:1',
    icon: Users,
  },
];

const potentialEmployees = [
  {
    id: 'EMP001',
    name: 'Alex Johnson',
    role: 'Software Developer',
    potential: 'High',
    strengths: ['Fast learner', 'Strong technical skills', 'Good mentor'],
    recommendations: ['Consider for tech lead role', 'Assign challenging projects'],
    growthRate: 85,
  },
  {
    id: 'EMP004',
    name: 'Emily Davis',
    role: 'Data Analyst',
    potential: 'High',
    strengths: ['Analytical mindset', 'Cross-functional collaboration', 'Initiative'],
    recommendations: ['Leadership training', 'Mentor junior analysts'],
    growthRate: 90,
  },
  {
    id: 'EMP002',
    name: 'Sarah Chen',
    role: 'Product Manager',
    potential: 'Very High',
    strengths: ['Strategic thinking', 'Stakeholder management', 'Innovation'],
    recommendations: ['Director track development', 'Executive coaching'],
    growthRate: 95,
  },
];

const improvementAreas = [
  {
    department: 'Engineering',
    area: 'Cloud Architecture',
    gap: 60,
    impact: 'High',
    suggestion: 'Launch AWS Solutions Architect certification program',
  },
  {
    department: 'Product',
    area: 'Data-Driven Decision Making',
    gap: 40,
    impact: 'Medium',
    suggestion: 'Implement analytics training and tools',
  },
  {
    department: 'Design',
    area: 'UX Research Methods',
    gap: 55,
    impact: 'Medium',
    suggestion: 'Partner with UX research consultants for workshops',
  },
];

const departmentSkillsData = [
  { department: 'Engineering', current: 72, target: 90 },
  { department: 'Product', current: 65, target: 85 },
  { department: 'Design', current: 68, target: 88 },
  { department: 'Analytics', current: 80, target: 95 },
  { department: 'Marketing', current: 58, target: 80 },
];

const growthTrendData = [
  { month: 'Jan', engagement: 65, learning: 70, retention: 88 },
  { month: 'Feb', engagement: 68, learning: 73, retention: 89 },
  { month: 'Mar', engagement: 72, learning: 78, retention: 91 },
  { month: 'Apr', engagement: 75, learning: 82, retention: 92 },
  { month: 'May', engagement: 78, learning: 85, retention: 93 },
];

const talentDistribution = [
  { name: 'Very High Potential', value: 15, color: '#2563EB' },
  { name: 'High Potential', value: 28, color: '#60A5FA' },
  { name: 'Medium Potential', value: 42, color: '#93C5FD' },
  { name: 'Developing', value: 25, color: '#DBEAFE' },
];

const radarData = [
  { skill: 'Technical', current: 78, industry: 85 },
  { skill: 'Leadership', current: 65, industry: 70 },
  { skill: 'Communication', current: 82, industry: 75 },
  { skill: 'Innovation', current: 70, industry: 80 },
  { skill: 'Collaboration', current: 88, industry: 82 },
];

export default function CompanyInsights() {
  const getInsightIcon = (type: string) => {
    switch (type) {
      case 'positive':
        return 'text-[#4167B1] bg-[#DEF0F9]';
      case 'warning':
        return 'text-secondary bg-orange-50';
      default:
        return 'text-[#4167B1] bg-[#DEF0F9]';
    }
  };

  const getPotentialBadge = (potential: string) => {
    switch (potential) {
      case 'Very High':
        return 'bg-[#4167B1] text-white';
      case 'High':
        return 'bg-secondary text-white';
      default:
        return 'bg-gray-500 text-white';
    }
  };

  return (
    <div className="space-y-6">
      {/* Overview Stats */}
      <div className="grid md:grid-cols-4 gap-4">
        <Card className="border border-[#D0E8F5]">
          <CardContent className="pt-6">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm text-muted-foreground mb-1">Top Performers</p>
                <p className="text-3xl text-foreground">15</p>
                <p className="text-xs text-muted-foreground mt-1">High potential employees</p>
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
                <p className="text-sm text-muted-foreground mb-1">Avg Growth Rate</p>
                <p className="text-3xl text-foreground">+12%</p>
                <p className="text-xs text-green-600 mt-1 flex items-center gap-1">
                  <ArrowUp className="w-3 h-3" />
                  vs last quarter
                </p>
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
                <p className="text-sm text-muted-foreground mb-1">Engagement Score</p>
                <p className="text-3xl text-foreground">78%</p>
                <p className="text-xs text-muted-foreground mt-1">Company average</p>
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
                <p className="text-sm text-muted-foreground mb-1">Retention Rate</p>
                <p className="text-3xl text-foreground">93%</p>
                <p className="text-xs text-muted-foreground mt-1">Above industry avg</p>
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
                        <h4 className="text-sm">{insight.title}</h4>
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
        {/* Growth Trends Chart */}
        <Card className="border border-[#D0E8F5]">
          <CardHeader className="border-b border-[#E8F3F9]">
            <CardTitle className="flex items-center gap-2 text-base">
              <BarChart3 className="w-5 h-5 text-[#4167B1]" />
              Growth Trends
            </CardTitle>
            <CardDescription>Monthly progress across key metrics</CardDescription>
          </CardHeader>
          <CardContent className="pt-6">
            <ResponsiveContainer width="100%" height={280}>
              <LineChart data={growthTrendData}>
                <CartesianGrid strokeDasharray="3 3" stroke="#E5E7EB" vertical={false} />
                <XAxis 
                  dataKey="month" 
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
                <Legend wrapperStyle={{ fontSize: '12px' }} />
                <Line 
                  type="monotone" 
                  dataKey="engagement" 
                  stroke="#2563EB" 
                  strokeWidth={2} 
                  name="Engagement"
                  dot={{ r: 4 }}
                />
                <Line 
                  type="monotone" 
                  dataKey="learning" 
                  stroke="#F97316" 
                  strokeWidth={2} 
                  name="Learning"
                  dot={{ r: 4 }}
                />
                <Line 
                  type="monotone" 
                  dataKey="retention" 
                  stroke="#10B981" 
                  strokeWidth={2} 
                  name="Retention"
                  dot={{ r: 4 }}
                />
              </LineChart>
            </ResponsiveContainer>
          </CardContent>
        </Card>

        {/* Talent Distribution */}
        <Card className="border border-[#D0E8F5]">
          <CardHeader className="border-b border-[#E8F3F9]">
            <CardTitle className="flex items-center gap-2 text-base">
              <PieChart className="w-5 h-5 text-[#4167B1]" />
              Talent Distribution
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
                  label={({ name, percent }) => `${name}: ${(percent * 100).toFixed(0)}%`}
                  outerRadius={90}
                  fill="#8884d8"
                  dataKey="value"
                >
                  {talentDistribution.map((entry, index) => (
                    <Cell key={`cell-${index}`} fill={entry.color} />
                  ))}
                </Pie>
                <Tooltip contentStyle={{ fontSize: '12px', borderRadius: '8px' }} />
              </RePieChart>
            </ResponsiveContainer>
          </CardContent>
        </Card>
      </div>

      {/* Skills Comparison Chart */}
      <div className="grid md:grid-cols-2 gap-6">
        <Card className="border border-[#D0E8F5]">
          <CardHeader className="border-b border-[#E8F3F9]">
            <CardTitle className="flex items-center gap-2 text-base">
              <Activity className="w-5 h-5 text-[#4167B1]" />
              Department Skills Analysis
            </CardTitle>
            <CardDescription>Current vs target skill levels</CardDescription>
          </CardHeader>
          <CardContent className="pt-6">
            <ResponsiveContainer width="100%" height={280}>
              <BarChart data={departmentSkillsData}>
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
                <Legend wrapperStyle={{ fontSize: '12px' }} />
                <Bar dataKey="current" fill="#2563EB" name="Current" radius={[4, 4, 0, 0]} />
                <Bar dataKey="target" fill="#F97316" name="Target" radius={[4, 4, 0, 0]} />
              </BarChart>
            </ResponsiveContainer>
          </CardContent>
        </Card>

        {/* Radar Chart */}
        <Card className="border border-[#D0E8F5]">
          <CardHeader className="border-b border-[#E8F3F9]">
            <CardTitle className="flex items-center gap-2 text-base">
              <Brain className="w-5 h-5 text-[#4167B1]" />
              Skills Benchmarking
            </CardTitle>
            <CardDescription>Company vs industry standards</CardDescription>
          </CardHeader>
          <CardContent className="pt-6">
            <ResponsiveContainer width="100%" height={280}>
              <RadarChart data={radarData}>
                <PolarGrid stroke="#E5E7EB" />
                <PolarAngleAxis dataKey="skill" stroke="#6B7280" tick={{ fontSize: 12 }} />
                <PolarRadiusAxis stroke="#6B7280" tick={{ fontSize: 12 }} />
                <Radar 
                  name="Company" 
                  dataKey="current" 
                  stroke="#2563EB" 
                  fill="#2563EB" 
                  fillOpacity={0.5} 
                />
                <Radar 
                  name="Industry" 
                  dataKey="industry" 
                  stroke="#F97316" 
                  fill="#F97316" 
                  fillOpacity={0.3} 
                />
                <Legend wrapperStyle={{ fontSize: '12px' }} />
                <Tooltip contentStyle={{ fontSize: '12px', borderRadius: '8px' }} />
              </RadarChart>
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
            Top talent showing exceptional growth (Hidden from employees)
          </CardDescription>
        </CardHeader>
        <CardContent className="pt-6">
          <div className="grid md:grid-cols-3 gap-4">
            {potentialEmployees.map((employee) => (
              <Card key={employee.id} className="border border-[#D0E8F5]">
                <CardContent className="pt-6">
                  <div className="flex items-start justify-between mb-4">
                    <div className="flex-1">
                      <h3 className="text-base mb-1">{employee.name}</h3>
                      <p className="text-sm text-muted-foreground mb-3">{employee.role}</p>
                      <Badge className={getPotentialBadge(employee.potential)} variant="secondary">
                        {employee.potential} Potential
                      </Badge>
                    </div>
                    <div className="text-right">
                      <p className="text-xs text-muted-foreground">Growth</p>
                      <div className="flex items-center gap-1 text-green-600">
                        <ArrowUp className="w-4 h-4" />
                        <span className="text-lg">{employee.growthRate}%</span>
                      </div>
                    </div>
                  </div>

                  <div className="mb-4">
                    <Progress value={employee.growthRate} className="h-2" />
                  </div>

                  <div className="mb-4">
                    <p className="text-xs text-muted-foreground mb-2">Key Strengths</p>
                    <div className="flex flex-wrap gap-1">
                      {employee.strengths.map((strength, idx) => (
                        <Badge key={idx} variant="outline" className="text-xs">{strength}</Badge>
                      ))}
                    </div>
                  </div>

                  <div className="space-y-2 bg-[#DEF0F9] p-3 rounded-lg border border-[#D0E8F5]">
                    <p className="text-xs text-muted-foreground">Recommended Actions</p>
                    {employee.recommendations.map((rec, idx) => (
                      <div key={idx} className="flex items-start gap-2 text-sm">
                        <span className="text-[#4167B1] mt-1">•</span>
                        <span className="text-sm text-foreground">{rec}</span>
                      </div>
                    ))}
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
          <CardTitle>Skills Gaps & Improvement Opportunities</CardTitle>
          <CardDescription>Strategic areas for workforce development</CardDescription>
        </CardHeader>
        <CardContent className="pt-6 space-y-6">
          {improvementAreas.map((area, idx) => (
            <div key={idx} className="border border-[#D0E8F5] rounded-lg p-5">
              <div className="flex items-start justify-between mb-4">
                <div>
                  <h4 className="text-base mb-1">{area.area}</h4>
                  <p className="text-sm text-muted-foreground">{area.department} Department</p>
                </div>
                <Badge 
                  variant="outline" 
                  className={area.impact === 'High' ? 'border-secondary text-secondary' : 'border-gray-400 text-gray-600'}
                >
                  {area.impact} Impact
                </Badge>
              </div>

              <div className="mb-4">
                <div className="flex items-center justify-between text-sm mb-2">
                  <span className="text-muted-foreground">Current Coverage</span>
                  <span className="text-foreground">{100 - area.gap}% skilled</span>
                </div>
                <Progress value={100 - area.gap} className="h-2" />
                <p className="text-xs text-muted-foreground mt-1">
                  Gap: {area.gap}% of team needs training
                </p>
              </div>

              <Alert className="border-[#4167B1]/20 bg-[#DEF0F9]">
                <Lightbulb className="w-4 h-4 text-[#4167B1]" />
                <AlertDescription>
                  <p className="text-sm text-foreground">
                    <strong className="text-[#4167B1]">Recommended Action: </strong>
                    {area.suggestion}
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
