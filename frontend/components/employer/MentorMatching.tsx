import { useState } from 'react';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '../ui/card';
import { Button } from '../ui/button';
import { Badge } from '../ui/badge';
import { Alert, AlertDescription } from '../ui/alert';
import { 
  Users, CheckCircle2, GitMerge, Award, 
  Target, TrendingUp, Star, UserPlus 
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
    role: 'Principal Engineer',
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

const matches = [
  {
    mentorId: 'EMP005',
    mentorName: 'David Lee',
    menteeId: 'EMP001',
    menteeName: 'Alex Johnson',
    matchScore: 95,
    reasons: [
      'Aligned technical expertise',
      'Complementary personality traits',
      'Shared interest in system design',
    ],
  },
  {
    mentorId: 'EMP008',
    mentorName: 'Maria Garcia',
    menteeId: 'EMP003',
    menteeName: 'Michael Brown',
    matchScore: 92,
    reasons: [
      'Design expertise alignment',
      'Similar creative approach',
      'Mentee goals match mentor strengths',
    ],
  },
  {
    mentorId: 'EMP002',
    mentorName: 'Sarah Chen',
    menteeId: 'EMP009',
    menteeName: 'Jennifer Taylor',
    matchScore: 88,
    reasons: [
      'Product management focus',
      'Analytical mindset match',
      'Career trajectory alignment',
    ],
  },
];

export default function MentorMatching() {
  const [selectedMatches, setSelectedMatches] = useState<number[]>([]);
  const [confirmedMatches, setConfirmedMatches] = useState<number[]>([]);

  const handleSelectMatch = (index: number) => {
    if (selectedMatches.includes(index)) {
      setSelectedMatches(selectedMatches.filter(i => i !== index));
    } else {
      setSelectedMatches([...selectedMatches, index]);
    }
  };

  const handleConfirmMatches = () => {
    setConfirmedMatches([...confirmedMatches, ...selectedMatches]);
    setSelectedMatches([]);
  };

  return (
    <div className="space-y-6">
      {/* Overview */}
      <div className="grid md:grid-cols-4 gap-4">
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
            <CardTitle className="text-sm text-muted-foreground">AI Matches</CardTitle>
          </CardHeader>
          <CardContent>
            <div className="text-3xl text-foreground">{matches.length}</div>
            <p className="text-sm text-muted-foreground">High-quality suggestions</p>
          </CardContent>
        </Card>

        <Card className="border border-[#D0E8F5]">
          <CardHeader className="pb-3">
            <CardTitle className="text-sm text-muted-foreground">Active Pairs</CardTitle>
          </CardHeader>
          <CardContent>
            <div className="text-3xl text-foreground">18</div>
            <p className="text-sm text-green-600">↑ 6 this month</p>
          </CardContent>
        </Card>
      </div>

      {/* AI-Suggested Matches */}
      <Card className="border border-gray-200">
        <CardHeader className="border-b border-gray-100">
          <div className="flex items-center justify-between">
            <div>
              <CardTitle className="flex items-center gap-2">
                <GitMerge className="w-5 h-5" />
                AI-Suggested Mentor Matches
              </CardTitle>
              <CardDescription>
                Based on personality, goals, expertise, and availability
              </CardDescription>
            </div>
            {selectedMatches.length > 0 && (
              <Button onClick={handleConfirmMatches}>
                <CheckCircle2 className="w-4 h-4 mr-2" />
                Confirm {selectedMatches.length} Match{selectedMatches.length > 1 ? 'es' : ''}
              </Button>
            )}
          </div>
        </CardHeader>
        <CardContent className="space-y-4">
          {matches.map((match, index) => {
            const isSelected = selectedMatches.includes(index);
            const isConfirmed = confirmedMatches.includes(index);

            return (
              <Card 
                key={index} 
                className={`border border-[#D0E8F5] ${isSelected ? 'border-[#4167B1]' : ''} ${isConfirmed ? 'opacity-60' : ''}`}
              >
                <CardContent className="pt-6">
                  <div className="flex items-start justify-between mb-4">
                    <div className="flex items-center gap-4">
                      <div className="flex flex-col items-center">
                        <div className="w-12 h-12 bg-[#DEF0F9] rounded-full flex items-center justify-center mb-1">
                          <Users className="w-6 h-6 text-[#4167B1]" />
                        </div>
                        <Badge variant="secondary" className="gap-1">
                          <Star className="w-3 h-3" />
                          {match.matchScore}%
                        </Badge>
                      </div>
                      <div>
                        <div className="flex items-center gap-2 mb-2">
                          <span>{match.mentorName}</span>
                          <span className="text-gray-400">→</span>
                          <span>{match.menteeName}</span>
                        </div>
                        <div className="text-sm text-gray-600">
                          Mentor to Mentee pairing
                        </div>
                      </div>
                    </div>
                    {!isConfirmed && (
                      <Button
                        variant={isSelected ? 'default' : 'outline'}
                        onClick={() => handleSelectMatch(index)}
                      >
                        {isSelected ? (
                          <>
                            <CheckCircle2 className="w-4 h-4 mr-2" />
                            Selected
                          </>
                        ) : (
                          <>
                            <UserPlus className="w-4 h-4 mr-2" />
                            Select
                          </>
                        )}
                      </Button>
                    )}
                    {isConfirmed && (
                      <Badge variant="secondary" className="gap-1">
                        <CheckCircle2 className="w-3 h-3" />
                        Confirmed
                      </Badge>
                    )}
                  </div>

                  <div className="space-y-2">
                    <p className="text-sm">Match Reasons:</p>
                    <div className="space-y-1">
                      {match.reasons.map((reason, idx) => (
                        <div key={idx} className="flex items-start gap-2 text-sm">
                          <CheckCircle2 className="w-4 h-4 mt-0.5 text-green-600" />
                          <span>{reason}</span>
                        </div>
                      ))}
                    </div>
                  </div>
                </CardContent>
              </Card>
            );
          })}
        </CardContent>
      </Card>

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
