import { render, screen } from '@testing-library/react'
import { describe, expect, it } from 'vitest'

import { Profile } from './Profile'
import type { Profile as ProfileData } from '../types/content'

const profileFixture: ProfileData = {
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
}

describe('Profile', () => {
  it('renders passed profile content without fetching', () => {
    render(<Profile profile={profileFixture} />)

    expect(screen.getByRole('heading', { name: 'Test Person' })).toBeInTheDocument()
    expect(screen.getByText('Test Engineer')).toBeInTheDocument()
  })

  it('renders an empty state when the profile has no name or title', () => {
    render(<Profile profile={{ ...profileFixture, name: '', title: '' }} />)

    expect(screen.getByText(/no profile content/i)).toBeInTheDocument()
  })

  it('does not render a phone number', () => {
    const { container } = render(<Profile profile={profileFixture} />)

    expect(container.textContent).not.toMatch(/\+?\d{2,}[\d\s-]{6,}/)
  })

  it('allows long profile copy to shrink and wrap on narrow screens', () => {
    render(<Profile profile={profileFixture} />)

    const summary = screen.getByText('A test summary.')
    expect(summary).toHaveClass('break-words')
    expect(summary.parentElement).toHaveClass('min-w-0')
  })
})
