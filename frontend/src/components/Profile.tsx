import type { Profile as ProfileData } from '../types/content'

interface ProfileProps {
  profile: ProfileData
}

export function Profile({ profile }: ProfileProps) {
  if (!profile.name && !profile.title) {
    return <p className="text-slate-600">No profile content yet.</p>
  }

  return (
    <section aria-labelledby="profile-name" className="grid gap-8 py-10 md:grid-cols-[1fr_auto] md:items-end">
      <div className="min-w-0 space-y-5">
        <p className="text-sm font-semibold uppercase tracking-[0.25em] text-cyan-700">Portfolio</p>
        <h1 id="profile-name" className="max-w-3xl text-4xl font-bold tracking-tight text-slate-950 sm:text-6xl">
          {profile.name}
        </h1>
        <p className="text-xl font-medium text-cyan-800 sm:text-2xl">{profile.title}</p>
        {profile.summary && <p className="max-w-3xl break-words text-base leading-8 text-slate-700 sm:text-lg">{profile.summary}</p>}
        <div className="flex flex-wrap gap-3">
          <a className="button-primary" href="#projects">Explore work</a>
          {profile.links.github && <a className="button-secondary" href={profile.links.github}>GitHub</a>}
          {profile.links.email && <a className="button-secondary" href={`mailto:${profile.links.email}`}>Contact</a>}
          <span className="inline-flex min-h-11 items-center rounded-full border border-dashed border-slate-300 px-4 text-sm text-slate-500">
            Ask my AI · coming later
          </span>
        </div>
      </div>
      {profile.location && (
        <p className="rounded-full bg-slate-100 px-4 py-2 text-sm font-medium text-slate-600">
          {profile.location}
        </p>
      )}
    </section>
  )
}
