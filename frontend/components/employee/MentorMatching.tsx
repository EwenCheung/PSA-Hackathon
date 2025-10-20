import { useState } from 'react';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '../ui/card';
import { Button } from '../ui/button';
import { Badge } from '../ui/badge';
import { Alert, AlertDescription } from '../ui/alert';
import { Input } from '../ui/input';
import { Textarea } from '../ui/textarea';
import { Tabs, TabsContent, TabsList, TabsTrigger } from '../ui/tabs';
import { 
  Users, Star, Target, BookOpen, MessageSquare, 
  CheckCircle, Award, TrendingUp, Search, UserCheck,
  Clock, ThumbsUp, ThumbsDown, Calendar
} from 'lucide-react';

interface MentorMatchingProps {
  employeeId: string;
  employeeData: {
    name: string;
    role: string;
    department: string;
  };
}

interface Mentor {
  id: string;
  name: string;
  role: string;
  department: string;
  expertise: string[];
  rating: number;
  totalMentees: number;
  available: boolean;
  bio: string;
  achievements: string[];
}

interface MentorshipRequest {
  id: string;
  menteeId: string;
  menteeName: string;
  menteeRole: string;
  message: string;
  goals: string[];
  requestedDate: string;
  status: 'pending' | 'accepted' | 'declined';
}

interface ActiveMentee {
  id: string;
  name: string;
  role: string;
  startDate: string;
  goals: string[];
  progress: number;
  lastMeeting: string;
  nextMeeting: string;
}

const availableMentors: Mentor[] = [
  {
    id: 'MENT001',
    name: 'Sarah Chen',
    role: 'Senior Product Manager',
    department: 'Product',
    expertise: ['Product Strategy', 'Stakeholder Management', 'Agile', 'Data Analysis'],
    rating: 4.9,
    totalMentees: 8,
    available: true,
    bio: 'Passionate about developing future product leaders. 10+ years in product management.',
    achievements: ['Led 3 successful product launches', 'Mentored 8 PMs to senior roles'],
  },
  {
    id: 'MENT002',
    name: 'David Lee',
    role: 'Principal Engineer',
    department: 'Engineering',
    expertise: ['System Design', 'Cloud Architecture', 'Leadership', 'Code Review'],
    rating: 4.8,
    totalMentees: 12,
    available: true,
    bio: 'Focused on helping engineers grow their technical and leadership skills.',
    achievements: ['Architected core platform', 'Promoted 5 engineers to senior level'],
  },
  {
    id: 'MENT003',
    name: 'Maria Garcia',
    role: 'Design Lead',
    department: 'Design',
    expertise: ['UX Design', 'Design Systems', 'User Research', 'Team Leadership'],
    rating: 5.0,
    totalMentees: 6,
    available: false,
    bio: 'Advocate for user-centered design and mentoring emerging design talent.',
    achievements: ['Built design system', 'Won 2 design awards'],
  },
  {
    id: 'MENT004',
    name: 'James Wilson',
    role: 'Engineering Manager',
    department: 'Engineering',
    expertise: ['Technical Leadership', 'Career Development', 'Team Management', 'Performance'],
    rating: 4.7,
    totalMentees: 10,
    available: true,
    bio: 'Helping engineers transition into leadership roles and achieve their career goals.',
    achievements: ['Grew team from 5 to 20', 'Mentored 4 new managers'],
  },
];

const goalCategories = [
  { id: 'technical', label: 'Technical Skills', icon: BookOpen },
  { id: 'leadership', label: 'Leadership', icon: Users },
  { id: 'career', label: 'Career Growth', icon: TrendingUp },
  { id: 'communication', label: 'Communication', icon: MessageSquare },
];

// Mock data - employee is also a mentor
const isMentor = true;

const mockPendingRequests: MentorshipRequest[] = [
  {
    id: 'REQ001',
    menteeId: 'EMP010',
    menteeName: 'John Smith',
    menteeRole: 'Junior Developer',
    message: 'Hi! I\'m looking to improve my system design skills and leadership abilities. I\'ve been following your work and would love to learn from your experience.',
    goals: ['Technical Skills', 'System Design', 'Leadership'],
    requestedDate: '2025-10-15',
    status: 'pending',
  },
  {
    id: 'REQ002',
    menteeId: 'EMP011',
    menteeName: 'Emily Chen',
    menteeRole: 'Software Developer',
    message: 'I\'m transitioning to a senior role and need guidance on technical leadership and code reviews. Your expertise would be invaluable.',
    goals: ['Leadership', 'Career Growth', 'Code Review'],
    requestedDate: '2025-10-16',
    status: 'pending',
  },
];

const mockActiveMentees: ActiveMentee[] = [
  {
    id: 'EMP012',
    name: 'Sarah Martinez',
    role: 'Mid-level Developer',
    startDate: '2025-08-01',
    goals: ['System Architecture', 'Technical Leadership', 'Career Growth'],
    progress: 65,
    lastMeeting: '2025-10-10',
    nextMeeting: '2025-10-24',
  },
  {
    id: 'EMP013',
    name: 'Michael Wong',
    role: 'Senior Developer',
    startDate: '2025-07-15',
    goals: ['Team Management', 'Stakeholder Communication'],
    progress: 80,
    lastMeeting: '2025-10-12',
    nextMeeting: '2025-10-26',
  },
];

export default function MentorMatching({ employeeId, employeeData }: MentorMatchingProps) {
  const [viewMode, setViewMode] = useState<'find' | 'manage'>('find');
  const [selectedGoals, setSelectedGoals] = useState<string[]>([]);
  const [customGoal, setCustomGoal] = useState('');
  const [searchTerm, setSearchTerm] = useState('');
  const [selectedMentor, setSelectedMentor] = useState<string | null>(null);
  const [requestMessage, setRequestMessage] = useState('');
  const [showRequestForm, setShowRequestForm] = useState(false);
  const [requestSent, setRequestSent] = useState(false);
  const [requests, setRequests] = useState<MentorshipRequest[]>(mockPendingRequests);
  const [mentees, setMentees] = useState<ActiveMentee[]>(mockActiveMentees);

  const handleGoalToggle = (goal: string) => {
    setSelectedGoals(prev =>
      prev.includes(goal)
        ? prev.filter(g => g !== goal)
        : [...prev, goal]
    );
  };

  const handleAddCustomGoal = () => {
    if (customGoal.trim() && !selectedGoals.includes(customGoal.trim())) {
      setSelectedGoals(prev => [...prev, customGoal.trim()]);
      setCustomGoal('');
    }
  };

  const handleRequestMentorship = (mentorId: string) => {
    setSelectedMentor(mentorId);
    setShowRequestForm(true);
    setRequestSent(false);
  };

  const handleSubmitRequest = () => {
    if (selectedMentor && requestMessage.trim()) {
      setRequestSent(true);
      setTimeout(() => {
        setShowRequestForm(false);
        setRequestMessage('');
        setSelectedMentor(null);
      }, 2000);
    }
  };

  const handleAcceptRequest = (requestId: string) => {
    setRequests(prev =>
      prev.map(req =>
        req.id === requestId ? { ...req, status: 'accepted' as const } : req
      )
    );
    const acceptedRequest = requests.find(req => req.id === requestId);
    if (acceptedRequest) {
      const newMentee: ActiveMentee = {
        id: acceptedRequest.menteeId,
        name: acceptedRequest.menteeName,
        role: acceptedRequest.menteeRole,
        startDate: new Date().toISOString().split('T')[0],
        goals: acceptedRequest.goals,
        progress: 0,
        lastMeeting: 'Not scheduled',
        nextMeeting: 'To be scheduled',
      };
      setMentees(prev => [...prev, newMentee]);
    }
  };

  const handleDeclineRequest = (requestId: string) => {
    setRequests(prev =>
      prev.map(req =>
        req.id === requestId ? { ...req, status: 'declined' as const } : req
      )
    );
  };

  const filteredMentors = availableMentors.filter(mentor =>
    mentor.name.toLowerCase().includes(searchTerm.toLowerCase()) ||
    mentor.role.toLowerCase().includes(searchTerm.toLowerCase()) ||
    mentor.expertise.some(skill => skill.toLowerCase().includes(searchTerm.toLowerCase()))
  );

  const recommendedMentors = availableMentors
    .filter(mentor => 
      mentor.available && 
      (mentor.department === employeeData.department || 
       mentor.expertise.some(skill => 
         selectedGoals.some(goal => 
           goal.toLowerCase().includes(skill.toLowerCase())
         )
       ))
    )
    .slice(0, 3);

  return (
    <div className="space-y-6">
      {/* Header Section */}
      <div className="flex items-center justify-between">
        <div>
          <h2 className="text-3xl font-bold">
            {isMentor ? 'Mentorship Hub' : 'Find Your Mentor'}
          </h2>
          <p className="text-muted-foreground mt-1">
            {isMentor 
              ? 'Manage your mentees and find mentors for your own growth'
              : 'Connect with experienced professionals to accelerate your career growth'
            }
          </p>
        </div>
        <Badge variant="secondary" className="text-lg px-4 py-2">
          <Users className="w-4 h-4 mr-2" />
          {availableMentors.filter(m => m.available).length} Available Mentors
        </Badge>
      </div>

      {/* Success Alert */}
      {requestSent && (
        <Alert className="bg-green-50 border-green-200">
          <CheckCircle className="h-4 w-4 text-green-600" />
          <AlertDescription className="text-green-800">
            Mentorship request sent successfully! You'll receive a response within 48 hours.
          </AlertDescription>
        </Alert>
      )}

      {/* Tabs for Mentor/Mentee view */}
      {isMentor ? (
        <Tabs value={viewMode} onValueChange={(v) => setViewMode(v as 'find' | 'manage')} className="space-y-6">
          <TabsList className="grid w-full grid-cols-2 max-w-md">
            <TabsTrigger value="find" className="gap-2">
              <Search className="w-4 h-4" />
              Find Mentors
            </TabsTrigger>
            <TabsTrigger value="manage" className="gap-2">
              <UserCheck className="w-4 h-4" />
              My Mentees ({mentees.length})
            </TabsTrigger>
          </TabsList>

          <TabsContent value="find" className="space-y-6">
            <FindMentorView 
              selectedGoals={selectedGoals}
              customGoal={customGoal}
              searchTerm={searchTerm}
              setCustomGoal={setCustomGoal}
              setSearchTerm={setSearchTerm}
              handleGoalToggle={handleGoalToggle}
              handleAddCustomGoal={handleAddCustomGoal}
              handleRequestMentorship={handleRequestMentorship}
              recommendedMentors={recommendedMentors}
              filteredMentors={filteredMentors}
            />
          </TabsContent>

          <TabsContent value="manage" className="space-y-6">
            <ManageMenteesView 
              requests={requests}
              mentees={mentees}
              handleAcceptRequest={handleAcceptRequest}
              handleDeclineRequest={handleDeclineRequest}
            />
          </TabsContent>
        </Tabs>
      ) : (
        <FindMentorView 
          selectedGoals={selectedGoals}
          customGoal={customGoal}
          searchTerm={searchTerm}
          setCustomGoal={setCustomGoal}
          setSearchTerm={setSearchTerm}
          handleGoalToggle={handleGoalToggle}
          handleAddCustomGoal={handleAddCustomGoal}
          handleRequestMentorship={handleRequestMentorship}
          recommendedMentors={recommendedMentors}
          filteredMentors={filteredMentors}
        />
      )}

      {/* Request Form Modal */}
      {showRequestForm && selectedMentor && (
        <div className="fixed inset-0 bg-black/50 flex items-center justify-center z-50">
          <Card className="w-full max-w-lg mx-4">
            <CardHeader>
              <CardTitle>Request Mentorship</CardTitle>
              <CardDescription>
                Send a message to {availableMentors.find(m => m.id === selectedMentor)?.name}
              </CardDescription>
            </CardHeader>
            <CardContent className="space-y-4">
              {selectedGoals.length > 0 && (
                <div>
                  <p className="text-sm font-medium mb-2">Your Goals:</p>
                  <div className="flex flex-wrap gap-2">
                    {selectedGoals.map(goal => (
                      <Badge key={goal} variant="secondary">
                        {goal}
                      </Badge>
                    ))}
                  </div>
                </div>
              )}
              <div>
                <label className="text-sm font-medium">Message</label>
                <Textarea
                  placeholder="Tell the mentor about yourself and why you'd like their guidance..."
                  value={requestMessage}
                  onChange={(e) => setRequestMessage(e.target.value)}
                  rows={5}
                  className="mt-1"
                />
              </div>
              <div className="flex gap-2">
                <Button 
                  variant="outline" 
                  className="flex-1"
                  onClick={() => {
                    setShowRequestForm(false);
                    setSelectedMentor(null);
                    setRequestMessage('');
                  }}
                >
                  Cancel
                </Button>
                <Button 
                  className="flex-1"
                  onClick={handleSubmitRequest}
                  disabled={!requestMessage.trim()}
                >
                  Send Request
                </Button>
              </div>
            </CardContent>
          </Card>
        </div>
      )}
    </div>
  );
}

interface FindMentorViewProps {
  selectedGoals: string[];
  customGoal: string;
  searchTerm: string;
  setCustomGoal: (value: string) => void;
  setSearchTerm: (value: string) => void;
  handleGoalToggle: (goal: string) => void;
  handleAddCustomGoal: () => void;
  handleRequestMentorship: (mentorId: string) => void;
  recommendedMentors: Mentor[];
  filteredMentors: Mentor[];
}

function FindMentorView({
  selectedGoals,
  customGoal,
  searchTerm,
  setCustomGoal,
  setSearchTerm,
  handleGoalToggle,
  handleAddCustomGoal,
  handleRequestMentorship,
  recommendedMentors,
  filteredMentors,
}: FindMentorViewProps) {
  return (
    <>
      {/* Goals Section */}
      <Card>
        <CardHeader>
          <CardTitle className="flex items-center gap-2">
            <Target className="w-5 h-5" />
            Your Mentorship Goals
          </CardTitle>
          <CardDescription>
            Select your development goals to help us recommend the best mentors
          </CardDescription>
        </CardHeader>
        <CardContent className="space-y-4">
          <div className="grid grid-cols-2 md:grid-cols-4 gap-3">
            {goalCategories.map(category => (
              <Button
                key={category.id}
                variant={selectedGoals.includes(category.label) ? 'default' : 'outline'}
                className="h-auto py-3 px-4 flex-col gap-2"
                onClick={() => handleGoalToggle(category.label)}
              >
                <category.icon className="w-5 h-5" />
                <span className="text-sm">{category.label}</span>
              </Button>
            ))}
          </div>

          <div className="flex gap-2">
            <Input
              placeholder="Add custom goal..."
              value={customGoal}
              onChange={(e) => setCustomGoal(e.target.value)}
              onKeyPress={(e) => e.key === 'Enter' && handleAddCustomGoal()}
            />
            <Button onClick={handleAddCustomGoal}>Add</Button>
          </div>

          {selectedGoals.length > 0 && (
            <div className="flex flex-wrap gap-2">
              {selectedGoals.map(goal => (
                <Badge 
                  key={goal} 
                  variant="secondary"
                  className="cursor-pointer hover:bg-destructive hover:text-destructive-foreground"
                  onClick={() => handleGoalToggle(goal)}
                >
                  {goal} ×
                </Badge>
              ))}
            </div>
          )}
        </CardContent>
      </Card>

      {/* Recommended Mentors */}
      {selectedGoals.length > 0 && recommendedMentors.length > 0 && (
        <div>
          <h3 className="text-xl font-semibold mb-4 flex items-center gap-2">
            <Award className="w-5 h-5 text-yellow-500" />
            Recommended for You
          </h3>
          <div className="grid md:grid-cols-3 gap-4">
            {recommendedMentors.map(mentor => (
              <Card key={mentor.id} className="border-primary/50">
                <CardHeader>
                  <div className="flex items-start justify-between">
                    <div>
                      <CardTitle className="text-lg">{mentor.name}</CardTitle>
                      <CardDescription>{mentor.role}</CardDescription>
                    </div>
                    <Badge variant="default" className="bg-yellow-500">
                      <Star className="w-3 h-3 mr-1" />
                      {mentor.rating}
                    </Badge>
                  </div>
                </CardHeader>
                <CardContent className="space-y-3">
                  <p className="text-sm text-muted-foreground line-clamp-2">{mentor.bio}</p>
                  <div className="flex flex-wrap gap-1">
                    {mentor.expertise.slice(0, 3).map(skill => (
                      <Badge key={skill} variant="secondary" className="text-xs">
                        {skill}
                      </Badge>
                    ))}
                  </div>
                  <Button 
                    className="w-full" 
                    onClick={() => handleRequestMentorship(mentor.id)}
                  >
                    Request Mentorship
                  </Button>
                </CardContent>
              </Card>
            ))}
          </div>
        </div>
      )}

      {/* Search and Browse All Mentors */}
      <div>
        <h3 className="text-xl font-semibold mb-4">Browse All Mentors</h3>
        <div className="mb-4">
          <div className="relative">
            <Search className="absolute left-3 top-3 h-4 w-4 text-muted-foreground" />
            <Input
              placeholder="Search by name, role, or expertise..."
              value={searchTerm}
              onChange={(e) => setSearchTerm(e.target.value)}
              className="pl-10"
            />
          </div>
        </div>

        <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-4">
          {filteredMentors.map(mentor => (
            <Card key={mentor.id} className={!mentor.available ? 'opacity-60' : ''}>
              <CardHeader>
                <div className="flex items-start justify-between">
                  <div>
                    <CardTitle className="text-lg">{mentor.name}</CardTitle>
                    <CardDescription>{mentor.role}</CardDescription>
                  </div>
                  <div className="flex flex-col items-end gap-1">
                    <Badge variant="secondary">
                      <Star className="w-3 h-3 mr-1" />
                      {mentor.rating}
                    </Badge>
                    {!mentor.available && (
                      <Badge variant="outline" className="text-xs">
                        Not Available
                      </Badge>
                    )}
                  </div>
                </div>
              </CardHeader>
              <CardContent className="space-y-3">
                <p className="text-sm text-muted-foreground">{mentor.bio}</p>
                <div>
                  <p className="text-xs font-medium mb-1">Expertise:</p>
                  <div className="flex flex-wrap gap-1">
                    {mentor.expertise.map(skill => (
                      <Badge key={skill} variant="secondary" className="text-xs">
                        {skill}
                      </Badge>
                    ))}
                  </div>
                </div>
                <div className="pt-2 border-t">
                  <p className="text-xs text-muted-foreground">
                    {mentor.totalMentees} mentees helped
                  </p>
                  <div className="mt-1 space-y-1">
                    {mentor.achievements.map((achievement, idx) => (
                      <p key={idx} className="text-xs text-muted-foreground flex items-start gap-1">
                        <CheckCircle className="w-3 h-3 mt-0.5 flex-shrink-0" />
                        {achievement}
                      </p>
                    ))}
                  </div>
                </div>
                <Button 
                  className="w-full" 
                  disabled={!mentor.available}
                  onClick={() => handleRequestMentorship(mentor.id)}
                >
                  {mentor.available ? 'Request Mentorship' : 'Currently Unavailable'}
                </Button>
              </CardContent>
            </Card>
          ))}
        </div>
      </div>
    </>
  );
}

interface ManageMenteesViewProps {
  requests: MentorshipRequest[];
  mentees: ActiveMentee[];
  handleAcceptRequest: (requestId: string) => void;
  handleDeclineRequest: (requestId: string) => void;
}

function ManageMenteesView({
  requests,
  mentees,
  handleAcceptRequest,
  handleDeclineRequest,
}: ManageMenteesViewProps) {
  const pendingRequestsList = requests.filter(r => r.status === 'pending');

  return (
    <>
      {/* Mentor Stats */}
      <div className="grid md:grid-cols-3 gap-4">
        <Card>
          <CardHeader className="pb-3">
            <CardTitle className="text-sm font-medium text-muted-foreground">Active Mentees</CardTitle>
          </CardHeader>
          <CardContent>
            <div className="text-3xl font-bold">{mentees.length}</div>
          </CardContent>
        </Card>
        <Card>
          <CardHeader className="pb-3">
            <CardTitle className="text-sm font-medium text-muted-foreground">Pending Requests</CardTitle>
          </CardHeader>
          <CardContent>
            <div className="text-3xl font-bold">{pendingRequestsList.length}</div>
          </CardContent>
        </Card>
        <Card>
          <CardHeader className="pb-3">
            <CardTitle className="text-sm font-medium text-muted-foreground">Mentor Rating</CardTitle>
          </CardHeader>
          <CardContent>
            <div className="text-3xl font-bold flex items-center gap-2">
              4.8 <Star className="w-6 h-6 text-yellow-500" />
            </div>
          </CardContent>
        </Card>
      </div>

      {/* Pending Requests */}
      {pendingRequestsList.length > 0 && (
        <div>
          <h3 className="text-xl font-semibold mb-4 flex items-center gap-2">
            <Clock className="w-5 h-5" />
            Pending Requests ({pendingRequestsList.length})
          </h3>
          <div className="space-y-4">
            {pendingRequestsList.map(request => (
              <Card key={request.id}>
                <CardHeader>
                  <div className="flex items-start justify-between">
                    <div>
                      <CardTitle className="text-lg">{request.menteeName}</CardTitle>
                      <CardDescription>{request.menteeRole}</CardDescription>
                    </div>
                    <Badge variant="outline">
                      {new Date(request.requestedDate).toLocaleDateString()}
                    </Badge>
                  </div>
                </CardHeader>
                <CardContent className="space-y-4">
                  <div>
                    <p className="text-sm font-medium mb-2">Goals:</p>
                    <div className="flex flex-wrap gap-2">
                      {request.goals.map(goal => (
                        <Badge key={goal} variant="secondary">{goal}</Badge>
                      ))}
                    </div>
                  </div>
                  <div>
                    <p className="text-sm font-medium mb-2">Message:</p>
                    <p className="text-sm text-muted-foreground">{request.message}</p>
                  </div>
                  <div className="flex gap-2">
                    <Button 
                      className="flex-1"
                      onClick={() => handleAcceptRequest(request.id)}
                    >
                      <ThumbsUp className="w-4 h-4 mr-2" />
                      Accept
                    </Button>
                    <Button 
                      variant="outline"
                      className="flex-1"
                      onClick={() => handleDeclineRequest(request.id)}
                    >
                      <ThumbsDown className="w-4 h-4 mr-2" />
                      Decline
                    </Button>
                  </div>
                </CardContent>
              </Card>
            ))}
          </div>
        </div>
      )}

      {/* Active Mentees */}
      <div>
        <h3 className="text-xl font-semibold mb-4 flex items-center gap-2">
          <Users className="w-5 h-5" />
          Active Mentees ({mentees.length})
        </h3>
        <div className="grid md:grid-cols-2 gap-4">
          {mentees.map(mentee => (
            <Card key={mentee.id}>
              <CardHeader>
                <div className="flex items-start justify-between">
                  <div>
                    <CardTitle className="text-lg">{mentee.name}</CardTitle>
                    <CardDescription>{mentee.role}</CardDescription>
                  </div>
                  <Badge variant="secondary">
                    Since {new Date(mentee.startDate).toLocaleDateString('en-US', { month: 'short', year: 'numeric' })}
                  </Badge>
                </div>
              </CardHeader>
              <CardContent className="space-y-4">
                <div>
                  <p className="text-sm font-medium mb-2">Focus Areas:</p>
                  <div className="flex flex-wrap gap-2">
                    {mentee.goals.map(goal => (
                      <Badge key={goal} variant="secondary" className="text-xs">{goal}</Badge>
                    ))}
                  </div>
                </div>
                <div>
                  <div className="flex items-center justify-between mb-2">
                    <p className="text-sm font-medium">Progress</p>
                    <span className="text-sm text-muted-foreground">{mentee.progress}%</span>
                  </div>
                  <div className="w-full bg-gray-200 rounded-full h-2">
                    <div 
                      className="bg-primary h-2 rounded-full transition-all"
                      style={{ width: `${mentee.progress}%` }}
                    />
                  </div>
                </div>
                <div className="grid grid-cols-2 gap-4 pt-2 border-t">
                  <div>
                    <p className="text-xs text-muted-foreground mb-1">Last Meeting</p>
                    <p className="text-sm font-medium flex items-center gap-1">
                      <Calendar className="w-3 h-3" />
                      {mentee.lastMeeting}
                    </p>
                  </div>
                  <div>
                    <p className="text-xs text-muted-foreground mb-1">Next Meeting</p>
                    <p className="text-sm font-medium flex items-center gap-1">
                      <Calendar className="w-3 h-3" />
                      {mentee.nextMeeting}
                    </p>
                  </div>
                </div>
                <Button className="w-full" variant="outline">
                  <MessageSquare className="w-4 h-4 mr-2" />
                  Send Message
                </Button>
              </CardContent>
            </Card>
          ))}
        </div>
      </div>

      {/* Accepted/Declined Requests Summary */}
      {requests.some(r => r.status !== 'pending') && (
        <div>
          <h3 className="text-xl font-semibold mb-4">Recent Actions</h3>
          <div className="space-y-2">
            {requests.filter(r => r.status !== 'pending').map(request => (
              <Alert key={request.id} className={request.status === 'accepted' ? 'bg-green-50 border-green-200' : 'bg-gray-50'}>
                <CheckCircle className={`h-4 w-4 ${request.status === 'accepted' ? 'text-green-600' : 'text-gray-600'}`} />
                <AlertDescription>
                  You {request.status} the mentorship request from <strong>{request.menteeName}</strong>
                </AlertDescription>
              </Alert>
            ))}
          </div>
        </div>
      )}
    </>
  );
}
