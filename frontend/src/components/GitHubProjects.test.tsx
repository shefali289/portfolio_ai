import { render, screen } from '@testing-library/react'
import { beforeEach, describe, expect, it, vi } from 'vitest'

import { GitHubProjects } from './GitHubProjects'
import { getGithubRepos } from '../lib/api'
import type { GithubRepos } from '../types/content'

vi.mock('../lib/api', () => ({ getGithubRepos: vi.fn() }))
const mockedRepos = vi.mocked(getGithubRepos)

const PROFILE_URL = 'https://github.com/test'

const loaded: GithubRepos = {
  repos: [
    {
      name: 'friday',
      description: 'A Python assistant.',
      url: 'https://github.com/test/friday',
      language: 'Python',
      topics: ['ai'],
      pushed_at: '2026-08-01T00:00:00Z',
    },
  ],
  reason: null,
}

const unavailable: GithubRepos = {
  repos: [],
  reason: 'GitHub rate limit reached.',
}

const empty: GithubRepos = { repos: [], reason: null }

const pending = <T,>() => new Promise<T>(() => {})

describe('GitHubProjects', () => {
  beforeEach(() => vi.clearAllMocks())

  it('renders live repositories', async () => {
    mockedRepos.mockResolvedValue(loaded)
    render(<GitHubProjects profileUrl={PROFILE_URL} />)

    expect(await screen.findByText('friday')).toBeInTheDocument()
    expect(screen.getByText(/A Python assistant/)).toBeInTheDocument()
    expect(screen.getByText('Python')).toBeInTheDocument()
  })

  it('links each repository to GitHub', async () => {
    mockedRepos.mockResolvedValue(loaded)
    render(<GitHubProjects profileUrl={PROFILE_URL} />)

    const link = await screen.findByRole('link', { name: /friday/i })
    expect(link).toHaveAttribute('href', 'https://github.com/test/friday')
  })

  it('shows a loading state while the request is in flight', () => {
    mockedRepos.mockReturnValue(pending<GithubRepos>())
    render(<GitHubProjects profileUrl={PROFILE_URL} />)

    expect(screen.getByRole('status')).toBeInTheDocument()
  })

  it('degrades honestly when GitHub is unavailable', async () => {
    mockedRepos.mockResolvedValue(unavailable)
    render(<GitHubProjects profileUrl={PROFILE_URL} />)

    expect(await screen.findByText(/rate limit/i)).toBeInTheDocument()
    // Supplementary content: a fallback link, never a blocking error dialog.
    expect(screen.getByRole('link', { name: /github/i })).toHaveAttribute(
      'href',
      PROFILE_URL,
    )
    expect(screen.queryByRole('alert')).not.toBeInTheDocument()
  })

  it('degrades when the request itself fails', async () => {
    mockedRepos.mockRejectedValue(new Error('network down'))
    render(<GitHubProjects profileUrl={PROFILE_URL} />)

    expect(await screen.findByRole('link', { name: /github/i })).toBeInTheDocument()
  })

  it('shows an honest empty state when there are no repositories', async () => {
    mockedRepos.mockResolvedValue(empty)
    render(<GitHubProjects profileUrl={PROFILE_URL} />)

    expect(await screen.findByText(/no public repositories/i)).toBeInTheDocument()
  })

  it('never invents a repository when the list is empty', async () => {
    mockedRepos.mockResolvedValue(empty)
    render(<GitHubProjects profileUrl={PROFILE_URL} />)

    await screen.findByText(/no public repositories/i)
    expect(screen.queryAllByRole('listitem')).toHaveLength(0)
  })
})
