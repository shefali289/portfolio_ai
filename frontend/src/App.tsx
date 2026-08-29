import { useCallback, useEffect, useState } from 'react'

import { Contact } from './components/Contact'
import { Credentials } from './components/Credentials'
import { EngineeringNotes } from './components/EngineeringNotes'
import { ExperienceTimeline } from './components/ExperienceTimeline'
import { Profile } from './components/Profile'
import { ProjectGallery } from './components/ProjectGallery'
import { SkillsExplorer } from './components/SkillsExplorer'
import { getContent } from './lib/api'
import type { PortfolioContent } from './types/content'

type State =
  | { status: 'loading' }
  | { status: 'error'; message: string }
  | { status: 'ready'; content: PortfolioContent }

const navigation = [
  ['Experience', '#experience'],
  ['Projects', '#projects'],
  ['Skills', '#skills'],
  ['Credentials', '#credentials'],
  ['Contact', '#contact'],
] as const

export default function App() {
  const [state, setState] = useState<State>({ status: 'loading' })

  const load = useCallback(() => {
    let cancelled = false
    getContent()
      .then((content) => {
        if (!cancelled) setState({ status: 'ready', content })
      })
      .catch((error: unknown) => {
        if (cancelled) return
        setState({
          status: 'error',
          message: error instanceof Error ? error.message : 'Something went wrong',
        })
      })
    return () => { cancelled = true }
  }, [])

  useEffect(() => load(), [load])

  const retry = () => {
    setState({ status: 'loading' })
    load()
  }

  return (
    <div className="min-h-screen overflow-x-hidden bg-[#f7f8fa] text-slate-900">
      <a href="#main" className="sr-only focus:not-sr-only focus:fixed focus:left-4 focus:top-4 focus:z-50 focus:rounded-full focus:bg-slate-950 focus:px-4 focus:py-3 focus:text-white">
        Skip to content
      </a>
      <header className="sticky top-0 z-40 border-b border-slate-200/80 bg-[#f7f8fa]/95 backdrop-blur">
        <div className="mx-auto flex w-full max-w-6xl items-center justify-between gap-4 px-4 py-4 sm:px-6">
          <a href="#main" className="font-bold tracking-tight text-slate-950">Engineer portfolio</a>
          <nav aria-label="Portfolio sections" className="hidden md:block">
            <ul className="flex items-center gap-5 text-sm font-medium text-slate-600">
              {navigation.map(([label, href]) => <li key={href}><a className="nav-link" href={href}>{label}</a></li>)}
            </ul>
          </nav>
        </div>
      </header>

      <main id="main" className="mx-auto w-full max-w-6xl px-4 pb-20 sm:px-6">
        {state.status === 'loading' && (
          <div role="status" aria-live="polite" className="space-y-4 py-20">
            <span className="sr-only">Loading portfolio…</span>
            <div aria-hidden className="h-12 w-3/4 max-w-xl motion-safe:animate-pulse rounded-2xl bg-slate-200" />
            <div aria-hidden className="h-6 w-1/2 max-w-sm motion-safe:animate-pulse rounded-xl bg-slate-200" />
          </div>
        )}

        {state.status === 'error' && (
          <div role="alert" className="my-16 rounded-3xl border border-red-200 bg-red-50 p-6">
            <h1 className="text-xl font-semibold text-red-900">Could not load the portfolio.</h1>
            <p className="mt-2 text-red-800">{state.message}</p>
            <button type="button" onClick={retry} className="mt-5 inline-flex min-h-11 items-center rounded-full bg-red-900 px-5 font-semibold text-white focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-4 focus-visible:outline-red-900">Try again</button>
          </div>
        )}

        {state.status === 'ready' && (
          <div className="space-y-24">
            <Profile profile={state.content.profile} />

            <section id="experience" aria-labelledby="experience-heading" className="scroll-mt-24">
              <p className="eyebrow">Career</p>
              <h2 id="experience-heading" className="section-heading">Experience</h2>
              <div className="mt-8"><ExperienceTimeline roles={state.content.experience.roles} /></div>
            </section>

            <section id="projects" aria-labelledby="projects-heading" className="scroll-mt-24">
              <p className="eyebrow">Selected work</p>
              <h2 id="projects-heading" className="section-heading">Projects</h2>
              <div className="mt-8"><ProjectGallery projects={state.content.projects.projects} /></div>
            </section>

            <section id="skills" aria-labelledby="skills-heading" className="scroll-mt-24">
              <p className="eyebrow">Evidence over ratings</p>
              <h2 id="skills-heading" className="section-heading">Skills</h2>
              <div className="mt-8"><SkillsExplorer content={state.content} /></div>
            </section>

            <section id="credentials" aria-labelledby="credentials-heading" className="scroll-mt-24">
              <p className="eyebrow">Learning and recognition</p>
              <h2 id="credentials-heading" className="section-heading">Credentials</h2>
              <div className="mt-8"><Credentials profile={state.content.profile} achievements={state.content.engineering_notes.achievements} /></div>
            </section>

            <EngineeringNotes notes={state.content.engineering_notes} />
            <Contact profile={state.content.profile} />
          </div>
        )}
      </main>

      <footer className="border-t border-slate-200">
        <div className="mx-auto w-full max-w-6xl px-4 py-8 text-sm text-slate-500 sm:px-6">
          Built with React, FastAPI, and resume-backed structured content.
        </div>
      </footer>
    </div>
  )
}
