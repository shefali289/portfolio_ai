import { useCallback, useEffect, useState } from 'react'

import { AskPortfolio } from './components/AskPortfolio'
import { Contact } from './components/Contact'
import { Credentials } from './components/Credentials'
import { EngineeringNotes } from './components/EngineeringNotes'
import { ExperienceTimeline } from './components/ExperienceTimeline'
import { Profile } from './components/Profile'
import { ProjectGallery } from './components/ProjectGallery'
import { SkillsExplorer } from './components/SkillsExplorer'
import { Reveal } from './components/Reveal'
import { getContent } from './lib/api'
import type { PortfolioContent } from './types/content'

type State =
  | { status: 'loading' }
  | { status: 'error'; message: string }
  | { status: 'ready'; content: PortfolioContent }

const sections = [
  { id: 'ask', label: 'Ask', eyebrow: 'Grounded in this portfolio' },
  { id: 'experience', label: 'Experience', eyebrow: 'Career' },
  { id: 'projects', label: 'Projects', eyebrow: 'Selected work' },
  { id: 'skills', label: 'Skills', eyebrow: 'Technical' },
  { id: 'credentials', label: 'Credentials', eyebrow: 'Learning and recognition' },
  { id: 'contact', label: 'Contact', eyebrow: 'Get in touch' },
] as const

/** Highlights the section currently in view, for the sticky rail. */
function useActiveSection(enabled: boolean): string {
  const [active, setActive] = useState<string>(sections[0].id)

  useEffect(() => {
    if (!enabled || typeof IntersectionObserver !== 'function') return

    const observer = new IntersectionObserver(
      (entries) => {
        const visible = entries
          .filter((entry) => entry.isIntersecting)
          .sort((a, b) => b.intersectionRatio - a.intersectionRatio)[0]
        if (visible) setActive(visible.target.id)
      },
      { rootMargin: '-20% 0px -60% 0px', threshold: [0.1, 0.5] },
    )

    for (const section of sections) {
      const node = document.getElementById(section.id)
      if (node) observer.observe(node)
    }
    return () => observer.disconnect()
  }, [enabled])

  return active
}

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
    return () => {
      cancelled = true
    }
  }, [])

  useEffect(() => load(), [load])

  const retry = () => {
    setState({ status: 'loading' })
    load()
  }

  const ready = state.status === 'ready'
  const active = useActiveSection(ready)

  return (
    <div className="min-h-screen overflow-x-hidden">
      <a
        href="#main"
        className="sr-only focus:not-sr-only focus:fixed focus:left-4 focus:top-4 focus:z-50 focus:rounded-full focus:px-4 focus:py-3"
        style={{ backgroundColor: 'var(--accent)', color: 'var(--accent-contrast)' }}
      >
        Skip to content
      </a>

      <header
        className="sticky top-0 z-40 backdrop-blur"
        style={{
          borderBottom: '1px solid var(--border-subtle)',
          backgroundColor: 'color-mix(in srgb, var(--surface-base) 88%, transparent)',
        }}
      >
        <div className="mx-auto flex w-full max-w-6xl items-center justify-between gap-4 px-4 py-4 sm:px-6">
          <a href="#main" className="eyebrow" style={{ textDecoration: 'none' }}>
            {state.status === 'ready' ? state.content.profile.name : ''}
          </a>
          <nav aria-label="Portfolio sections" className="hidden md:block">
            <ul className="flex items-center gap-6">
              {sections.map((section) => (
                <li key={section.id}>
                  <a
                    className="nav-link"
                    href={`#${section.id}`}
                    aria-current={active === section.id ? 'location' : undefined}
                    style={
                      active === section.id
                        ? { color: 'var(--text-signal)' }
                        : { color: 'var(--text-muted)' }
                    }
                  >
                    {section.label}
                  </a>
                </li>
              ))}
            </ul>
          </nav>
        </div>
      </header>

      <main id="main" className="mx-auto w-full max-w-6xl px-4 pb-24 sm:px-6">
        {state.status === 'loading' && (
          <div role="status" aria-live="polite" className="space-y-4 py-24">
            <span className="sr-only">Loading portfolio…</span>
            <div
              aria-hidden
              className="h-14 w-3/4 max-w-xl rounded-2xl motion-safe:animate-pulse"
              style={{ backgroundColor: 'var(--surface-sunken)' }}
            />
            <div
              aria-hidden
              className="h-6 w-1/2 max-w-sm rounded-xl motion-safe:animate-pulse"
              style={{ backgroundColor: 'var(--surface-sunken)' }}
            />
          </div>
        )}

        {state.status === 'error' && (
          <div
            role="alert"
            className="my-16 rounded-3xl p-6"
            style={{
              border: '1px solid var(--border-strong)',
              backgroundColor: 'var(--surface-raised)',
            }}
          >
            <h1 className="card-title text-xl">Could not load the portfolio.</h1>
            <p className="body-text mt-2">{state.message}</p>
            <button type="button" onClick={retry} className="button-primary mt-5">
              Try again
            </button>
          </div>
        )}

        {state.status === 'ready' && (
          <div className="space-y-28">
            <Profile profile={state.content.profile} />

            {sections
              .filter((section) => section.id !== 'contact')
              .map((section) => (
                <Reveal key={section.id}>
                  <section
                    id={section.id}
                    aria-labelledby={`${section.id}-heading`}
                    className="scroll-mt-24"
                  >
                    <p className="eyebrow">{section.eyebrow}</p>
                    <h2 id={`${section.id}-heading`} className="section-heading">
                      {section.label}
                    </h2>
                    <div className="rule mt-5" />
                    <div className="mt-8">
                      {section.id === 'ask' && <AskPortfolio />}
                      {section.id === 'experience' && (
                        <ExperienceTimeline roles={state.content.experience.roles} />
                      )}
                      {section.id === 'projects' && (
                        <ProjectGallery projects={state.content.projects.projects} />
                      )}
                      {section.id === 'skills' && (
                        <SkillsExplorer content={state.content} />
                      )}
                      {section.id === 'credentials' && (
                        <Credentials
                          profile={state.content.profile}
                          achievements={state.content.engineering_notes.achievements}
                        />
                      )}
                    </div>
                  </section>
                </Reveal>
              ))}

            <EngineeringNotes notes={state.content.engineering_notes} />

            <Reveal>
              <Contact profile={state.content.profile} />
            </Reveal>
          </div>
        )}
      </main>

      <footer style={{ borderTop: '1px solid var(--border-subtle)' }}>
        <div className="mx-auto w-full max-w-6xl px-4 py-8 sm:px-6">
          <p className="meta">React · FastAPI</p>
        </div>
      </footer>
    </div>
  )
}
