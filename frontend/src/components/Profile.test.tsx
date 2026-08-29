import { render, screen } from '@testing-library/react'
import { beforeEach, describe, expect, it, vi } from 'vitest'

import { Profile } from './Profile'
import { getProfile } from '../lib/api'
import type { Profile as ProfileData } from '../types/content'

vi.mock('../lib/api', () => ({
  getProfile: vi.fn(),
}))

const mockedGetProfile = vi.mocked(getProfile)

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

/** A promise that never settles, so the loading state stays on screen. */
const pending = <T,>() => new Promise<T>(() => {})

describe('Profile', () => {
  beforeEach(() => {
    vi.clearAllMocks()
  })

  it('renders the name and title returned by the API', async () => {
    mockedGetProfile.mockResolvedValue(profileFixture)

    render(<Profile />)

    expect(await screen.findByRole('heading', { name: 'Test Person' })).toBeInTheDocument()
    expect(screen.getByText('Test Engineer')).toBeInTheDocument()
  })

  it('renders the loading state while the request is in flight', () => {
    mockedGetProfile.mockReturnValue(pending<ProfileData>())

    render(<Profile />)

    expect(screen.getByRole('status')).toBeInTheDocument()
  })

  it('renders the error state when the API rejects', async () => {
    mockedGetProfile.mockRejectedValue(new Error('network down'))

    render(<Profile />)

    expect(await screen.findByRole('alert')).toBeInTheDocument()
  })

  it('renders the empty state when the profile has no name', async () => {
    mockedGetProfile.mockResolvedValue({ ...profileFixture, name: '', title: '' })

    render(<Profile />)

    expect(await screen.findByText(/no profile content/i)).toBeInTheDocument()
  })

  it('does not render a phone number', async () => {
    mockedGetProfile.mockResolvedValue(profileFixture)
    const { container } = render(<Profile />)

    await screen.findByRole('heading', { name: 'Test Person' })
    expect(container.textContent).not.toMatch(/\+?\d{2,}[\d\s-]{6,}/)
  })
})
