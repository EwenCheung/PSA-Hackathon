import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '../ui/card';
import { Button } from '../ui/button';
import { Badge } from '../ui/badge';
import { Alert, AlertDescription } from '../ui/alert';
import { 
  Users, Award, 
  Target, Star, CheckCircle2, TrendingUp, Calendar
} from 'lucide-react';

const mentors = [
  {
    id: 'EMP002',
    name: 'Sarah Chen',
    role: 'Senior Product Manager',
    expertise: ['Product Strategy', 'Stakeholder Management', 'Agile'],
    mentees: 2,
    capacity: 3,
    points: 1800,
    rating: 4.9,
    personality: 'Analytical, Supportive',
  },
  {
    id: 'EMP005',
    name: 'David Lee',
    role: 'Junior Engineer',
    expertise: ['System Design', 'Cloud Architecture', 'Leadership'],
    mentees: 3,
    capacity: 3,
    points: 2100,
    rating: 4.8,
    personality: 'Technical, Patient',
  },
  {
    id: 'EMP008',
    name: 'Maria Garcia',
    role: 'Design Lead',
    expertise: ['UX Design', 'Design Systems', 'Team Leadership'],
    mentees: 1,
    capacity: 3,
    points: 1500,
    rating: 5.0,
    personality: 'Creative, Empathetic',
  },
];

const mentees = [
  {
    id: 'EMP001',
    name: 'Alex Johnson',
    role: 'Software Developer',
    goals: ['Become Tech Lead', 'Learn System Design', 'Improve Leadership'],
    personality: 'Eager, Technical',
    matchedWith: null,
  },
  {
    id: 'EMP003',
    name: 'Michael Brown',
    role: 'Designer',
    goals: ['Master UX Research', 'Design Leadership', 'Portfolio Building'],
    personality: 'Creative, Detail-oriented',
    matchedWith: null,
  },
  {
    id: 'EMP009',
    name: 'Jennifer Taylor',
    role: 'Junior Product Manager',
    goals: ['Product Strategy', 'Data Analysis', 'Roadmap Planning'],
    personality: 'Analytical, Organized',
    matchedWith: null,
  },
];

const mentorshipPairs = [
  {
    id: 'PAIR001',
    mentor: {
      id: 'EMP005',
      name: 'David Lee',
      role: 'Junior Engineer',
    },
    mentee: {
      id: 'EMP012',
      name: 'Sarah Martinez',
      role: 'Intern Software Developer',
    },
    startDate: '2025-08-01',
    focusAreas: ['System Architecture', 'Technical Leadership', 'Career Growth'],
    status: 'active',
    progress: 65,
    nextMeeting: '2025-10-24',
    sessionsCompleted: 8,
  },
  {
    id: 'PAIR002',
    mentor: {
      id: 'EMP002',
      name: 'Sarah Chen',
      role: 'Senior Product Manager',
    },
    mentee: {
      id: 'EMP009',
      name: 'Jennifer Taylor',
      role: 'Junior Product Manager',
    },
    startDate: '2025-09-01',
    focusAreas: ['Product Strategy', 'Data Analysis', 'Roadmap Planning'],
    status: 'active',
    progress: 45,
    nextMeeting: '2025-10-22',
    sessionsCompleted: 5,
  },
  {
    id: 'PAIR003',
    mentor: {
      id: 'EMP008',
      name: 'Maria Garcia',
      role: 'Design Lead',
    },
    mentee: {
      id: 'EMP003',
      name: 'Michael Brown',
      role: 'Designer',
    },
    startDate: '2025-07-15',
    focusAreas: ['UX Design', 'Design Systems', 'Portfolio Building'],
    status: 'active',
    progress: 80,
    nextMeeting: '2025-10-20',
    sessionsCompleted: 12,
  },
  {
    id: 'PAIR004',
    mentor: {
      id: 'EMP005',
      name: 'David Lee',
      role: 'Junior Engineer',
    },
    mentee: {
      id: 'EMP013',
      name: 'Michael Wong',
      role: 'Intern Frontend Developer',
    },
    startDate: '2025-07-01',
    focusAreas: ['Team Management', 'Stakeholder Communication'],
    status: 'active',
    progress: 85,
    nextMeeting: '2025-10-26',
    sessionsCompleted: 14,
  },
  {
    id: 'PAIR005',
    mentor: {
      id: 'EMP002',
      name: 'Sarah Chen',
      role: 'Senior Product Manager',
    },
    mentee: {
      id: 'EMP014',
      name: 'Lisa Anderson',
      role: 'Associate Product Manager',
    },
    startDate: '2025-06-01',
    focusAreas: ['Agile Methodology', 'Stakeholder Management'],
    status: 'completed',
    progress: 100,
    nextMeeting: null,
    sessionsCompleted: 16,
  },
];

export default function MentorMatching() {
  const activePairs = mentorshipPairs.filter(pair => pair.status === 'active');
  const completedPairs = mentorshipPairs.filter(pair => pair.status === 'completed');

  return (
    <div className="space-y-6">
      {/* Overview */}
      <div className="grid md:grid-cols-3 gap-4">
        <Card className="border border-[#D0E8F5]">
          <CardHeader className="pb-3">
            <CardTitle className="text-sm text-muted-foreground">Available Mentors</CardTitle>
          </CardHeader>
          <CardContent>
            <div className="text-3xl text-foreground">{mentors.length}</div>
            <p className="text-sm text-muted-foreground">
              {mentors.reduce((acc, m) => acc + (m.capacity - m.mentees), 0)} slots open
            </p>
          </CardContent>
        </Card>

        <Card className="border border-[#D0E8F5]">
          <CardHeader className="pb-3">
            <CardTitle className="text-sm text-muted-foreground">Seeking Mentors</CardTitle>
          </CardHeader>
          <CardContent>
            <div className="text-3xl text-foreground">{mentees.length}</div>
            <p className="text-sm text-muted-foreground">Looking for guidance</p>
          </CardContent>
        </Card>

        <Card className="border border-[#D0E8F5]">
          <CardHeader className="pb-3">
            <CardTitle className="text-sm text-muted-foreground">Active Pairs</CardTitle>
          </CardHeader>
          <CardContent>
            <div className="text-3xl text-foreground">{activePairs.length}</div>
            <p className="text-sm text-green-600">↑ {mentorshipPairs.length - completedPairs.length} this quarter</p>
          </CardContent>
        </Card>
      </div>

      {/* Active Mentorship Pairs */}
      <Card className="border border-[#D0E8F5]">
        <CardHeader className="border-b border-[#E8F3F9]">
          <CardTitle className="flex items-center gap-2">
            <Users className="w-5 h-5" />
            Active Mentorship Pairs
          </CardTitle>
          <CardDescription>Current mentor-mentee relationships and their progress</CardDescription>
        </CardHeader>
        <CardContent className="pt-6 space-y-4">
          {activePairs.map((pair) => (
            <Card key={pair.id} className="border border-[#D0E8F5]">
              <CardContent className="pt-6">
                <div className="flex items-start justify-between mb-4">
                  <div className="flex items-center gap-4">
                    <div className="flex items-center gap-2">
                      <div className="text-center">
                        <div className="w-12 h-12 bg-[#4167B1] rounded-full flex items-center justify-center mb-1">
                          <span className="text-white font-semibold">M</span>
                        </div>
                        <p className="text-xs text-muted-foreground">Mentor</p>
                      </div>
                      <div>
                        <p className="font-semibold">{pair.mentor.name}</p>
                        <p className="text-sm text-muted-foreground">{pair.mentor.role}</p>
                        <p className="text-xs text-muted-foreground">{pair.mentor.id}</p>
                      </div>
                    </div>
                    <div className="text-2xl text-gray-400">→</div>
                    <div className="flex items-center gap-2">
                      <div className="text-center">
                        <div className="w-12 h-12 bg-[#DEF0F9] rounded-full flex items-center justify-center mb-1">
                          <span className="text-[#4167B1] font-semibold">E</span>
                        </div>
                        <p className="text-xs text-muted-foreground">Mentee</p>
                      </div>
                      <div>
                        <p className="font-semibold">{pair.mentee.name}</p>
                        <p className="text-sm text-muted-foreground">{pair.mentee.role}</p>
                        <p className="text-xs text-muted-foreground">{pair.mentee.id}</p>
                      </div>
                    </div>
                  </div>
                  <Badge variant="secondary" className="bg-green-100 text-green-700">
                    <CheckCircle2 className="w-3 h-3 mr-1" />
                    Active
                  </Badge>
                </div>

                <div className="grid md:grid-cols-2 gap-4 mb-4">
                  <div>
                    <p className="text-sm font-medium mb-2">Focus Areas:</p>
                    <div className="flex flex-wrap gap-2">
                      {pair.focusAreas.map((area, idx) => (
                        <Badge key={idx} variant="secondary" className="text-xs">{area}</Badge>
                      ))}
                    </div>
                  </div>
                  <div>
                    <p className="text-sm font-medium mb-2">Stats:</p>
                    <div className="space-y-1 text-sm">
                      <div className="flex items-center gap-2">
                        <Calendar className="w-4 h-4 text-muted-foreground" />
                        <span className="text-muted-foreground">Started:</span>
                        <span>{new Date(pair.startDate).toLocaleDateString('en-US', { month: 'short', day: 'numeric', year: 'numeric' })}</span>
                      </div>
                      <div className="flex items-center gap-2">
                        <CheckCircle2 className="w-4 h-4 text-green-600" />
                        <span className="text-muted-foreground">Sessions:</span>
                        <span>{pair.sessionsCompleted} completed</span>
                      </div>
                      {pair.nextMeeting && (
                        <div className="flex items-center gap-2">
                          <Calendar className="w-4 h-4 text-blue-600" />
                          <span className="text-muted-foreground">Next:</span>
                          <span>{new Date(pair.nextMeeting).toLocaleDateString('en-US', { month: 'short', day: 'numeric' })}</span>
                        </div>
                      )}
                    </div>
                  </div>
                </div>

                <div>
                  <div className="flex items-center justify-between mb-2">
                    <p className="text-sm font-medium flex items-center gap-2">
                      <TrendingUp className="w-4 h-4" />
                      Progress
                    </p>
                    <span className="text-sm font-semibold text-[#4167B1]">{pair.progress}%</span>
                  </div>
                  <div className="w-full bg-gray-200 rounded-full h-2">
                    <div 
                      className="bg-[#4167B1] h-2 rounded-full transition-all"
                      style={{ width: `${pair.progress}%` }}
                    />
                  </div>
                </div>
              </CardContent>
            </Card>
          ))}
        </CardContent>
      </Card>

      {/* Completed Pairs */}
      {completedPairs.length > 0 && (
        <Card className="border border-[#D0E8F5]">
          <CardHeader className="border-b border-[#E8F3F9]">
            <CardTitle className="flex items-center gap-2">
              <Award className="w-5 h-5 text-green-600" />
              Completed Mentorships
            </CardTitle>
            <CardDescription>Successfully completed mentor-mentee relationships</CardDescription>
          </CardHeader>
          <CardContent className="pt-6 space-y-3">
            {completedPairs.map((pair) => (
              <Card key={pair.id} className="border border-green-200 bg-green-50/50">
                <CardContent className="pt-4">
                  <div className="flex items-center justify-between">
                    <div className="flex items-center gap-4">
                      <div className="flex items-center gap-2 text-sm">
                        <span className="font-semibold">{pair.mentor.name}</span>
                        <span className="text-gray-400">→</span>
                        <span className="font-semibold">{pair.mentee.name}</span>
                      </div>
                      <Badge variant="secondary" className="text-xs">
                        {pair.sessionsCompleted} sessions
                      </Badge>
                    </div>
                    <Badge variant="secondary" className="bg-green-600 text-white">
                      <CheckCircle2 className="w-3 h-3 mr-1" />
                      Completed
                    </Badge>
                  </div>
                </CardContent>
              </Card>
            ))}
          </CardContent>
        </Card>
      )}

      {/* Available Mentors */}
      <Card className="border border-[#D0E8F5]">
        <CardHeader className="border-b border-[#E8F3F9]">
          <CardTitle>Available Mentors</CardTitle>
          <CardDescription>Senior employees ready to mentor</CardDescription>
        </CardHeader>
        <CardContent className="pt-6 space-y-4">
          {mentors.map((mentor) => (
            <Card key={mentor.id} className="border border-[#D0E8F5]">
              <CardContent className="pt-6">
                <div className="flex items-start justify-between mb-4">
                  <div>
                    <h3 className="text-lg mb-1">{mentor.name}</h3>
                    <p className="text-sm text-gray-600">{mentor.role} • {mentor.id}</p>
                  </div>
                  <div className="text-right space-y-1">
                    <div className="flex items-center gap-1">
                      <Star className="w-4 h-4 text-yellow-500" />
                      <span>{mentor.rating}</span>
                    </div>
                    <Badge variant="outline">{mentor.points} pts earned</Badge>
                  </div>
                </div>

                <div className="grid md:grid-cols-2 gap-4 mb-4">
                  <div>
                    <p className="text-sm mb-2">Expertise:</p>
                    <div className="flex flex-wrap gap-2">
                      {mentor.expertise.map((skill, idx) => (
                        <Badge key={idx} variant="secondary">{skill}</Badge>
                      ))}
                    </div>
                  </div>
                  <div>
                    <p className="text-sm mb-2">Personality:</p>
                    <Badge variant="outline">{mentor.personality}</Badge>
                  </div>
                </div>

                <div className="flex items-center justify-between text-sm">
                  <span className="text-gray-600">
                    Current Mentees: {mentor.mentees}/{mentor.capacity}
                  </span>
                  {mentor.mentees < mentor.capacity ? (
                    <Badge className="bg-green-100 text-green-700" variant="secondary">
                      Available
                    </Badge>
                  ) : (
                    <Badge variant="outline">At Capacity</Badge>
                  )}
                </div>
              </CardContent>
            </Card>
          ))}
        </CardContent>
      </Card>

      {/* Seeking Mentors */}
      <Card className="border border-[#D0E8F5]">
        <CardHeader className="border-b border-[#E8F3F9]">
          <CardTitle>Employees Seeking Mentors</CardTitle>
          <CardDescription>Team members looking for guidance</CardDescription>
        </CardHeader>
        <CardContent className="pt-6 space-y-4">
          {mentees.map((mentee) => (
            <Card key={mentee.id} className="border border-[#D0E8F5]">
              <CardContent className="pt-6">
                <div className="flex items-start justify-between mb-4">
                  <div>
                    <h3 className="text-lg mb-1">{mentee.name}</h3>
                    <p className="text-sm text-gray-600">{mentee.role} • {mentee.id}</p>
                  </div>
                  <Badge variant="outline">{mentee.personality}</Badge>
                </div>

                <div>
                  <p className="text-sm mb-2">Career Goals:</p>
                  <div className="space-y-1">
                    {mentee.goals.map((goal, idx) => (
                      <div key={idx} className="flex items-start gap-2 text-sm">
                        <Target className="w-4 h-4 mt-0.5 text-[#4167B1]" />
                        <span>{goal}</span>
                      </div>
                    ))}
                  </div>
                </div>
              </CardContent>
            </Card>
          ))}
        </CardContent>
      </Card>

      {/* Point System Info */}
      <Alert>
        <Award className="w-4 h-4" />
        <AlertDescription>
          <strong>Mentor Rewards:</strong> Mentors earn 50 points per mentoring session completed. 
          Mentees can also award points to their mentors for exceptional guidance.
        </AlertDescription>
      </Alert>
    </div>
  );
}
