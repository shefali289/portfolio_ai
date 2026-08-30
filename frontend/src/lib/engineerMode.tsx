import { useCallback, useMemo, useState } from 'react'

import { EngineerModeContext, STORAGE_KEY, useEngineerMode } from './engineerModeContext'

/**
 * Engineer Mode: reveal what each AI response actually cost and cited.
 *
 * Off by default. A recruiter should meet the portfolio, not the
 * instrumentation; an engineer can switch it on in one click.
 *
 * Persistence is a convenience, never a requirement. Private browsing and
 * blocked site data both make `localStorage` throw, so every access is guarded
 * and a failure means "off" rather than a blank page.
 */
function readStored(): boolean {
  try {
    return window.localStorage.getItem(STORAGE_KEY) === '1'
  } catch {
    return false
  }
}

function writeStored(enabled: boolean): void {
  try {
    window.localStorage.setItem(STORAGE_KEY, enabled ? '1' : '0')
  } catch {
    // Persistence lost for this browser; the toggle still works this session.
  }
}

export function EngineerModeProvider({ children }: { children: React.ReactNode }) {
  // Lazy initial state: read storage once, on mount, not on every render.
  const [enabled, setEnabled] = useState<boolean>(readStored)

  const toggle = useCallback(() => {
    setEnabled((current) => {
      const next = !current
      writeStored(next)
      return next
    })
  }, [])

  const value = useMemo(() => ({ enabled, toggle }), [enabled, toggle])

  return <EngineerModeContext.Provider value={value}>{children}</EngineerModeContext.Provider>
}

export function EngineerModeToggle() {
  const { enabled, toggle } = useEngineerMode()

  return (
    <button
      type="button"
      onClick={toggle}
      aria-pressed={enabled}
      className="nav-link inline-flex items-center"
      style={{
        border: '1px solid var(--border-subtle)',
        borderRadius: '9999px',
        // 44px: the minimum comfortable touch target at 375px. Padding alone
        // left this at ~30px, which measured as a real a11y failure.
        minHeight: '44px',
        padding: '0 0.9rem',
        color: enabled ? 'var(--text-signal)' : 'var(--text-muted)',
      }}
    >
      Engineer Mode
    </button>
  )
}
