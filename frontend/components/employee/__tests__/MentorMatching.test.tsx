import { render, screen, waitFor } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import { vi } from 'vitest';

import MentorMatching from '../MentorMatching';

const mocks = vi.hoisted(() => ({
  fetchMentorsMock: vi.fn(),
  fetchMentorByIdMock: vi.fn(),
  fetchMentorshipRequestsMock: vi.fn(),
  fetchMentorshipPairsMock: vi.fn(),
  getMentorRecommendationsMock: vi.fn(),
  createMentorshipRequestMock: vi.fn(),
  updateMentorshipRequestMock: vi.fn(),
  deleteMentorshipRequestMock: vi.fn(),
}));

const {
  fetchMentorsMock,
  fetchMentorByIdMock,
  fetchMentorshipRequestsMock,
  fetchMentorshipPairsMock,
  getMentorRecommendationsMock,
  createMentorshipRequestMock,
  updateMentorshipRequestMock,
  deleteMentorshipRequestMock,
} = mocks;

vi.mock('../../../services/mentoringService', () => ({
  fetchMentors: mocks.fetchMentorsMock,
  fetchMentorById: mocks.fetchMentorByIdMock,
  fetchMentorshipRequests: mocks.fetchMentorshipRequestsMock,
  fetchMentorshipPairs: mocks.fetchMentorshipPairsMock,
  getMentorRecommendations: mocks.getMentorRecommendationsMock,
  createMentorshipRequest: mocks.createMentorshipRequestMock,
  updateMentorshipRequest: mocks.updateMentorshipRequestMock,
  deleteMentorshipRequest: mocks.deleteMentorshipRequestMock,
}));

const mockMentors = [
  {
    employeeId: 'MENTOR123',
    name: 'Dana Mentor',
    role: 'Staff Engineer',
    department: 'Innovation',
    expertiseAreas: ['System Design', 'Coaching'],
    rating: 4.9,
    menteesCount: 1,
    maxMentees: 3,
    isAvailable: true,
    bio: 'Seasoned architect passionate about mentoring.',
    yearsOfExperience: 12,
    achievements: ['Built mentorship program'],
  },
];

const mockPendingRequest = {
  requestId: 'REQ123',
  menteeId: 'EMP200',
  menteeName: 'Taylor Learner',
  menteeRole: 'Software Engineer',
  mentorId: 'MENTOR123',
  mentorName: 'Dana Mentor',
  message: 'Excited to learn more!',
  goals: ['System Design'],
  status: 'pending' as const,
  createdAt: '2024-01-01T00:00:00.000Z',
  respondedAt: null,
};

const mockDeclinedRequest = {
  requestId: 'REQ124',
  menteeId: 'EMP200',
  menteeName: 'Taylor Learner',
  menteeRole: 'Software Engineer',
  mentorId: 'MENTOR456',
  mentorName: 'Morgan Architect',
  message: 'Please mentor me on leadership.',
  goals: ['Leadership'],
  status: 'declined' as const,
  createdAt: '2024-02-01T00:00:00.000Z',
  respondedAt: '2024-02-02T12:00:00.000Z',
};
const mockPairs: any[] = [];

beforeEach(() => {
  fetchMentorsMock.mockResolvedValue(mockMentors);
  fetchMentorByIdMock.mockResolvedValue(mockMentors[0]);
  fetchMentorshipRequestsMock.mockReset();
  fetchMentorshipRequestsMock.mockResolvedValue([]);
  fetchMentorshipPairsMock.mockResolvedValue(mockPairs);
  getMentorRecommendationsMock.mockResolvedValue([]);
  createMentorshipRequestMock.mockResolvedValue({
    requestId: 'REQ123',
    menteeId: 'EMP200',
    mentorId: 'MENTOR123',
    message: 'Thanks!',
    goals: ['System Design'],
    status: 'pending',
    createdAt: '2024-01-01T00:00:00.000Z',
  });
  updateMentorshipRequestMock.mockResolvedValue(null);
  deleteMentorshipRequestMock.mockResolvedValue(undefined);
});

afterEach(() => {
  vi.clearAllMocks();
});

const renderComponent = () =>
  render(
    <MentorMatching
      employeeId="EMP200"
      employeeData={{
        name: 'Taylor Learner',
        role: 'Software Engineer',
        department: 'Innovation',
      }}
    />,
  );

test('loads mentors from the mentoring service', async () => {
  fetchMentorshipRequestsMock
    .mockResolvedValueOnce([])
    .mockResolvedValueOnce([])
    .mockResolvedValueOnce([])
    .mockResolvedValueOnce([mockPendingRequest]);
  renderComponent();

  await waitFor(() => {
    expect(fetchMentorsMock).toHaveBeenCalledWith({ menteeId: 'EMP200' });
  });

  expect(fetchMentorByIdMock).toHaveBeenCalledWith('EMP200');
  expect(fetchMentorshipRequestsMock).toHaveBeenCalledWith('EMP200', undefined);
  expect(fetchMentorshipRequestsMock).toHaveBeenCalledWith(undefined, 'EMP200');
  expect(fetchMentorshipPairsMock).toHaveBeenCalledWith('EMP200', undefined);

  expect(await screen.findByText('Dana Mentor')).toBeInTheDocument();
  expect(await screen.findByText(/application history/i)).toBeInTheDocument();
  expect(screen.getByText(/no mentorship requests yet/i)).toBeInTheDocument();
});

test('shows declined history entries while allowing new pending requests', async () => {
  fetchMentorshipRequestsMock
    .mockResolvedValueOnce([])
    .mockResolvedValueOnce([mockDeclinedRequest, mockPendingRequest])
    .mockResolvedValue([mockDeclinedRequest, mockPendingRequest]);

  renderComponent();

  await screen.findByText('Application History');

  expect(screen.getByText('Morgan Architect')).toBeInTheDocument();
  expect(screen.getByText('Dana Mentor')).toBeInTheDocument();
  expect(screen.getAllByText('Pending').length).toBeGreaterThan(0);
  expect(screen.getByText('Declined')).toBeInTheDocument();
  expect(screen.getByText('Cancel Request')).toBeInTheDocument();
  expect(screen.getByText('Remove from History')).toBeInTheDocument();
});

test('submits mentorship request through the mentoring service', async () => {
  const user = userEvent.setup();
  fetchMentorshipRequestsMock
    .mockResolvedValueOnce([])
    .mockResolvedValueOnce([])
    .mockResolvedValue([]);
  renderComponent();

  await screen.findByText('Dana Mentor');

  const requestButtons = screen.getAllByRole('button', { name: /request mentorship/i });
  await user.click(requestButtons[0]);

  const messageBox = await screen.findByPlaceholderText(
    /tell the mentor about yourself/i,
  );
  await user.type(messageBox, 'Looking forward to learning from you!');

  const sendButton = screen.getByRole('button', { name: /send request/i });
  await user.click(sendButton);

  await waitFor(() => {
    expect(createMentorshipRequestMock).toHaveBeenCalledWith(
      'EMP200',
      'MENTOR123',
      'Looking forward to learning from you!',
      expect.any(Array),
    );
  });

  await waitFor(() => {
    expect(fetchMentorshipRequestsMock).toHaveBeenCalledTimes(4);
    expect(fetchMentorshipPairsMock).toHaveBeenCalledTimes(2);
    expect(fetchMentorsMock).toHaveBeenCalledTimes(2);
  });

  expect(
    screen.getByText(/Mentorship request sent successfully/i),
  ).toBeInTheDocument();

  await waitFor(() => {
    expect(fetchMentorshipRequestsMock).toHaveBeenCalledTimes(4);
  });
});

test('allows cancelling a pending mentorship request from history', async () => {
  const user = userEvent.setup();
  fetchMentorshipRequestsMock
    .mockResolvedValueOnce([mockPendingRequest])
    .mockResolvedValueOnce([mockPendingRequest])
    .mockResolvedValueOnce([mockPendingRequest])
    .mockResolvedValueOnce([]);

  renderComponent();

  const cancelButton = await screen.findByRole('button', { name: /cancel request/i });
  await user.click(cancelButton);

  await waitFor(() => {
    expect(deleteMentorshipRequestMock).toHaveBeenCalledWith('REQ123', 'EMP200');
  });

  await waitFor(() => {
    expect(screen.getByText(/no mentorship requests yet/i)).toBeInTheDocument();
  });
});
