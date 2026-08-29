import type { Profile as ProfileData } from '../types/content'

interface ProfileProps {
  profile: ProfileData
  /** Counts derived from content, shown as the evidence behind the claim. */
  evidence?: { roles: number; projects: number; skills: number }
}

export function Profile({ profile, evidence }: ProfileProps) {
  if (!profile.name && !profile.title) {
    return <p className="empty-state">No profile content yet.</p>
  }

  return (
    <section aria-labelledby="profile-name" className="py-14 sm:py-20">
      <p className="eyebrow">AI Engineer · Auckland</p>

      <h1
        id="profile-name"
        className="mt-5 max-w-4xl text-5xl font-bold leading-[1.05] tracking-tight sm:text-7xl"
        style={{ color: 'var(--text-primary)' }}
      >
        {profile.name}
      </h1>

      <p
        className="mt-4 max-w-3xl text-xl sm:text-2xl"
        style={{ color: 'var(--text-signal)', fontFamily: 'var(--font-display)' }}
      >
        {profile.title}
      </p>

      {profile.summary && <p className="lede mt-6 max-w-3xl">{profile.summary}</p>}

      {/* The thesis, stated as data: this portfolio is backed by countable
          evidence rather than adjectives. */}
      {evidence && (
        <div className="mt-8 flex flex-wrap items-center gap-x-6 gap-y-2">
          <span className="provenance">
            <span aria-hidden>◆</span> {evidence.roles} roles
          </span>
          <span className="provenance">
            <span aria-hidden>◆</span> {evidence.projects} projects
          </span>
          <span className="provenance">
            <span aria-hidden>◆</span> {evidence.skills} skills, each linked to its proof
          </span>
        </div>
      )}

      <div className="mt-9 flex flex-wrap gap-3">
        <a className="button-primary" href="#skills">
          Explore the evidence
        </a>
        {profile.links.github && (
          <a className="button-secondary" href={profile.links.github}>
            GitHub
          </a>
        )}
        {profile.links.email && (
          <a className="button-secondary" href={`mailto:${profile.links.email}`}>
            Contact
          </a>
        )}
      </div>

      <p className="meta mt-8">
        rendered from content/profile.json · nothing here is hand-written copy
      </p>
    </section>
  )
}
