import { describe, expect, it } from 'vitest'

import { buildEvidenceIndex } from './evidence'

const content = {
  profile: {
    name: 'Test', title: 'Engineer', location: '', summary: '',
    links: { email: '', linkedin: '', github: '' },
    education: [{ id: 'education-1', qualification: 'MIT', institution: 'UoA', location: '', start: '', end: '', grade: '' }],
    certifications: [{ id: 'certification-1', name: 'AI Engineer Associate', issuer: 'Microsoft' }],
    languages: [],
  },
  experience: {
    roles: [{ id: 'role-1', title: 'AI Engineer', company: 'Test Company', location: '', start: '', end: null, current: true, highlights: [], technologies: [], link: null }],
  },
  skills: { _note: null, groups: [] },
  projects: {
    projects: [{ id: 'project-1', name: 'Portfolio', date: '', context: '', description: '', technologies: [], links: { demo: null, repo: null }, todo: null }],
  },
  engineering_notes: {
    _note: null,
    achievements: [{ id: 'achievement-1', name: 'Claude Code in Action', issuer: 'Anthropic Academy' }],
    building: [], learning: [], beyond: [], todo: [],
  },
}

describe('buildEvidenceIndex', () => {
  it('indexes every supported evidence type with a human-readable label', () => {
    const index = buildEvidenceIndex(content)

    expect(index['role:role-1']).toBe('AI Engineer at Test Company')
    expect(index['project:project-1']).toBe('Portfolio')
    expect(index['certification:certification-1']).toBe('AI Engineer Associate — Microsoft')
    expect(index['education:education-1']).toBe('MIT — UoA')
    expect(index['achievement:achievement-1']).toBe('Claude Code in Action — Anthropic Academy')
  })

  it('does not manufacture a label for an unknown reference', () => {
    const index = buildEvidenceIndex(content)
    expect(index['role:missing']).toBeUndefined()
  })
})
