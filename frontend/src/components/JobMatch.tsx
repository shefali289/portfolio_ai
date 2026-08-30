import { useId, useState } from 'react'

import { matchJob } from '../lib/api'
import type { JobMatchReport, RequirementMatch } from '../types/content'

type State =
  | { status: 'idle' }
  | { status: 'running' }
  | { status: 'done'; report: JobMatchReport }
  | { status: 'error'; message: string }

/**
 * Paste a job description; four agents run in sequence and report back.
 *
 * Gaps are shown as gaps. A requirement the portfolio cannot evidence is listed
 * plainly rather than softened into a near-match — an honest report is the
 * point, and a flattering one would be useless to a recruiter.
 */
export function JobMatch() {
  const [text, setText] = useState('')
  const [state, setState] = useState<State>({ status: 'idle' })
  const fieldId = useId()

  const submit = (event: React.FormEvent) => {
    event.preventDefault()
    const trimmed = text.trim()
    if (!trimmed || state.status === 'running') return

    setState({ status: 'running' })
    matchJob(trimmed)
      .then((report) => setState({ status: 'done', report }))
      .catch((error: unknown) =>
        setState({
          status: 'error',
          message: error instanceof Error ? error.message : 'Something went wrong',
        }),
      )
  }

  return (
    <div className="section-card">
      <form onSubmit={submit} className="space-y-3">
        <label htmlFor={fieldId} className="sr-only">
          Job description
        </label>
        <textarea
          id={fieldId}
          value={text}
          onChange={(event) => setText(event.target.value)}
          rows={5}
          placeholder="Paste a job description…"
          className="w-full rounded-2xl p-4 text-sm"
          style={{
            backgroundColor: 'var(--surface-sunken)',
            border: '1px solid var(--border-subtle)',
            color: 'var(--text-primary)',
          }}
        />
        <button type="submit" className="button-primary">
          Match against my portfolio
        </button>
      </form>

      {state.status === 'running' && (
        <div role="status" aria-live="polite" className="mt-5">
          <span className="sr-only">Running the match…</span>
          <div
            aria-hidden
            className="h-4 w-2/3 rounded motion-safe:animate-pulse"
            style={{ backgroundColor: 'var(--surface-sunken)' }}
          />
        </div>
      )}

      {state.status === 'error' && (
        <div role="alert" className="mt-5">
          <p className="body-text">Could not run the match.</p>
          <p className="meta mt-1">{state.message}</p>
        </div>
      )}

      {state.status === 'done' && (
        <div className="mt-6 space-y-6" aria-live="polite">
          <ol className="flex flex-wrap gap-x-4 gap-y-1">
            {state.report.steps.map((step) => (
              <li key={step.name} className="meta">
                <span aria-hidden style={{ color: 'var(--accent)' }}>
                  ✓
                </span>{' '}
                {step.label}
              </li>
            ))}
          </ol>

          <p className="body-text">{state.report.summary}</p>

          {state.report.matches.length > 0 && (
            <section aria-labelledby="jm-matches">
              <h3 id="jm-matches" className="card-title">
                Evidenced
              </h3>
              <ul className="mt-3 space-y-3">
                {state.report.matches.map((m) => (
                  <RequirementRow key={m.requirement.text} match={m} />
                ))}
              </ul>
            </section>
          )}

          {state.report.gaps.length > 0 && (
            <section aria-labelledby="jm-gaps">
              <h3 id="jm-gaps" className="card-title">
                Gaps
              </h3>
              <p className="meta mt-1">Not evidenced anywhere in this portfolio.</p>
              <ul className="mt-3 flex flex-wrap gap-2">
                {state.report.gaps.map((g) => (
                  <li key={g.requirement.text} className="tag">
                    {g.requirement.text}
                  </li>
                ))}
              </ul>
            </section>
          )}
        </div>
      )}
    </div>
  )
}

function RequirementRow({ match }: { match: RequirementMatch }) {
  return (
    <li>
      <p className="font-medium" style={{ color: 'var(--text-primary)' }}>
        {match.requirement.text}
      </p>
      <ul className="mt-1 space-y-1">
        {match.evidence.map((e) => (
          <li key={e.source} className="body-text text-sm">
            {e.text}
          </li>
        ))}
      </ul>
    </li>
  )
}
