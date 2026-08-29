import { useMemo, useState } from 'react'

import type { Project } from '../types/content'

interface ProjectGalleryProps {
  projects: Project[]
}

export function ProjectGallery({ projects }: ProjectGalleryProps) {
  const [technology, setTechnology] = useState<string | null>(null)
  const technologies = useMemo(
    () => [...new Set(projects.flatMap((project) => project.technologies))].sort(),
    [projects],
  )
  const visible = technology
    ? projects.filter((project) => project.technologies.includes(technology))
    : projects

  if (projects.length === 0) return <p className="empty-state">No projects to show yet.</p>

  return (
    <div className="space-y-6">
      <div aria-label="Filter projects by technology" className="flex flex-wrap gap-2">
        {technologies.map((tech) => (
          <button
            key={tech}
            type="button"
            aria-pressed={technology === tech}
            onClick={() => setTechnology(tech)}
            className="filter-button"
          >
            {tech}
          </button>
        ))}
        <button type="button" onClick={() => setTechnology(null)} className="filter-button">Clear filters</button>
      </div>
      <div className="grid gap-5 md:grid-cols-2">
        {visible.map((project) => (
          <article key={project.id} className="section-card flex flex-col">
            <p className="text-sm font-medium text-cyan-700">{project.context} · {project.date}</p>
            <h3 className="mt-2 text-xl font-semibold text-slate-950">{project.name}</h3>
            <p className="mt-3 flex-1 leading-7 text-slate-700">{project.description}</p>
            <div className="mt-5 flex flex-wrap gap-2">{project.technologies.map((tech) => <span key={tech} className="tag">{tech}</span>)}</div>
            {(project.links.demo || project.links.repo) && (
              <div className="mt-5 flex gap-4">
                {project.links.demo && <a className="text-link" href={project.links.demo}>Live demo</a>}
                {project.links.repo && <a className="text-link" href={project.links.repo}>Repository</a>}
              </div>
            )}
          </article>
        ))}
      </div>
    </div>
  )
}
