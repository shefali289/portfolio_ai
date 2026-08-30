import { render, screen } from '@testing-library/react'
import userEvent from '@testing-library/user-event'
import { beforeEach, describe, expect, it, vi } from 'vitest'

import { JobMatch } from './JobMatch'
import { matchJob } from '../lib/api'
import type { JobMatchReport } from '../types/content'

vi.mock('../lib/api', () => ({ matchJob: vi.fn() }))
const mockedMatch = vi.mocked(matchJob)

const report: JobMatchReport = {
  matches: [
    {
      requirement: { text: 'Python', source_line: 'We are hiring a Python engineer.' },
      verdict: 'match',
      evidence: [{ text: 'AI Engineer at Spark.', source: 'AI Engineer · Spark', score: 0.6 }],
    },
  ],
  gaps: [
    {
      requirement: { text: 'Kubernetes', source_line: 'deploy them on Kubernetes.' },
      verdict: 'gap',
      evidence: [],
    },
  ],
  summary: 'Found evidence for 1 requirement of 2. Not evidenced in this portfolio: Kubernetes.',
  steps: [
    { name: 'requirement', label: 'Understanding the role', status: 'done', ms: 1 },
    { name: 'portfolio', label: 'Searching the portfolio', status: 'done', ms: 2 },
    { name: 'evidence', label: 'Weighing the evidence', status: 'done', ms: 3 },
    { name: 'response', label: 'Preparing the response', status: 'done', ms: 4 },
  ],
  provider: 'template',
}

const pending = <T,>() => new Promise<T>(() => {})

async function submit(text = 'We are hiring a Python engineer on Kubernetes.') {
  const user = userEvent.setup()
  render(<JobMatch />)
  await user.type(screen.getByRole('textbox', { name: /job description/i }), text)
  await user.click(screen.getByRole('button', { name: /match/i }))
  return user
}

describe('JobMatch', () => {
  beforeEach(() => vi.clearAllMocks())

  it('lists matched requirements with their evidence', async () => {
    mockedMatch.mockResolvedValue(report)
    await submit()

    expect(await screen.findByText('Python')).toBeInTheDocument()
    expect(screen.getByText(/AI Engineer at Spark/)).toBeInTheDocument()
  })

  it('reports an unevidenced requirement plainly as a gap', async () => {
    mockedMatch.mockResolvedValue(report)
    await submit()

    expect(await screen.findByText('Kubernetes')).toBeInTheDocument()
    // Stated as a gap, not softened into a near-match.
    expect(screen.getByRole('heading', { name: /gaps/i })).toBeInTheDocument()
  })

  it('shows the four chain steps', async () => {
    mockedMatch.mockResolvedValue(report)
    await submit()

    expect(await screen.findByText('Understanding the role')).toBeInTheDocument()
    expect(screen.getByText('Preparing the response')).toBeInTheDocument()
  })

  it('shows a loading state while the chain runs', async () => {
    mockedMatch.mockReturnValue(pending<JobMatchReport>())
    await submit()

    expect(screen.getByRole('status')).toBeInTheDocument()
  })

  it('shows an error state when the request fails', async () => {
    mockedMatch.mockRejectedValue(new Error('network down'))
    await submit()

    expect(await screen.findByRole('alert')).toBeInTheDocument()
  })

  it('does not submit an empty job description', async () => {
    const user = userEvent.setup()
    render(<JobMatch />)

    await user.click(screen.getByRole('button', { name: /match/i }))

    expect(mockedMatch).not.toHaveBeenCalled()
  })
})
