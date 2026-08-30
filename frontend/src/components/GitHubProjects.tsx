import { useEffect, useState } from 'react'

import { getGithubRepos } from '../lib/api'
import type { GithubRepo } from '../types/content'

interface GitHubProjectsProps {
  /** The profile's GitHub URL, from `content/profile.json`. */
  profileUrl: string
}

type State =
  | { status: 'loading' }
  | { status: 'ready'; repos: GithubRepo[] }
  | { status: 'unavailable'; reason: string }

/** `2026-08-01T00:00:00Z` -> `Aug 2026`. */
function updated(pushedAt: string): string {
  const date = new Date(pushedAt)
  if (Number.isNaN(date.getTime())) return ''
  return date.toLocaleDateString(undefined, { month: 'short', year: 'numeric' })
}

/**
 * Live public repositories, fetched from the GitHub REST API.
 *
 * This is the *tool* half of the portfolio: unlike every other section it is
 * not backed by `content/*.json`, and it can be empty or unreachable at any
 * moment. It degrades to an honest sentence and a link rather than an error —
 * a supplementary section must never look like a broken page.
 */
export function GitHubProjects({ profileUrl }: GitHubProjectsProps) {
  const [state, setState] = useState<State>({ status: 'loading' })

  useEffect(() => {
    let cancelled = false
    getGithubRepos()
      .then((result) => {
        if (cancelled) return
        if (result.reason) {
          setState({ status: 'unavailable', reason: result.reason })
        } else {
          setState({ status: 'ready', repos: result.repos })
        }
      })
      .catch(() => {
        if (!cancelled) {
          setState({ status: 'unavailable', reason: 'GitHub could not be reached right now.' })
        }
      })
    return () => {
      cancelled = true
    }
  }, [])

  if (state.status === 'loading') {
    return (
      <div role="status" aria-live="polite" className="grid gap-5 md:grid-cols-2">
        <span className="sr-only">Loading repositories…</span>
        {[0, 1].map((key) => (
          <div
            key={key}
            aria-hidden
            className="h-32 rounded-3xl motion-safe:animate-pulse"
            style={{ backgroundColor: 'var(--surface-sunken)' }}
          />
        ))}
      </div>
    )
  }

  if (state.status === 'unavailable') {
    return (
      <div className="section-card">
        <p className="body-text">{state.reason}</p>
        <p className="meta mt-2">
          The repositories are still there —{' '}
          <a className="text-link" href={profileUrl}>
            view them on GitHub
          </a>
          .
        </p>
      </div>
    )
  }

  if (state.repos.length === 0) {
    return <p className="empty-state">No public repositories to show yet.</p>
  }

  return (
    <ul className="grid list-none gap-5 p-0 md:grid-cols-2">
      {state.repos.map((repo) => (
        <li key={repo.name} className="section-card flex flex-col">
          <div className="flex items-start justify-between gap-4">
            <h3 className="card-title text-lg">
              <a className="text-link" href={repo.url}>
                {repo.name}
              </a>
            </h3>
            {repo.pushed_at && <span className="meta">{updated(repo.pushed_at)}</span>}
          </div>

          {repo.description && <p className="body-text mt-3 flex-1">{repo.description}</p>}

          <div className="mt-5 flex flex-wrap gap-2">
            {repo.language && <span className="tag">{repo.language}</span>}
            {repo.topics.map((topic) => (
              <span key={topic} className="tag">
                {topic}
              </span>
            ))}
          </div>
        </li>
      ))}
    </ul>
  )
}
