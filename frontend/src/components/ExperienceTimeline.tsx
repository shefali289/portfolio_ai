import { useState } from 'react'

import type { Role } from '../types/content'

interface ExperienceTimelineProps {
  roles: Role[]
}

function period(role: Role) {
  return `${role.start} — ${role.current ? 'Present' : (role.end ?? '')}`
}

export function ExperienceTimeline({ roles }: ExperienceTimelineProps) {
  const [openRole, setOpenRole] = useState<string | null>(null)

  if (roles.length === 0) return <p className="empty-state">No experience content yet.</p>

  return (
    /* A spine runs down the left; each role hangs off it as a node. */
    <div
      className="relative space-y-4 pl-6 sm:pl-8"
      style={{ borderLeft: '1px solid var(--border-subtle)' }}
    >
      {roles.map((role) => {
        const expanded = openRole === role.id
        const panelId = `role-${role.id}`

        return (
          <article key={role.id} className="section-card relative">
            {/* Node on the spine. Current role is filled, past roles hollow. */}
            <span
              aria-hidden
              className="absolute left-[-1.6rem] top-7 h-2.5 w-2.5 rounded-full sm:left-[-2.1rem]"
              style={{
                backgroundColor: role.current ? 'var(--accent)' : 'var(--surface-base)',
                border: '1px solid var(--accent)',
              }}
            />

            <button
              type="button"
              aria-expanded={expanded}
              aria-controls={panelId}
              onClick={() => setOpenRole(expanded ? null : role.id)}
              className="flex min-h-11 w-full items-start justify-between gap-4 text-left"
            >
              <span>
                <span className="card-title block">
                  {role.title} · {role.company}
                </span>
                <span className="meta mt-1.5 block">
                  {period(role)} · {role.location}
                  {role.current && ' · current'}
                </span>
              </span>
              <span
                aria-hidden
                className="text-xl leading-none"
                style={{ color: 'var(--text-signal)' }}
              >
                {expanded ? '−' : '+'}
              </span>
            </button>

            {expanded && (
              <div
                id={panelId}
                className="mt-5 space-y-4 pt-5"
                style={{ borderTop: '1px solid var(--border-subtle)' }}
              >
                <ul className="space-y-3">
                  {role.highlights.map((highlight) => (
                    <li key={highlight} className="body-text flex gap-3">
                      <span aria-hidden style={{ color: 'var(--accent)' }}>
                        ◆
                      </span>
                      <span>{highlight}</span>
                    </li>
                  ))}
                </ul>

                {role.technologies.length > 0 && (
                  <div className="flex flex-wrap gap-2">
                    {role.technologies.map((tech) => (
                      <span key={tech} className="tag">
                        {tech}
                      </span>
                    ))}
                  </div>
                )}

                {role.link && (
                  <a className="text-link" href={role.link}>
                    View related work
                  </a>
                )}
              </div>
            )}
          </article>
        )
      })}
    </div>
  )
}
