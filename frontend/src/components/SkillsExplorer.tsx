import type { PortfolioContent } from '../types/content'

interface SkillsExplorerProps {
  content: PortfolioContent
}

/**
 * Skills exactly as the resume lists them: grouped by category, nothing else.
 *
 * No evidence links, coverage ratio or source labels — the resume states which
 * skills there are, not where each was used, and the portfolio does not infer
 * what the resume does not say.
 */
export function SkillsExplorer({ content }: SkillsExplorerProps) {
  if (content.skills.groups.length === 0) {
    return <p className="empty-state">No skills to show yet.</p>
  }

  return (
    <div className="grid gap-5 md:grid-cols-2">
      {content.skills.groups.map((group) => (
        <section
          key={group.id}
          className="section-card"
          aria-labelledby={`skill-group-${group.id}`}
        >
          <h3 id={`skill-group-${group.id}`} className="card-title">
            {group.name}
          </h3>
          <ul className="mt-4 flex flex-wrap gap-2">
            {group.skills.map((skill) => (
              <li key={skill.name} className="tag">
                {skill.name}
              </li>
            ))}
          </ul>
        </section>
      ))}
    </div>
  )
}
