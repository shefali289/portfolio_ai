import { render, screen } from '@testing-library/react'
import userEvent from '@testing-library/user-event'
import { describe, expect, it } from 'vitest'

import { ExperienceTimeline } from './ExperienceTimeline'

const role = {
  id: 'role-1',
  title: 'AI Engineer',
  company: 'Test Company',
  location: 'Auckland',
  start: '2025-01',
  end: null,
  current: true,
  highlights: ['Built a grounded portfolio.'],
  technologies: ['Python'],
  link: null,
}

describe('ExperienceTimeline', () => {
  it('expands and collapses a role with a semantic button', async () => {
    const user = userEvent.setup()
    render(<ExperienceTimeline roles={[role]} />)

    const trigger = screen.getByRole('button', { name: /ai engineer.*test company/i })
    expect(trigger).toHaveAttribute('aria-expanded', 'false')
    expect(screen.queryByText('Built a grounded portfolio.')).not.toBeInTheDocument()

    await user.click(trigger)
    expect(trigger).toHaveAttribute('aria-expanded', 'true')
    expect(screen.getByText('Built a grounded portfolio.')).toBeInTheDocument()

    await user.click(trigger)
    expect(screen.queryByText('Built a grounded portfolio.')).not.toBeInTheDocument()
  })

  it('renders an honest empty state', () => {
    render(<ExperienceTimeline roles={[]} />)
    expect(screen.getByText(/no experience content/i)).toBeInTheDocument()
  })
})
