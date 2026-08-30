import { render, screen } from '@testing-library/react'
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
        { name: 'Python' },
        { name: 'Java' },
      ],
    }],
  },
  projects: { projects: [] },
  engineering_notes: {
    _note: null, achievements: [], building: [], learning: [], beyond: [], todo: [],
  },
}

describe('SkillsExplorer', () => {
  it('lists every skill in its resume group', () => {
    render(<SkillsExplorer content={content} />)

    expect(screen.getByRole('heading', { name: 'Programming' })).toBeInTheDocument()
    expect(screen.getByText('Python')).toBeInTheDocument()
    expect(screen.getByText('Java')).toBeInTheDocument()
  })

  it('shows no ratings, percentages or usage claims', () => {
    const { container } = render(<SkillsExplorer content={content} />)

    // The resume says which skills exist, not how good or where used.
    expect(container.textContent).not.toMatch(/\d+%/)
    expect(container.textContent).not.toMatch(/evidence/i)
    expect(container.textContent).not.toMatch(/content\/\w+\.json/)
  })

  it('renders an honest empty state', () => {
    render(<SkillsExplorer content={{ ...content, skills: { _note: null, groups: [] } }} />)
    expect(screen.getByText(/no skills to show/i)).toBeInTheDocument()
  })
})
