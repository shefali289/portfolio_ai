import type { Achievement, Profile } from '../types/content'

interface CredentialsProps {
  profile: Profile
  achievements: Achievement[]
}

export function Credentials({ profile, achievements }: CredentialsProps) {
  const empty = profile.education.length === 0
    && profile.certifications.length === 0
    && profile.languages.length === 0
    && achievements.length === 0

  if (empty) return <p className="empty-state">No credentials content yet.</p>

  return (
    <div className="grid gap-5 md:grid-cols-2">
      {profile.education.map((item) => (
        <article key={item.id} className="section-card">
          <p className="eyebrow">Education</p>
          <h3 className="mt-2 font-semibold text-slate-950">{item.qualification}</h3>
          <p className="mt-1 text-slate-700">{item.institution} · {item.location}</p>
          <p className="mt-2 text-sm text-slate-500">{item.start} — {item.end} · {item.grade}</p>
        </article>
      ))}
      {profile.certifications.map((item) => (
        <article key={item.id} className="section-card">
          <p className="eyebrow">Certification</p>
          <h3 className="mt-2 font-semibold text-slate-950">{item.name}</h3>
          <p className="mt-1 text-slate-600">{item.issuer}</p>
        </article>
      ))}
      {achievements.map((item) => (
        <article key={item.id} className="section-card">
          <p className="eyebrow">Achievement</p>
          <h3 className="mt-2 font-semibold text-slate-950">{item.name}</h3>
          <p className="mt-1 text-slate-600">{item.issuer}</p>
        </article>
      ))}
      {profile.languages.length > 0 && (
        <article className="section-card">
          <p className="eyebrow">Languages</p>
          <ul className="mt-3 space-y-2">{profile.languages.map((item) => <li key={item.name}><span className="font-medium text-slate-950">{item.name}</span><span className="text-slate-500"> · {item.proficiency}</span></li>)}</ul>
        </article>
      )}
    </div>
  )
}
