import type { Profile as ProfileData } from '../types/content'

interface ProfileProps {
  profile: ProfileData
}

export function Profile({ profile }: ProfileProps) {
  if (!profile.name && !profile.title) {
    return <p className="empty-state">No profile content yet.</p>
  }

  return (
    <section aria-labelledby="profile-name" className="py-14 sm:py-20">
      {profile.location && <p className="eyebrow">{profile.location}</p>}

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

      <div className="mt-9 flex flex-wrap gap-3">
        <a className="button-primary" href="#experience">
          View work
        </a>
        {profile.links.github && (
          <a className="button-secondary" href={profile.links.github}>
            GitHub
          </a>
        )}
        {profile.links.linkedin && (
          <a className="button-secondary" href={profile.links.linkedin}>
            LinkedIn
          </a>
        )}
        {profile.links.email && (
          <a className="button-secondary" href={`mailto:${profile.links.email}`}>
            Email
          </a>
        )}
      </div>
    </section>
  )
}
