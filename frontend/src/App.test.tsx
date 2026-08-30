import { render, screen } from '@testing-library/react'
import userEvent from '@testing-library/user-event'
import { beforeEach, describe, expect, it, vi } from 'vitest'

import App from './App'

// The GitHub section fetches on mount, so its stub must be hoisted alongside
// the others; these tests stay about the aggregate content request, and
// GitHubProjects has its own suite.
const { mockGetContent, mockGetProfile, mockGetGithubRepos } = vi.hoisted(() => ({
  mockGetContent: vi.fn(),
  mockGetProfile: vi.fn(() => new Promise(() => {})),
  mockGetGithubRepos: vi.fn(() => Promise.resolve({ repos: [], reason: null })),
}))

vi.mock('./lib/api', () => ({
  getContent: mockGetContent,
  getProfile: mockGetProfile,
  getGithubRepos: mockGetGithubRepos,
}))

const contentFixture = {
  profile: {
    name: 'Test Person',
    title: 'Test Engineer',
    location: 'Auckland, New Zealand',
    summary: 'A test summary.',
    links: {
      email: 'test@example.com',
      linkedin: 'https://linkedin.com/in/test',
      github: 'https://github.com/test',
    },
    education: [],
    certifications: [],
    languages: [],
  },
  experience: { roles: [] },
  skills: { _note: null, groups: [] },
  projects: { projects: [] },
  engineering_notes: {
    _note: null,
    achievements: [],
    building: [],
    learning: [],
    beyond: [],
    todo: [],
  },
}

const pending = () => new Promise<never>(() => {})

describe('App', () => {
  beforeEach(() => {
    vi.clearAllMocks()
  })

  it('shows a page-level loading state while portfolio content is pending', () => {
    mockGetContent.mockReturnValue(pending())

    render(<App />)

    expect(screen.getByRole('status')).toHaveTextContent(/loading portfolio/i)
  })

  it('renders the profile and collection empty states from one response', async () => {
    mockGetContent.mockResolvedValue(contentFixture)

    render(<App />)

    expect(await screen.findByRole('heading', { name: 'Test Person' })).toBeInTheDocument()
    expect(screen.getByText(/no experience content/i)).toBeInTheDocument()
    expect(screen.getByText(/no projects to show/i)).toBeInTheDocument()
    expect(screen.getByText(/no skills to show/i)).toBeInTheDocument()
  })

  it('shows an actionable error and retries the aggregate request', async () => {
    const user = userEvent.setup()
    mockGetContent
      .mockRejectedValueOnce(new Error('network down'))
      .mockResolvedValueOnce(contentFixture)

    render(<App />)

    expect(await screen.findByRole('alert')).toHaveTextContent(/could not load/i)
    await user.click(screen.getByRole('button', { name: /try again/i }))
    expect(await screen.findByRole('heading', { name: 'Test Person' })).toBeInTheDocument()
    expect(mockGetContent).toHaveBeenCalledTimes(2)
  })

  it('omits unsupported narrative sections when their arrays are empty', async () => {
    mockGetContent.mockResolvedValue(contentFixture)

    render(<App />)
    await screen.findByRole('heading', { name: 'Test Person' })

    expect(screen.queryByRole('heading', { name: /what i'm building/i })).not.toBeInTheDocument()
    expect(screen.queryByRole('heading', { name: /what i'm learning/i })).not.toBeInTheDocument()
    expect(screen.queryByRole('heading', { name: /beyond engineering/i })).not.toBeInTheDocument()
  })
})
