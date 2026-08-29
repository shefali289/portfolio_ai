import { useMemo, useState } from 'react'

import { buildEvidenceIndex } from '../lib/evidence'
import type { PortfolioContent } from '../types/content'

interface SkillsExplorerProps {
  content: PortfolioContent
}

export function SkillsExplorer({ content }: SkillsExplorerProps) {
  const [selected, setSelected] = useState<string | null>(null)
  const evidenceIndex = useMemo(() => buildEvidenceIndex(content), [content])

  if (content.skills.groups.length === 0) return <p className="empty-state">No skills to show yet.</p>

  return (
    <div className="grid gap-5 md:grid-cols-2">
      {content.skills.groups.map((group) => (
        <section key={group.id} className="section-card" aria-labelledby={`skill-group-${group.id}`}>
          <h3 id={`skill-group-${group.id}`} className="text-lg font-semibold text-slate-950">{group.name}</h3>
          <div className="mt-4 flex flex-wrap gap-2">
            {group.skills.map((skill) => {
              const key = `${group.id}:${skill.name}`
              const open = selected === key
              return (
                <div key={skill.name} className="w-full">
                  <button
                    type="button"
                    aria-expanded={open}
                    onClick={() => setSelected(open ? null : key)}
                    className="skill-button"
                  >
                    {skill.name}
                  </button>
                  {open && (
                    <div className="mt-2 rounded-xl bg-slate-50 p-3 text-sm text-slate-700">
                      {skill.evidence.length > 0 ? (
                        <ul className="space-y-1">
                          {skill.evidence.map((item) => (
                            <li key={`${item.type}:${item.ref}`}>{evidenceIndex[`${item.type}:${item.ref}`]}</li>
                          ))}
                        </ul>
                      ) : <p>Evidence not yet documented.</p>}
                    </div>
                  )}
                </div>
              )
            })}
          </div>
        </section>
      ))}
    </div>
  )
}
