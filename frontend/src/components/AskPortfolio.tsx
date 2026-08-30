import { useId, useState } from 'react'

import { askPortfolio } from '../lib/api'
import type { ChatAnswer } from '../types/content'

type State =
  | { status: 'idle' }
  | { status: 'asking' }
  | { status: 'answered'; result: ChatAnswer }
  | { status: 'error'; message: string }

/**
 * Ask a question about the portfolio.
 *
 * Answers come only from `content/*.json`. An unsupported question is refused
 * by retrieval before any model runs, and the refusal is shown as-is rather
 * than dressed up as an answer.
 */
export function AskPortfolio() {
  const [question, setQuestion] = useState('')
  const [state, setState] = useState<State>({ status: 'idle' })
  const inputId = useId()

  const submit = (event: React.FormEvent) => {
    event.preventDefault()
    const trimmed = question.trim()
    if (!trimmed || state.status === 'asking') return

    setState({ status: 'asking' })
    askPortfolio(trimmed)
      .then((result) => setState({ status: 'answered', result }))
      .catch((error: unknown) =>
        setState({
          status: 'error',
          message: error instanceof Error ? error.message : 'Something went wrong',
        }),
      )
  }

  return (
    <div className="section-card">
      <form onSubmit={submit} className="flex flex-col gap-3 sm:flex-row">
        <label htmlFor={inputId} className="sr-only">
          Ask a question about this portfolio
        </label>
        <input
          id={inputId}
          type="text"
          value={question}
          onChange={(event) => setQuestion(event.target.value)}
          placeholder="What AI experience does she have?"
          className="min-h-11 flex-1 rounded-full px-5 text-sm"
          style={{
            backgroundColor: 'var(--surface-sunken)',
            border: '1px solid var(--border-subtle)',
            color: 'var(--text-primary)',
          }}
        />
        <button type="submit" className="button-primary justify-center">
          Ask
        </button>
      </form>

      {state.status === 'asking' && (
        <div role="status" aria-live="polite" className="mt-5">
          <span className="sr-only">Finding an answer…</span>
          <div
            aria-hidden
            className="h-4 w-2/3 rounded motion-safe:animate-pulse"
            style={{ backgroundColor: 'var(--surface-sunken)' }}
          />
        </div>
      )}

      {state.status === 'error' && (
        <div role="alert" className="mt-5">
          <p className="body-text">Could not reach the assistant.</p>
          <p className="meta mt-1">{state.message}</p>
        </div>
      )}

      {state.status === 'answered' && (
        <div className="mt-5" aria-live="polite">
          <p className="body-text whitespace-pre-line">{state.result.answer}</p>
        </div>
      )}
    </div>
  )
}
