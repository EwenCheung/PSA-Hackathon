import { useState } from 'react';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '../ui/card';
import { Progress } from '../ui/progress';
import { Badge } from '../ui/badge';
import { Button } from '../ui/button';
import { 
  Clock, Target, TrendingUp, Award, 
  CheckCircle2, Circle, BookOpen, Star 
} from 'lucide-react';
import { Tabs, TabsContent, TabsList, TabsTrigger } from '../ui/tabs';

interface CareerPathProps {
  employeeId: string;
  employeeData: any;
  points: number;
  onPointsUpdate: (points: number) => void;
}

const recommendedCourses = [
  {
    id: 1,
    title: 'Advanced React Patterns',
    description: 'Master advanced React concepts including hooks, context, and performance optimization',
    difficulty: 'Advanced',
    duration: '6 weeks',
    effort: '5-7 hours/week',
    points: 150,
    roi: 'High',
    progress: 0,
    status: 'not-started',
    skills: ['React', 'JavaScript', 'Performance'],
  },
  {
    id: 2,
    title: 'System Design Fundamentals',
    description: 'Learn to design scalable systems and prepare for senior roles',
    difficulty: 'Intermediate',
    duration: '8 weeks',
    effort: '4-6 hours/week',
    points: 200,
    roi: 'Very High',
    progress: 35,
    status: 'in-progress',
    skills: ['Architecture', 'Scalability', 'Design'],
  },
  {
    id: 3,
    title: 'Leadership for Engineers',
    description: 'Develop leadership skills to transition into management roles',
    difficulty: 'Intermediate',
    duration: '4 weeks',
    effort: '3-4 hours/week',
    points: 100,
    roi: 'High',
    progress: 100,
    status: 'completed',
    skills: ['Leadership', 'Communication', 'Management'],
  },
  {
    id: 4,
    title: 'Cloud Architecture with AWS',
    description: 'Build and deploy scalable cloud applications',
    difficulty: 'Advanced',
    duration: '10 weeks',
    effort: '6-8 hours/week',
    points: 250,
    roi: 'Very High',
    progress: 0,
    status: 'not-started',
    skills: ['AWS', 'Cloud', 'DevOps'],
  },
];

const careerGoals = [
  { id: 1, goal: 'Become Senior Developer', progress: 65, target: '2025-12-31' },
  { id: 2, goal: 'Lead a Project Team', progress: 40, target: '2026-06-30' },
  { id: 3, goal: 'Master Cloud Technologies', progress: 25, target: '2026-12-31' },
];

export default function CareerPath({ employeeId, employeeData, points, onPointsUpdate }: CareerPathProps) {
  const [courses, setCourses] = useState(recommendedCourses);
  const [selectedCourse, setSelectedCourse] = useState<number | null>(null);

  const handleCompleteCourse = (courseId: number) => {
    setCourses(courses.map(course => 
      course.id === courseId 
        ? { ...course, progress: 100, status: 'completed' }
        : course
    ));
    const course = courses.find(c => c.id === courseId);
    if (course) {
      onPointsUpdate(points + course.points);
    }
  };

  const handleStartCourse = (courseId: number) => {
    setCourses(courses.map(course => 
      course.id === courseId 
        ? { ...course, progress: 10, status: 'in-progress' }
        : course
    ));
  };

  const getDifficultyColor = (difficulty: string) => {
    switch (difficulty) {
      case 'Beginner': return 'border-green-600 text-green-700 bg-green-50';
      case 'Intermediate': return 'border-[#6B9DD6] text-[#4167B1] bg-[#DEF0F9]';
      case 'Advanced': return 'border-[#4167B1] text-[#4167B1] bg-[#DEF0F9]';
      default: return 'bg-muted text-muted-foreground';
    }
  };

  const getRoiColor = (roi: string) => {
    switch (roi) {
      case 'Very High': return 'text-green-600';
      case 'High': return 'text-[#4167B1]';
      case 'Medium': return 'text-[#6B9DD6]';
      default: return 'text-muted-foreground';
    }
  };

  return (
    <div className="space-y-6">
      {/* Career Overview */}
      <div className="grid md:grid-cols-3 gap-4">
        <Card className="border border-[#D0E8F5]">
          <CardHeader className="pb-3">
            <CardTitle className="text-sm text-muted-foreground">Current Level</CardTitle>
          </CardHeader>
          <CardContent>
            <div className="text-2xl text-foreground">{employeeData.level}</div>
            <p className="text-sm text-muted-foreground mt-1">Software Developer</p>
          </CardContent>
        </Card>
        
        <Card className="border border-[#D0E8F5]">
          <CardHeader className="pb-3">
            <CardTitle className="text-sm text-muted-foreground">Courses Completed</CardTitle>
          </CardHeader>
          <CardContent>
            <div className="text-2xl text-foreground">
              {courses.filter(c => c.status === 'completed').length} / {courses.length}
            </div>
            <p className="text-sm text-muted-foreground mt-1">Keep learning!</p>
          </CardContent>
        </Card>

        <Card className="border border-[#D0E8F5]">
          <CardHeader className="pb-3">
            <CardTitle className="text-sm text-muted-foreground">Points Earned</CardTitle>
          </CardHeader>
          <CardContent>
            <div className="text-2xl text-foreground">{points} pts</div>
            <p className="text-sm text-muted-foreground mt-1">From courses & mentoring</p>
          </CardContent>
        </Card>
      </div>

      <Tabs defaultValue="courses" className="space-y-4">
        <TabsList>
          <TabsTrigger value="courses">Recommended Courses</TabsTrigger>
          <TabsTrigger value="goals">Career Goals</TabsTrigger>
        </TabsList>

        <TabsContent value="courses" className="space-y-4">
          {/* Course Filters */}
          <Card className="border border-[#D0E8F5]">
            <CardHeader className="border-b border-[#E8F3F9]">
              <CardTitle>Personalized Course Recommendations</CardTitle>
              <CardDescription>
                Based on your profile, role, and career goals
              </CardDescription>
            </CardHeader>
          </Card>

          {/* Course List */}
          <div className="grid gap-4">
            {courses.map((course) => (
              <Card key={course.id} className={`border border-[#D0E8F5] ${selectedCourse === course.id ? 'border-[#4167B1]' : ''}`}>
                <CardHeader>
                  <div className="flex items-start justify-between">
                    <div className="flex-1">
                      <div className="flex items-center gap-2 mb-2">
                        <CardTitle>{course.title}</CardTitle>
                        {course.status === 'completed' && (
                          <CheckCircle2 className="w-5 h-5 text-green-600" />
                        )}
                      </div>
                      <CardDescription>{course.description}</CardDescription>
                    </div>
                  </div>
                  <div className="flex flex-wrap gap-2 mt-3">
                    <Badge className={getDifficultyColor(course.difficulty)} variant="secondary">
                      {course.difficulty}
                    </Badge>
                    {course.skills.map(skill => (
                      <Badge key={skill} variant="outline">{skill}</Badge>
                    ))}
                  </div>
                </CardHeader>
                <CardContent className="space-y-4">
                  {/* Course Stats */}
                  <div className="grid grid-cols-2 md:grid-cols-4 gap-4 text-sm">
                    <div className="flex items-center gap-2">
                      <Clock className="w-4 h-4 text-gray-500" />
                      <div>
                        <p className="text-gray-600">Duration</p>
                        <p>{course.duration}</p>
                      </div>
                    </div>
                    <div className="flex items-center gap-2">
                      <Target className="w-4 h-4 text-gray-500" />
                      <div>
                        <p className="text-gray-600">Effort</p>
                        <p>{course.effort}</p>
                      </div>
                    </div>
                    <div className="flex items-center gap-2">
                      <TrendingUp className={`w-4 h-4 ${getRoiColor(course.roi)}`} />
                      <div>
                        <p className="text-gray-600">ROI</p>
                        <p className={getRoiColor(course.roi)}>{course.roi}</p>
                      </div>
                    </div>
                    <div className="flex items-center gap-2">
                      <Award className="w-4 h-4 text-gray-500" />
                      <div>
                        <p className="text-gray-600">Reward</p>
                        <p>{course.points} pts</p>
                      </div>
                    </div>
                  </div>

                  {/* Progress */}
                  {course.status !== 'not-started' && (
                    <div className="space-y-2">
                      <div className="flex justify-between text-sm">
                        <span className="text-gray-600">Progress</span>
                        <span>{course.progress}%</span>
                      </div>
                      <Progress value={course.progress} />
                    </div>
                  )}

                  {/* Actions */}
                  <div className="flex gap-2">
                    {course.status === 'not-started' && (
                      <Button onClick={() => handleStartCourse(course.id)}>
                        <BookOpen className="w-4 h-4 mr-2" />
                        Start Course
                      </Button>
                    )}
                    {course.status === 'in-progress' && (
                      <>
                        <Button>Continue Learning</Button>
                        <Button 
                          variant="outline"
                          onClick={() => handleCompleteCourse(course.id)}
                        >
                          Mark Complete
                        </Button>
                      </>
                    )}
                    {course.status === 'completed' && (
                      <Button variant="secondary" disabled>
                        <CheckCircle2 className="w-4 h-4 mr-2" />
                        Completed
                      </Button>
                    )}
                  </div>
                </CardContent>
              </Card>
            ))}
          </div>
        </TabsContent>

        <TabsContent value="goals" className="space-y-4">
          <Card className="border border-[#D0E8F5]">
            <CardHeader className="border-b border-[#E8F3F9]">
              <CardTitle>Your Career Goals</CardTitle>
              <CardDescription>
                Track your progress towards your professional objectives
              </CardDescription>
            </CardHeader>
          </Card>

          <div className="grid gap-4">
            {careerGoals.map((goal) => (
              <Card key={goal.id} className="border border-[#D0E8F5]">
                <CardHeader>
                  <div className="flex items-center justify-between">
                    <CardTitle className="text-lg">{goal.goal}</CardTitle>
                    <Badge variant="outline">
                      Target: {new Date(goal.target).toLocaleDateString()}
                    </Badge>
                  </div>
                </CardHeader>
                <CardContent className="space-y-3">
                  <div className="flex justify-between text-sm">
                    <span className="text-gray-600">Progress</span>
                    <span>{goal.progress}%</span>
                  </div>
                  <Progress value={goal.progress} />
                  <div className="flex items-center gap-2 text-sm text-gray-600">
                    <Star className="w-4 h-4" />
                    <span>
                      {goal.progress >= 75 ? 'Almost there!' : 
                       goal.progress >= 50 ? 'Making great progress' : 
                       'Keep pushing forward'}
                    </span>
                  </div>
                </CardContent>
              </Card>
            ))}
          </div>
        </TabsContent>
      </Tabs>
    </div>
  );
}
