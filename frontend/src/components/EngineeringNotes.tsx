import type { EngineeringNotes as Notes } from '../types/content'

interface EngineeringNotesProps {
  notes: Notes
}

export function EngineeringNotes({ notes }: EngineeringNotesProps) {
  const sections = [
    { id: 'building', title: "What I'm Building", items: notes.building },
    { id: 'learning', title: "What I'm Learning", items: notes.learning },
    { id: 'beyond', title: 'Beyond Engineering', items: notes.beyond },
  ].filter((section) => section.items.length > 0)

  if (sections.length === 0) return null

  return (
    <section aria-label="Engineering notes" className="grid gap-5 md:grid-cols-3">
      {sections.map((section) => (
        <article key={section.id} className="section-card">
          <h2 className="card-title text-xl">{section.title}</h2>
          <ul className="body-text mt-4 space-y-2">{section.items.map((item) => <li key={item}>{item}</li>)}</ul>
        </article>
      ))}
    </section>
  )
}
