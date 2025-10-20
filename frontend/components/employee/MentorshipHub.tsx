import { useEffect, useMemo, useState } from 'react';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '../ui/card';
import { Badge } from '../ui/badge';
import { Button } from '../ui/button';
import { Alert, AlertDescription } from '../ui/alert';
import { Users, Sparkles, Info, RefreshCcw } from 'lucide-react';

import type { EmployeeProfile, EmployeeDirectoryEntry } from '../../src/types/employee';
import type { MentorMatch } from '../../src/types/mentorship';
import {
  fetchMentors,
  fetchMentorMatch,
  applyForMentor,
  cancelMentorMatch,
} from '../../src/services/mentorship';

interface MentorshipHubProps {
  employee: EmployeeProfile;
}

export default function MentorshipHub({ employee }: MentorshipHubProps) {
  const [mentors, setMentors] = useState<EmployeeDirectoryEntry[]>([]);
  const [currentMatch, setCurrentMatch] = useState<MentorMatch | null>(null);
  const [loading, setLoading] = useState(true);
  const [actionLoading, setActionLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [showExplanation, setShowExplanation] = useState(false);

  useEffect(() => {
    const load = async () => {
      setLoading(true);
      setError(null);
      try {
        const [mentorList, match] = await Promise.all([
          fetchMentors(),
          fetchMentorMatch(employee.id),
        ]);
        setMentors(mentorList);
        setCurrentMatch(match);
      } catch (err) {
        const message = err instanceof Error ? err.message : 'Unable to load mentorship data.';
        setError(message);
      } finally {
        setLoading(false);
      }
    };

    load();
  }, [employee.id]);

  const currentMentorProfile = useMemo(
    () => mentors.find((mentor) => mentor.id === currentMatch?.mentor_id) || null,
    [mentors, currentMatch]
  );

  const handleApply = async (mentorId: string) => {
    setActionLoading(true);
    setError(null);
    try {
      const match = await applyForMentor({ mentee_id: employee.id, mentor_id: mentorId });
      setCurrentMatch(match);
      setShowExplanation(false);
    } catch (err) {
      const message = err instanceof Error ? err.message : 'Unable to apply for mentor.';
      setError(message);
    } finally {
      setActionLoading(false);
    }
  };

  const handleCancel = async () => {
    if (!currentMatch) return;
    setActionLoading(true);
    setError(null);
    try {
      await cancelMentorMatch(employee.id);
      setCurrentMatch(null);
      setShowExplanation(false);
    } catch (err) {
      const message = err instanceof Error ? err.message : 'Unable to cancel mentor request.';
      setError(message);
    } finally {
      setActionLoading(false);
    }
  };

  if (loading) {
    return (
      <Card className="border border-[#D0E8F5]">
        <CardContent className="p-6">Loading mentorship hub...</CardContent>
      </Card>
    );
  }

  return (
    <div className="space-y-6">
      {error && (
        <Alert variant="destructive">
          <Info className="w-4 h-4" />
          <AlertDescription>{error}</AlertDescription>
        </Alert>
      )}

      <Card className="border border-[#D0E8F5]">
        <CardHeader className="flex flex-row items-center justify-between gap-4">
          <div>
            <CardTitle className="flex items-center gap-2 text-lg text-[#4167B1]">
              <Users className="w-5 h-5" />
              Your Mentor Match
            </CardTitle>
            <CardDescription>
              {currentMatch
                ? 'You currently have one active mentor application.'
                : 'Apply to a mentor to start a new mentorship journey.'}
            </CardDescription>
          </div>
          <Button variant="ghost" size="sm" onClick={() => setShowExplanation((v) => !v)} disabled={!currentMatch}>
            <Sparkles className="w-4 h-4 mr-2" />
            {showExplanation ? 'Hide AI reasoning' : 'Show AI reasoning'}
          </Button>
        </CardHeader>
        <CardContent className="space-y-4">
          {currentMatch ? (
            <div className="rounded-lg border border-[#D0E8F5] bg-white p-4">
              <div className="flex items-start justify-between gap-4">
                <div>
                  <h3 className="text-lg font-semibold text-[#4167B1]">
                    {currentMentorProfile?.name ?? currentMatch.mentor_id}
                  </h3>
                  <p className="text-sm text-muted-foreground">
                    {currentMentorProfile?.role ?? 'Mentor'} • Level {currentMentorProfile?.position_level ?? '—'}
                  </p>
                  <p className="text-sm text-muted-foreground mt-1">
                    Submitted on {new Date(currentMatch.created_at).toLocaleString()}
                  </p>
                </div>
                <Badge variant="secondary" className="text-base px-3 py-1">
                  Match {Math.round(currentMatch.match_score * 100)}%
                </Badge>
              </div>

              {showExplanation && (
                <div className="mt-4 rounded-md bg-[#DEF0F9]/40 p-3 text-sm text-[#1a3d62]">
                  {currentMatch.explanation}
                </div>
              )}

              <div className="mt-4 flex items-center gap-2">
                <Button variant="outline" size="sm" onClick={handleCancel} disabled={actionLoading}>
                  <RefreshCcw className="w-4 h-4 mr-2" />
                  Cancel request
                </Button>
                <p className="text-xs text-muted-foreground">
                  Cancelling frees you to apply for a different mentor.
                </p>
              </div>
            </div>
          ) : (
            <div className="rounded-lg border border-dashed border-[#4167B1]/40 bg-[#DEF0F9]/20 p-6 text-center text-sm text-muted-foreground">
              You have not applied for a mentor yet. Choose a mentor below to send your match request.
            </div>
          )}
        </CardContent>
      </Card>

      <Card className="border border-gray-200">
        <CardHeader>
          <CardTitle>Browse Mentors</CardTitle>
          <CardDescription>Select a mentor with a higher position level than you to request guidance.</CardDescription>
        </CardHeader>
        <CardContent className="grid gap-4 md:grid-cols-2">
          {mentors.length === 0 && (
            <div className="rounded-lg border border-dashed border-[#D0E8F5] p-6 text-center text-sm text-muted-foreground">
              No mentors found in the database yet. Seed the employees table to view available mentors.
            </div>
          )}

          {mentors.map((mentor) => {
            const isCurrent = mentor.id === currentMatch?.mentor_id;
            const isHigherLevel = (mentor.position_level ?? 0) > (employee.position_level ?? 0);
            const skills = mentor.skills ? Object.keys(mentor.skills) : [];

            return (
              <Card
                key={mentor.id}
                className={`border ${isCurrent ? 'border-[#4167B1]' : 'border-[#D0E8F5]'}`}
              >
                <CardContent className="space-y-3 p-4">
                  <div className="flex items-start justify-between gap-3">
                    <div>
                      <h3 className="text-lg font-semibold text-[#4167B1]">{mentor.name}</h3>
                      <p className="text-sm text-muted-foreground">
                        {mentor.role ?? 'Mentor'} • Level {mentor.position_level ?? '—'}
                      </p>
                    </div>
                    <Badge variant="outline">{mentor.department_id ?? 'Dept'}</Badge>
                  </div>

                  {skills.length > 0 && (
                    <div className="flex flex-wrap gap-2">
                      {skills.slice(0, 4).map((skill) => (
                        <Badge key={skill} variant="secondary" className="bg-[#DEF0F9] text-[#1a3d62]">
                          {skill}
                        </Badge>
                      ))}
                    </div>
                  )}

                  <div className="flex items-center gap-3">
                    <Badge variant="secondary" className="bg-white text-[#4167B1]">
                      Position Level {mentor.position_level ?? '—'}
                    </Badge>
                    <Badge variant="secondary" className="bg-white text-[#4167B1]">
                      {mentor.points_current} pts
                    </Badge>
                  </div>

                  <Button
                    className="w-full"
                    disabled={actionLoading || !isHigherLevel}
                    onClick={() => handleApply(mentor.id)}
                  >
                    {isCurrent ? 'Update AI match' : 'Apply for mentor'}
                  </Button>
                  {!isHigherLevel && (
                    <p className="text-xs text-muted-foreground">
                      Mentor must have a higher position level than you.
                    </p>
                  )}
                </CardContent>
              </Card>
            );
          })}
        </CardContent>
      </Card>
    </div>
  );
}
