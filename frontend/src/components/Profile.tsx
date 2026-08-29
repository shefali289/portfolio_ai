/**
 * Renders the profile fetched from `/api/profile`.
 *
 * Proves the stack end to end: content/profile.json -> ContentService ->
 * FastAPI -> api.ts -> here. Nothing on this page is hardcoded copy.
 *
 * Handles all three states explicitly: loading, error, empty.
 */

import { useCallback, useEffect, useState } from 'react'

import { getProfile } from '../lib/api'
import type { Profile as ProfileData } from '../types/content'

type State =
  | { status: 'loading' }
  | { status: 'error'; message: string }
  | { status: 'ready'; profile: ProfileData }

export function Profile() {
  const [state, setState] = useState<State>({ status: 'loading' })

  // Note: no synchronous setState in here. The component already starts in
  // 'loading', and setting it again in the effect body triggers a cascading
  // render (react-hooks/set-state-in-effect). Retry sets it from its handler.
  const load = useCallback(() => {
    let cancelled = false

    getProfile()
      .then((profile) => {
        if (!cancelled) setState({ status: 'ready', profile })
      })
      .catch((error: unknown) => {
        if (cancelled) return
        const message = error instanceof Error ? error.message : 'Something went wrong'
        setState({ status: 'error', message })
      })

    return () => {
      cancelled = true
    }
  }, [])

  useEffect(() => load(), [load])

  const retry = () => {
    setState({ status: 'loading' })
    load()
  }

  if (state.status === 'loading') {
    return (
      <div role="status" aria-live="polite" className="space-y-3">
        <span className="sr-only">Loading profile…</span>
        <div aria-hidden className="h-9 w-64 animate-pulse rounded bg-slate-200" />
        <div aria-hidden className="h-5 w-40 animate-pulse rounded bg-slate-200" />
      </div>
    )
  }

  if (state.status === 'error') {
    return (
      <div role="alert" className="rounded border border-red-300 bg-red-50 p-4">
        <p className="font-medium text-red-800">Could not load the profile.</p>
        <p className="mt-1 text-sm text-red-700">{state.message}</p>
        <button
          type="button"
          onClick={retry}
          className="mt-3 rounded border border-red-300 px-3 py-1.5 text-sm font-medium text-red-800 hover:bg-red-100"
        >
          Try again
        </button>
      </div>
    )
  }

  const { profile } = state

  if (!profile.name && !profile.title) {
    return <p className="text-slate-600">No profile content yet.</p>
  }

  return (
    <section aria-labelledby="profile-name" className="space-y-3">
      <h1 id="profile-name" className="text-3xl font-semibold tracking-tight text-slate-900">
        {profile.name}
      </h1>
      <p className="text-lg text-slate-700">{profile.title}</p>
      {profile.location && <p className="text-sm text-slate-500">{profile.location}</p>}
      {profile.summary && <p className="max-w-2xl leading-relaxed text-slate-700">{profile.summary}</p>}
    </section>
  )
}
