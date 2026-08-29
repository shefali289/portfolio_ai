import { render, screen } from '@testing-library/react'
import userEvent from '@testing-library/user-event'
import { describe, expect, it } from 'vitest'

import { ProjectGallery } from './ProjectGallery'

const projects = [
  {
    id: 'boardscape',
    name: 'Boardscape',
    date: '2022-05',
    context: 'Course project',
    description: 'A social board-game platform.',
    technologies: ['ReactJS', 'NodeJS'],
    links: { demo: null, repo: null },
    todo: null,
  },
  {
    id: 'friday',
    name: 'F.R.I.D.A.Y.',
    date: '2020-06',
    context: 'Personal project',
    description: 'A desktop voice assistant.',
    technologies: ['Python'],
    links: { demo: null, repo: 'https://github.com/test/friday' },
    todo: null,
  },
]

describe('ProjectGallery', () => {
  it('filters by technologies already present in project content and resets', async () => {
    const user = userEvent.setup()
    render(<ProjectGallery projects={projects} />)

    await user.click(screen.getByRole('button', { name: 'ReactJS' }))
    expect(screen.getByRole('heading', { name: 'Boardscape' })).toBeInTheDocument()
    expect(screen.queryByRole('heading', { name: 'F.R.I.D.A.Y.' })).not.toBeInTheDocument()

    await user.click(screen.getByRole('button', { name: /clear filters/i }))
    expect(screen.getByRole('heading', { name: 'F.R.I.D.A.Y.' })).toBeInTheDocument()
  })

  it('renders an honest empty state', () => {
    render(<ProjectGallery projects={[]} />)
    expect(screen.getByText(/no projects to show/i)).toBeInTheDocument()
  })
})
