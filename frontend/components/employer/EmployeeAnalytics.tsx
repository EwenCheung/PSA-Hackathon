import { useEffect, useMemo, useState } from 'react';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '../ui/card';
import { Badge } from '../ui/badge';
import { Progress } from '../ui/progress';
import { Users, TrendingUp, CheckCircle2, Target, AlertCircle } from 'lucide-react';
import { API_BASE_URL } from '../../lib/env';

interface AnalyticsOverview {
  total_employees: number;
  total_completed_courses: number;
  average_career_progress: number;
}

interface AnalyticsDepartment {
  department_id: string;
  department_name: string;
  employee_count: number;
  average_performance: number;
}

interface AnalyticsEmployee {
  id: string;
  name: string;
  role: string;
  department: string;
  courses_completed: number;
  courses_in_progress: number;
  career_progress_percent: number;
  points: number;
}

export default function EmployeeAnalytics() {
  const [overview, setOverview] = useState<AnalyticsOverview | null>(null);
  const [departments, setDepartments] = useState<AnalyticsDepartment[]>([]);
  const [employees, setEmployees] = useState<AnalyticsEmployee[]>([]);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const controller = new AbortController();

    async function fetchAnalytics() {
      setIsLoading(true);
      setError(null);
      try {
        const [overviewResp, deptResp, employeeResp] = await Promise.all([
          fetch(`${API_BASE_URL}/api/v1/analytics/overview`, { signal: controller.signal }),
          fetch(`${API_BASE_URL}/api/v1/analytics/departments`, { signal: controller.signal }),
          fetch(`${API_BASE_URL}/api/v1/analytics/employees`, { signal: controller.signal }),
        ]);

        if (!overviewResp.ok || !deptResp.ok || !employeeResp.ok) {
          throw new Error('Failed to load analytics data.');
        }

        const [overviewData, departmentData, employeeData] = await Promise.all([
          overviewResp.json(),
          deptResp.json(),
          employeeResp.json(),
        ]);

        setOverview(overviewData);
        setDepartments(departmentData);
        setEmployees(employeeData);
      } catch (fetchError) {
        if ((fetchError as Error).name !== 'AbortError') {
          setError((fetchError as Error).message || 'Unable to load analytics data.');
        }
      } finally {
        setIsLoading(false);
      }
    }

    fetchAnalytics();

    return () => controller.abort();
  }, []);

  const totalDepartments = useMemo(() => departments.length, [departments]);
  const totalCoursesInProgress = useMemo(
    () => employees.reduce((sum, employee) => sum + employee.courses_in_progress, 0),
    [employees]
  );
  const averageDepartmentPerformance = useMemo(() => {
    if (!departments.length) return 0;
    const total = departments.reduce((acc, dept) => acc + dept.average_performance, 0);
    return total / departments.length;
  }, [departments]);

  if (isLoading) {
    return (
      <div className="space-y-6">
        <Card className="border border-[#D0E8F5]">
          <CardContent className="py-12 text-center text-muted-foreground">
            Loading analytics…
          </CardContent>
        </Card>
      </div>
    );
  }

  if (error || !overview) {
    return (
      <Card className="border border-destructive/20 bg-destructive/5">
        <CardHeader>
          <CardTitle className="flex items-center gap-2 text-destructive">
            <AlertCircle className="w-4 h-4" />
            Unable to load analytics
          </CardTitle>
          <CardDescription className="text-destructive">
            {error ?? 'Please try again later.'}
          </CardDescription>
        </CardHeader>
      </Card>
    );
  }

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
            <div className="text-3xl text-foreground">{overview.total_employees.toLocaleString()}</div>
            <p className="text-sm text-muted-foreground">
              Across {totalDepartments || 'no'} department{totalDepartments === 1 ? '' : 's'}
            </p>
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
            <div className="text-3xl text-foreground">
              {overview.total_completed_courses.toLocaleString()}
            </div>
            <p className="text-sm text-muted-foreground">
              {totalCoursesInProgress} course{totalCoursesInProgress === 1 ? '' : 's'} in progress
            </p>
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
            <div className="text-3xl text-foreground">
              {overview.average_career_progress.toFixed(1)}%
            </div>
            <p className="text-sm text-muted-foreground">Company-wide average</p>
          </CardContent>
        </Card>

        <Card className="border border-[#D0E8F5]">
          <CardHeader className="pb-3">
            <CardTitle className="text-sm text-muted-foreground flex items-center gap-2">
              <Target className="w-4 h-4" />
              Avg Dept Performance
            </CardTitle>
          </CardHeader>
          <CardContent>
            <div className="text-3xl text-foreground">{averageDepartmentPerformance.toFixed(1)}%</div>
            <p className="text-sm text-muted-foreground">Blended goal + points score</p>
          </CardContent>
        </Card>
      </div>

      {/* Department Overview */}
      <Card className="border border-[#D0E8F5]">
        <CardHeader className="border-b border-[#E8F3F9]">
          <CardTitle>Department Overview</CardTitle>
          <CardDescription>Performance across departments</CardDescription>
        </CardHeader>
        <CardContent>
          <div className="space-y-4">
            {departments.map((dept) => (
              <div key={dept.department_id} className="space-y-2">
                <div className="flex items-center justify-between">
                  <div className="flex items-center gap-3">
                    <span>{dept.department_name}</span>
                    <Badge variant="outline">{dept.employee_count} employees</Badge>
                  </div>
                  <span className="text-sm">{dept.average_performance.toFixed(1)}%</span>
                </div>
                <Progress value={dept.average_performance} />
              </div>
            ))}
            {!departments.length && (
              <p className="text-sm text-muted-foreground">No departmental data available yet.</p>
            )}
          </div>
        </CardContent>
      </Card>

      {/* Employee Details */}
      <Card className="border border-[#D0E8F5]">
        <CardHeader className="border-b border-[#E8F3F9]">
          <CardTitle>Employee Details</CardTitle>
          <CardDescription>Individual progress and learning activity</CardDescription>
        </CardHeader>
        <CardContent className="pt-6">
          <div className="space-y-4">
            {employees.map((employee) => (
              <Card key={employee.id} className="border border-[#D0E8F5]">
                <CardContent className="pt-6 space-y-4">
                  <div className="flex items-start justify-between">
                    <div>
                      <h3 className="text-lg">{employee.name}</h3>
                      <p className="text-sm text-gray-600">
                        {employee.role} • {employee.department} • {employee.id}
                      </p>
                    </div>
                    <Badge variant="secondary" className="font-medium">
                      {employee.points.toLocaleString()} pts
                    </Badge>
                  </div>

                  <div className="grid grid-cols-1 md:grid-cols-3 gap-4 text-sm">
                    <div className="flex items-center gap-2">
                      <CheckCircle2 className="w-4 h-4 text-green-600" />
                      <div>
                        <p className="text-gray-600">Completed</p>
                        <p>{employee.courses_completed} course{employee.courses_completed === 1 ? '' : 's'}</p>
                      </div>
                    </div>
                    <div className="flex items-center gap-2">
                      <Target className="w-4 h-4 text-[#4167B1]" />
                      <div>
                        <p className="text-gray-600">In Progress</p>
                        <p>{employee.courses_in_progress} course{employee.courses_in_progress === 1 ? '' : 's'}</p>
                      </div>
                    </div>
                    <div className="flex items-center gap-2">
                      <TrendingUp className="w-4 h-4 text-purple-600" />
                      <div>
                        <p className="text-gray-600">Career Progress</p>
                        <p>{employee.career_progress_percent.toFixed(1)}%</p>
                      </div>
                    </div>
                  </div>

                  <div className="space-y-2">
                    <div className="flex items-center justify-between text-sm">
                      <span className="text-gray-600">Career Progress</span>
                      <span>{employee.career_progress_percent.toFixed(1)}%</span>
                    </div>
                    <Progress value={employee.career_progress_percent} />
                  </div>
                </CardContent>
              </Card>
            ))}
            {!employees.length && (
              <Card className="border border-dashed border-[#D0E8F5] bg-muted/30">
                <CardContent className="py-10 text-center text-muted-foreground">
                  No employee analytics available yet.
                </CardContent>
              </Card>
            )}
          </div>
        </CardContent>
      </Card>
    </div>
  );
}
