/**
 * Layout shell. Phase 2 fills `main` with the rest of the portfolio sections;
 * Phase 1 only proves the stack is wired end to end.
 */

import { Profile } from './components/Profile'

export default function App() {
  return (
    <div className="min-h-screen bg-white text-slate-900">
      <a
        href="#main"
        className="sr-only focus:not-sr-only focus:absolute focus:left-4 focus:top-4 focus:rounded focus:bg-slate-900 focus:px-3 focus:py-2 focus:text-white"
      >
        Skip to content
      </a>

      <header className="border-b border-slate-200">
        <div className="mx-auto max-w-4xl px-6 py-4">
          <p className="text-sm font-medium tracking-wide text-slate-500">Portfolio</p>
        </div>
      </header>

      <main id="main" className="mx-auto max-w-4xl px-6 py-12">
        <Profile />
      </main>

      <footer className="border-t border-slate-200">
        <div className="mx-auto max-w-4xl px-6 py-6 text-sm text-slate-500">
          Built with React, FastAPI and content from <code>content/*.json</code>.
        </div>
      </footer>
    </div>
  )
}
