import { useMemo, useState } from 'react'

import { buildEvidenceIndex } from '../lib/evidence'
import type { PortfolioContent, SkillEvidence } from '../types/content'

interface SkillsExplorerProps {
  content: PortfolioContent
}

/** Which content file backs each kind of evidence — the provenance label. */
const SOURCE_FILE: Record<string, string> = {
  role: 'content/experience.json',
  project: 'content/projects.json',
  certification: 'content/profile.json',
  education: 'content/profile.json',
  achievement: 'content/engineering-notes.json',
}

function sourcesFor(evidence: SkillEvidence[]): string[] {
  return [...new Set(evidence.map((item) => SOURCE_FILE[item.type]).filter(Boolean))]
}

export function SkillsExplorer({ content }: SkillsExplorerProps) {
  const [selected, setSelected] = useState<string | null>(null)
  const evidenceIndex = useMemo(() => buildEvidenceIndex(content), [content])

  const { total, proven } = useMemo(() => {
    const all = content.skills.groups.flatMap((group) => group.skills)
    return { total: all.length, proven: all.filter((s) => s.evidence.length > 0).length }
  }, [content.skills.groups])

  if (content.skills.groups.length === 0) {
    return <p className="empty-state">No skills to show yet.</p>
  }

  return (
    <div className="space-y-6">
      {/* The honesty counter. Stating the ratio up front is the point: the
          portfolio does not pretend every listed skill is demonstrated. */}
      <p className="provenance">
        <span aria-hidden>◆</span>
        {proven} of {total} skills evidenced · select one to see its proof
      </p>

      <div className="grid gap-5 md:grid-cols-2">
        {content.skills.groups.map((group) => (
          <section
            key={group.id}
            className="section-card"
            aria-labelledby={`skill-group-${group.id}`}
          >
            <h3
              id={`skill-group-${group.id}`}
              className="text-lg font-semibold"
              style={{ color: 'var(--text-primary)' }}
            >
              {group.name}
            </h3>

            <div className="mt-4 space-y-2">
              {group.skills.map((skill) => {
                const key = `${group.id}:${skill.name}`
                const open = selected === key
                const isProven = skill.evidence.length > 0

                return (
                  <div key={skill.name}>
                    <button
                      type="button"
                      aria-expanded={open}
                      data-proven={isProven}
                      onClick={() => setSelected(open ? null : key)}
                      className="skill-button w-full text-left"
                    >
                      <span className="flex items-center justify-between gap-3">
                        <span>{skill.name}</span>
                        <span aria-hidden className="text-xs opacity-70">
                          {isProven ? `${skill.evidence.length}◆` : '—'}
                        </span>
                      </span>
                    </button>

                    {open && (
                      <div
                        className="mt-2 rounded-xl p-3 text-sm"
                        style={{
                          backgroundColor: 'var(--accent-wash)',
                          color: 'var(--text-secondary)',
                        }}
                      >
                        {isProven ? (
                          <>
                            <ul className="space-y-1">
                              {skill.evidence.map((item) => (
                                <li key={`${item.type}:${item.ref}`}>
                                  {evidenceIndex[`${item.type}:${item.ref}`]}
                                </li>
                              ))}
                            </ul>
                            <p className="provenance mt-3">
                              source: {sourcesFor(skill.evidence).join(' · ')}
                            </p>
                          </>
                        ) : (
                          <p>
                            Evidence not yet documented. Listed on the resume, but no
                            role or project here demonstrates it.
                          </p>
                        )}
                      </div>
                    )}
                  </div>
                )
              })}
            </div>
          </section>
        ))}
      </div>
    </div>
  )
}
