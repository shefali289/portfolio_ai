import { render, screen } from '@testing-library/react'
import userEvent from '@testing-library/user-event'
import { describe, expect, it } from 'vitest'

import { SkillsExplorer } from './SkillsExplorer'

const content = {
  profile: {
    name: 'Test Person', title: 'Engineer', location: '', summary: '',
    links: { email: '', linkedin: '', github: '' },
    education: [], certifications: [], languages: [],
  },
  experience: {
    roles: [{
      id: 'role-1', title: 'AI Engineer', company: 'Test Company', location: '',
      start: '2025-01', end: null, current: true, highlights: [],
      technologies: ['Python'], link: null,
    }],
  },
  skills: {
    _note: null,
    groups: [{
      id: 'programming', name: 'Programming', skills: [
        { name: 'Python', evidence: [{ type: 'role', ref: 'role-1' }], todo: null },
        { name: 'Java', evidence: [], todo: 'TODO: evidence not stated' },
      ],
    }],
  },
  projects: { projects: [] },
  engineering_notes: {
    _note: null, achievements: [], building: [], learning: [], beyond: [], todo: [],
  },
}

describe('SkillsExplorer', () => {
  it('reveals resume-backed evidence without percentage bars', async () => {
    const user = userEvent.setup()
    const { container } = render(<SkillsExplorer content={content} />)

    await user.click(screen.getByRole('button', { name: 'Python' }))
    expect(screen.getByText(/ai engineer at test company/i)).toBeInTheDocument()
    expect(container.textContent).not.toMatch(/\d+%/)
  })

  it('shows an honest status for a skill with no evidence', async () => {
    const user = userEvent.setup()
    render(<SkillsExplorer content={content} />)

    await user.click(screen.getByRole('button', { name: 'Java' }))
    expect(screen.getByText(/evidence not yet documented/i)).toBeInTheDocument()
    expect(screen.queryByText(/todo:/i)).not.toBeInTheDocument()
  })

  it('renders an honest empty state', () => {
    render(<SkillsExplorer content={{ ...content, skills: { _note: null, groups: [] } }} />)
    expect(screen.getByText(/no skills to show/i)).toBeInTheDocument()
  })
})

describe('SkillsExplorer — evidence explorer', () => {
  it('labels a skill that has no evidence as unproven', () => {
    render(<SkillsExplorer content={content} />)

    // Honesty is the design statement: unproven skills are shown, not hidden.
    expect(screen.getByRole('button', { name: /java/i })).toHaveAttribute(
      'data-proven',
      'false',
    )
    expect(screen.getByRole('button', { name: /python/i })).toHaveAttribute(
      'data-proven',
      'true',
    )
  })

  it('summarises how much of the skill set is evidence-backed', () => {
    render(<SkillsExplorer content={content} />)

    expect(screen.getByText(/1 of 2 skills evidenced/i)).toBeInTheDocument()
  })

  it('selecting a second skill closes the first', async () => {
    const user = userEvent.setup()
    render(<SkillsExplorer content={content} />)

    await user.click(screen.getByRole('button', { name: 'Python' }))
    expect(screen.getByText(/ai engineer at test company/i)).toBeInTheDocument()

    await user.click(screen.getByRole('button', { name: 'Java' }))
    expect(screen.queryByText(/ai engineer at test company/i)).not.toBeInTheDocument()
  })

  it('names the source file the evidence comes from', async () => {
    const user = userEvent.setup()
    render(<SkillsExplorer content={content} />)

    await user.click(screen.getByRole('button', { name: 'Python' }))
    expect(screen.getByText(/content\/experience\.json/i)).toBeInTheDocument()
  })
})
