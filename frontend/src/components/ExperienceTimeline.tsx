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
    <div className="space-y-4">
      {roles.map((role) => {
        const expanded = openRole === role.id
        const panelId = `role-${role.id}`
        return (
          <article key={role.id} className="section-card relative overflow-hidden">
            <button
              type="button"
              aria-expanded={expanded}
              aria-controls={panelId}
              onClick={() => setOpenRole(expanded ? null : role.id)}
              className="flex min-h-11 w-full items-start justify-between gap-4 text-left focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-4 focus-visible:outline-cyan-700"
            >
              <span>
                <span className="block text-lg font-semibold text-slate-950">{role.title} · {role.company}</span>
                <span className="mt-1 block text-sm text-slate-500">{period(role)} · {role.location}</span>
              </span>
              <span aria-hidden className="text-2xl text-cyan-700">{expanded ? '−' : '+'}</span>
            </button>
            {expanded && (
              <div id={panelId} className="mt-5 space-y-4 border-t border-slate-200 pt-5">
                <ul className="space-y-3 text-slate-700">
                  {role.highlights.map((highlight) => <li key={highlight} className="flex gap-3"><span aria-hidden className="text-cyan-600">◆</span><span>{highlight}</span></li>)}
                </ul>
                {role.technologies.length > 0 && <div className="flex flex-wrap gap-2">{role.technologies.map((tech) => <span key={tech} className="tag">{tech}</span>)}</div>}
                {role.link && <a className="text-link" href={role.link}>View related work</a>}
              </div>
            )}
          </article>
        )
      })}
    </div>
  )
}
