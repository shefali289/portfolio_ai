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
    <div className="space-y-7">
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
        <button type="button" onClick={() => setTechnology(null)} className="filter-button">
          Clear filters
        </button>
      </div>

      <div className="grid gap-5 md:grid-cols-2">
        {visible.map((project, index) => (
          <article key={project.id} className="section-card flex flex-col">
            <div className="flex items-start justify-between gap-4">
              <p className="eyebrow">
                {project.context} · {project.date}
              </p>
              {/* Index numeral: gives the grid an editorial rhythm. */}
              <span aria-hidden className="numeral">
                {String(index + 1).padStart(2, '0')}
              </span>
            </div>

            <h3 className="card-title mt-2 text-xl">{project.name}</h3>
            <p className="body-text mt-3 flex-1">{project.description}</p>

            <div className="mt-5 flex flex-wrap gap-2">
              {project.technologies.map((tech) => (
                <span key={tech} className="tag">
                  {tech}
                </span>
              ))}
            </div>

            {(project.links.demo || project.links.repo) && (
              <div className="mt-5 flex gap-4">
                {project.links.demo && (
                  <a className="text-link" href={project.links.demo}>
                    Live demo
                  </a>
                )}
                {project.links.repo && (
                  <a className="text-link" href={project.links.repo}>
                    Repository
                  </a>
                )}
              </div>
            )}
          </article>
        ))}
      </div>
    </div>
  )
}
