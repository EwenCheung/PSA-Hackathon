import { useState, useEffect } from 'react';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '../ui/card';
import { Progress } from '../ui/progress';
import { Badge } from '../ui/badge';
import { Button } from '../ui/button';
import { BookOpen, TrendingUp, Crown, ExternalLink, Target, Lightbulb } from 'lucide-react';
import { Tabs, TabsContent, TabsList, TabsTrigger } from '../ui/tabs';
import { API_BASE } from '../../src/services/apiClient';
import type { EmployeeProfile } from '../../src/types/employee';

interface CareerPathProps {
  employeeId: string;
  profile: EmployeeProfile;
}

interface Course {
  title: string;
  url: string;
  reason: string;
  matched_skills: string[];
  expected_outcome: string;
}

interface CareerPathway {
  duration: string;
  focus: string[];
  suggested_actions: string[];
  expected_outcomes: string;
}

interface LeadershipEvaluation {
  leadership_analysis: string;
  leadership_score: {
    experience_weight: number;
    learning_engagement_weight: number;
    soft_skills_alignment_weight: number;
    overall_score: number;
  };
  potential_level: string;
  recommendations: string[];
}

export default function CareerPath({ employeeId, profile }: CareerPathProps) {
  const [employeeData, setEmployeeData] = useState<any>(profile);
  const [courses, setCourses] = useState<Course[]>([]);
  const [coursesAnalysis, setCoursesAnalysis] = useState<string>("");
  const [careerPathway, setCareerPathway] = useState<any>(null);
  const [leadership, setLeadership] = useState<LeadershipEvaluation | null>(null);
  const [loading, setLoading] = useState(false);
  const [activeTab, setActiveTab] = useState<'overview' | 'courses' | 'pathway' | 'leadership'>('overview');

  useEffect(() => {
    if (!employeeId) return;
    fetchProfile();
  }, [employeeId]);

  useEffect(() => {
    setEmployeeData(profile);
  }, [profile]);

  const fetchProfile = async () => {
    setLoading(true);
    try {
      const res = await fetch(`${API_BASE}/api/v1/employees/${employeeId}`);
      const data = await res.json();
      setEmployeeData(data);
    } catch (err) {
      console.error('Error fetching profile:', err);
    } finally {
      setLoading(false);
    }
  };

  const fetchCourses = async () => {
    setLoading(true);
    try {
      const res = await fetch(`${API_BASE}/api/v1/employees/${employeeId}/career/recommendations`);
      const data = await res.json();
      setCourses(data.recommendations?.recommended_courses || []);
      setCoursesAnalysis(data.recommendations?.analysis || "");
      setActiveTab('courses');
    } catch (err) {
      console.error('Error fetching courses:', err);
    } finally {
      setLoading(false);
    }
  };

  const fetchCareerPathway = async () => {
    setLoading(true);
    try {
      const res = await fetch(`${API_BASE}/api/v1/employees/${employeeId}/career/pathway`);
      const data = await res.json();
      setCareerPathway(data.career_pathway);
      setActiveTab('pathway');
    } catch (err) {
      console.error('Error fetching career pathway:', err);
    } finally {
      setLoading(false);
    }
  };

  const fetchLeadership = async () => {
    setLoading(true);
    try {
      const res = await fetch(`${API_BASE}/api/v1/employees/${employeeId}/leadership/potential`);
      const data = await res.json();
      setLeadership(data.evaluation);
      setActiveTab('leadership');
    } catch (err) {
      console.error('Error fetching leadership:', err);
    } finally {
      setLoading(false);
    }
  };

  const getPotentialColor = (level: string) => {
    switch (level.toLowerCase()) {
      case 'high': return 'bg-green-100 text-green-800 border-green-200';
      case 'medium': return 'bg-yellow-100 text-yellow-800 border-yellow-200';
      case 'low': return 'bg-orange-100 text-orange-800 border-orange-200';
      default: return 'bg-gray-100 text-gray-800 border-gray-200';
    }
  };

  return (
    <div className="space-y-6 p-6 max-w-7xl mx-auto">
      {/* Employee Profile */}
      {loading && !employeeData.id ? (
        <Card className="border border-[#D0E8F5]">
          <CardContent className="p-6">Loading profile...</CardContent>
        </Card>
      ) : employeeData.id ? (
        <Card className="border-2 border-[#4167B1] bg-gradient-to-br from-white to-[#DEF0F9]/30">
          <CardHeader>
            <div className="flex items-start justify-between">
              <div>
                <CardTitle className="text-3xl text-[#4167B1]">{employeeData.name}</CardTitle>
                <CardDescription className="text-lg mt-1">{employeeData.role} • {employeeData.level}</CardDescription>
              </div>
              <Badge variant="secondary" className="text-lg px-4 py-2">{employeeData.points_current} pts</Badge>
            </div>
          </CardHeader>
          <CardContent className="grid md:grid-cols-2 gap-6">
            <div className="space-y-3">
              <div>
                <p className="text-sm text-muted-foreground">Department</p>
                <p className="font-medium">{employeeData.department_id}</p>
              </div>
              <div>
                <p className="text-sm text-muted-foreground">Hire Date</p>
                <p className="font-medium">{employeeData.hire_date}</p>
              </div>
              <div>
                <p className="text-sm text-muted-foreground mb-2">Skills</p>
                <div className="flex flex-wrap gap-2">
                  {(Array.isArray(employeeData.skills)
                    ? employeeData.skills
                    : Object.keys(employeeData.skills || {})
                  ).map((skill: string) => (
                    <Badge key={skill} variant="outline" className="bg-white">{skill}</Badge>
                  ))}
                </div>
              </div>
            </div>
            <div className="space-y-3">
              <div>
                <p className="text-sm text-muted-foreground mb-2">Career Goals</p>
                <div className="flex flex-wrap gap-2">
                  {(Array.isArray(employeeData.goals) ? employeeData.goals : [])
                    .map((goal: string) => (
                      <Badge key={goal} className="bg-[#4167B1]">{goal}</Badge>
                    ))}
                </div>
              </div>
              <div>
                <p className="text-sm text-muted-foreground mb-2">Enrolled Courses</p>
                {employeeData.courses_enrolled && Object.keys(employeeData.courses_enrolled).length > 0 ? (
                  <div className="space-y-1">
                    {Object.entries(employeeData.courses_enrolled).map(([course, status]) => (
                      <div key={course} className="flex items-center gap-2 text-sm">
                        <Badge variant="outline" className="bg-white">{course}</Badge>
                        <span className="text-muted-foreground">{status as string}</span>
                      </div>
                    ))}
                  </div>
                ) : <p className="text-sm text-muted-foreground">No courses enrolled yet</p>}
              </div>
            </div>
          </CardContent>
        </Card>
      ) : null}

      {/* Tabs */}
      <Tabs value={activeTab} onValueChange={(value) => setActiveTab(value as any)} className="space-y-6">
        <TabsList className="grid w-full grid-cols-4 h-auto">
          <TabsTrigger value="overview" className="py-3">
            <div className="flex flex-col items-center gap-1">
              <span className="text-base">Overview</span>
            </div>
          </TabsTrigger>
          <TabsTrigger value="courses" className="py-3">
            <div className="flex flex-col items-center gap-1">
              <BookOpen className="w-4 h-4" />
              <span className="text-base">Courses</span>
            </div>
          </TabsTrigger>
          <TabsTrigger value="pathway" className="py-3">
            <div className="flex flex-col items-center gap-1">
              <TrendingUp className="w-4 h-4" />
              <span className="text-base">Career Path</span>
            </div>
          </TabsTrigger>
          <TabsTrigger value="leadership" className="py-3">
            <div className="flex flex-col items-center gap-1">
              <Crown className="w-4 h-4" />
              <span className="text-base">Leadership</span>
            </div>
          </TabsTrigger>
        </TabsList>

        {/* Overview Tab */}
        <TabsContent value="overview" className="space-y-4">
          <Card className="border-2 border-[#4167B1]">
            <CardHeader>
              <CardTitle className="text-2xl">Welcome to Your Career Dashboard</CardTitle>
              <CardDescription className="text-base">Explore your personalized career development resources using the tabs above</CardDescription>
            </CardHeader>
            <CardContent className="space-y-4">
              <div className="grid md:grid-cols-3 gap-4">
                <div className="flex items-start gap-3">
                  <div className="w-10 h-10 bg-blue-100 rounded-lg flex items-center justify-center shrink-0">
                    <BookOpen className="w-5 h-5 text-blue-600" />
                  </div>
                  <div>
                    <h3 className="font-semibold">Courses</h3>
                    <p className="text-sm text-muted-foreground">Discover tailored learning paths matched to your skills and goals</p>
                  </div>
                </div>
                <div className="flex items-start gap-3">
                  <div className="w-10 h-10 bg-green-100 rounded-lg flex items-center justify-center shrink-0">
                    <TrendingUp className="w-5 h-5 text-green-600" />
                  </div>
                  <div>
                    <h3 className="font-semibold">Career Path</h3>
                    <p className="text-sm text-muted-foreground">Map your growth journey with short, mid, and long-term goals</p>
                  </div>
                </div>
                <div className="flex items-start gap-3">
                  <div className="w-10 h-10 bg-purple-100 rounded-lg flex items-center justify-center shrink-0">
                    <Crown className="w-5 h-5 text-purple-600" />
                  </div>
                  <div>
                    <h3 className="font-semibold">Leadership</h3>
                    <p className="text-sm text-muted-foreground">Assess your leadership potential and get personalized recommendations</p>
                  </div>
                </div>
              </div>
            </CardContent>
          </Card>
        </TabsContent>

        {/* Courses Tab */}
        <TabsContent value="courses" className="space-y-4">
          {courses.length === 0 ? (
            <Card className="border-2 border-dashed border-gray-300">
              <CardContent className="p-12 text-center">
                <BookOpen className="w-12 h-12 mx-auto mb-4 text-gray-400" />
                <p className="text-gray-600">Click "View Courses" to load your personalized course recommendations</p>
                <Button onClick={fetchCourses} className="mt-4" disabled={loading}>
                  {loading ? 'Loading...' : 'Load Courses'}
                </Button>
              </CardContent>
            </Card>
          ) : (
            <>
              <div className="flex items-center justify-between gap-3">
                <div className="flex items-center gap-3">
                  <BookOpen className="w-6 h-6 text-blue-600" />
                  <h2 className="text-2xl font-bold">Recommended Courses</h2>
                </div>
                <Button onClick={fetchCourses} variant="outline" size="sm" disabled={loading}>
                  {loading ? 'Regenerating...' : 'Regenerate'}
                </Button>
              </div>
              
              {coursesAnalysis && (
                <Card className="border-2 border-blue-200 bg-blue-50/50">
                  <CardHeader>
                    <CardTitle className="flex items-center gap-2">
                      <Lightbulb className="w-5 h-5" /> Analysis
                    </CardTitle>
                    <CardDescription className="text-base text-gray-700">{coursesAnalysis}</CardDescription>
                  </CardHeader>
                </Card>
              )}

              <div className="grid gap-4">
                {courses.map((course, idx) => (
                  <Card key={idx} className="border border-[#D0E8F5] hover:shadow-md transition-shadow">
                    <CardHeader>
                      <div className="flex items-start justify-between gap-4">
                        <div className="flex-1">
                          <CardTitle className="text-xl">{course.title}</CardTitle>
                          <CardDescription className="mt-2">{course.reason}</CardDescription>
                        </div>
                        <Button 
                          variant="outline" 
                          size="sm"
                          onClick={() => window.open(course.url, '_blank')}
                          className="shrink-0"
                        >
                          <ExternalLink className="w-4 h-4 mr-2" /> View Course
                        </Button>
                      </div>
                      <div className="flex flex-wrap gap-2 mt-3">
                        {course.matched_skills.map(skill => (
                          <Badge key={skill} variant="secondary">{skill}</Badge>
                        ))}
                      </div>
                    </CardHeader>
                    <CardContent>
                      <div className="bg-green-50 border border-green-200 rounded-lg p-3">
                        <p className="text-sm font-medium text-green-900">Expected Outcome:</p>
                        <p className="text-sm text-green-800 mt-1">{course.expected_outcome}</p>
                      </div>
                    </CardContent>
                  </Card>
                ))}
              </div>
            </>
          )}
        </TabsContent>

        {/* Career Pathway Tab */}
        <TabsContent value="pathway" className="space-y-4">
          {!careerPathway ? (
            <Card className="border-2 border-dashed border-gray-300">
              <CardContent className="p-12 text-center">
                <TrendingUp className="w-12 h-12 mx-auto mb-4 text-gray-400" />
                <p className="text-gray-600">Click "View Pathway" to discover your personalized career development path</p>
                <Button onClick={fetchCareerPathway} className="mt-4" disabled={loading}>
                  {loading ? 'Loading...' : 'Load Career Pathway'}
                </Button>
              </CardContent>
            </Card>
          ) : (
            <>
              <div className="flex items-center justify-between gap-3">
                <div className="flex items-center gap-3">
                  <TrendingUp className="w-6 h-6 text-green-600" />
                  <h2 className="text-2xl font-bold">Career Development Pathway</h2>
                </div>
                <Button onClick={fetchCareerPathway} variant="outline" size="sm" disabled={loading}>
                  {loading ? 'Regenerating...' : 'Regenerate'}
                </Button>
              </div>

              {careerPathway.analysis && (
                <Card className="border-2 border-green-200 bg-green-50/50">
                  <CardHeader>
                    <CardTitle className="flex items-center gap-2">
                      <Lightbulb className="w-5 h-5" /> Analysis
                    </CardTitle>
                    <CardDescription className="text-base text-gray-700">{careerPathway.analysis}</CardDescription>
                  </CardHeader>
                </Card>
              )}

              {careerPathway.career_pathway && (
                <Tabs defaultValue="short_term" className="space-y-4">
                  <TabsList className="grid w-full grid-cols-3">
                    <TabsTrigger value="short_term">Short Term</TabsTrigger>
                    <TabsTrigger value="mid_term">Mid Term</TabsTrigger>
                    <TabsTrigger value="long_term">Long Term</TabsTrigger>
                  </TabsList>

                  {Object.entries(careerPathway.career_pathway).map(([term, data]: any) => (
                    <TabsContent key={term} value={term} className="space-y-4">
                      <Card className="border-2 border-[#4167B1]">
                        <CardHeader>
                          <CardTitle className="text-xl">{term.replace('_', ' ').charAt(0).toUpperCase() + term.replace('_', ' ').slice(1)}</CardTitle>
                          <CardDescription className="text-base font-medium">{data.duration}</CardDescription>
                        </CardHeader>
                        <CardContent className="space-y-4">
                          <div>
                            <h4 className="font-semibold mb-2 flex items-center gap-2">
                              <Target className="w-4 h-4" /> Focus Areas
                            </h4>
                            <div className="flex flex-wrap gap-2">
                              {data.focus.map((item: string, i: number) => (
                                <Badge key={i} className="bg-[#4167B1]">{item}</Badge>
                              ))}
                            </div>
                          </div>

                          <div>
                            <h4 className="font-semibold mb-2">Suggested Actions</h4>
                            <ul className="space-y-2">
                              {data.suggested_actions.map((action: string, i: number) => (
                                <li key={i} className="flex items-start gap-2">
                                  <span className="text-[#4167B1] mt-1">•</span>
                                  <span className="text-sm">{action}</span>
                                </li>
                              ))}
                            </ul>
                          </div>

                          <div className="bg-blue-50 border border-blue-200 rounded-lg p-4">
                            <h4 className="font-semibold mb-2 text-blue-900">Expected Outcomes</h4>
                            <p className="text-sm text-blue-800">{data.expected_outcomes}</p>
                          </div>
                        </CardContent>
                      </Card>
                    </TabsContent>
                  ))}
                </Tabs>
              )}
            </>
          )}
        </TabsContent>

{/* Leadership Tab */}
<TabsContent value="leadership" className="space-y-4">
  {!leadership ? (
    <Card className="border-2 border-dashed border-gray-300">
      <CardContent className="p-12 text-center">
        <Crown className="w-12 h-12 mx-auto mb-4 text-gray-400" />
        <p className="text-gray-600">
          Click "View Assessment" to evaluate your leadership potential
        </p>
        <Button onClick={fetchLeadership} className="mt-4" disabled={loading}>
          {loading ? "Loading..." : "Load Leadership Assessment"}
        </Button>
      </CardContent>
    </Card>
  ) : (
    <>
      <div className="flex items-center justify-between">
        <div className="flex items-center gap-3">
          <Crown className="w-6 h-6 text-purple-600" />
          <h2 className="text-2xl font-bold">Leadership Potential Assessment</h2>
        </div>
        <Button
          onClick={fetchLeadership}
          variant="outline"
          size="sm"
          disabled={loading}
        >
          {loading ? "Regenerating..." : "Regenerate"}
        </Button>
      </div>

      <Card className={`border-2 ${getPotentialColor(leadership.potential_level)}`}>
        <CardHeader>
          <div className="flex items-center justify-between">
            <CardTitle className="text-2xl">
              Leadership Level: {leadership.potential_level}
            </CardTitle>
            <Badge className="text-lg px-4 py-2 bg-white">
              Overall Score: {leadership.leadership_score.overall_score ?? 0}/10
            </Badge>
          </div>
        </CardHeader>
        <CardContent className="space-y-4">
          <p className="text-base">{leadership.leadership_analysis}</p>

          <div className="grid md:grid-cols-3 gap-4 mt-4">
            <Card className="border border-purple-200 p-4 text-center">
              <p className="text-sm text-muted-foreground">Experience</p>
              <p className="text-3xl font-bold text-[#4167B1]">
                {leadership.leadership_score.experience_weight ?? 0}
              </p>
            </Card>
            <Card className="border border-purple-200 p-4 text-center">
              <p className="text-sm text-muted-foreground">Learning Engagement</p>
              <p className="text-3xl font-bold text-[#4167B1]">
                {leadership.leadership_score.learning_engagement_weight ?? 0}
              </p>
            </Card>
            <Card className="border border-purple-200 p-4 text-center">
              <p className="text-sm text-muted-foreground">Soft Skills</p>
              <p className="text-3xl font-bold text-[#4167B1]">
                {leadership.leadership_score.soft_skills_alignment_weight ?? 0}
              </p>
            </Card>
          </div>
        </CardContent>
      </Card>

      <Card className="border-2 border-purple-200">
        <CardHeader>
          <CardTitle>Recommendations for Growth</CardTitle>
        </CardHeader>
        <CardContent>
          <ul className="space-y-3">
            {leadership.recommendations.map((rec, i) => (
              <li
                key={i}
                className="flex items-start gap-3 p-3 bg-purple-50 rounded-lg"
              >
                <span className="text-purple-600 font-bold shrink-0">
                  {i + 1}.
                </span>
                <span className="text-sm">{rec}</span>
              </li>
            ))}
          </ul>
        </CardContent>
      </Card>
    </>
  )}
</TabsContent>
      </Tabs>
    </div>
  );
}
