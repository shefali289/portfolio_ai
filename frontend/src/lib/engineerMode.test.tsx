import { act, render, screen } from '@testing-library/react'
import userEvent from '@testing-library/user-event'
import { beforeEach, describe, expect, it, vi } from 'vitest'

import { EngineerModeProvider, EngineerModeToggle } from './engineerMode'
import { useEngineerMode } from './engineerModeContext'

function Probe() {
  const { enabled } = useEngineerMode()
  return <span data-testid="state">{enabled ? 'on' : 'off'}</span>
}

function App() {
  return (
    <EngineerModeProvider>
      <EngineerModeToggle />
      <Probe />
    </EngineerModeProvider>
  )
}

describe('EngineerMode', () => {
  beforeEach(() => {
    window.localStorage.clear()
    vi.restoreAllMocks()
  })

  it('is off by default', () => {
    render(<App />)

    expect(screen.getByTestId('state')).toHaveTextContent('off')
  })

  it('turns on when the toggle is pressed', async () => {
    const user = userEvent.setup()
    render(<App />)

    await user.click(screen.getByRole('button', { name: /engineer mode/i }))

    expect(screen.getByTestId('state')).toHaveTextContent('on')
  })

  it('reports its state through aria-pressed', async () => {
    const user = userEvent.setup()
    render(<App />)
    const toggle = screen.getByRole('button', { name: /engineer mode/i })

    expect(toggle).toHaveAttribute('aria-pressed', 'false')
    await user.click(toggle)

    expect(toggle).toHaveAttribute('aria-pressed', 'true')
  })

  it('remembers the choice across a remount', async () => {
    const user = userEvent.setup()
    const first = render(<App />)
    await user.click(screen.getByRole('button', { name: /engineer mode/i }))
    first.unmount()

    render(<App />)

    expect(screen.getByTestId('state')).toHaveTextContent('on')
  })

  it('falls back to off when localStorage cannot be read', () => {
    // Private mode and blocked site data both make this throw. Engineer Mode is
    // a convenience: losing it must never take the page down with it.
    vi.spyOn(Storage.prototype, 'getItem').mockImplementation(() => {
      throw new Error('access denied')
    })

    render(<App />)

    expect(screen.getByTestId('state')).toHaveTextContent('off')
  })

  it('does not crash when localStorage cannot be written', async () => {
    const user = userEvent.setup()
    vi.spyOn(Storage.prototype, 'setItem').mockImplementation(() => {
      throw new Error('quota exceeded')
    })
    render(<App />)

    await act(async () => {
      await user.click(screen.getByRole('button', { name: /engineer mode/i }))
    })

    // The toggle still works for this session; only persistence is lost.
    expect(screen.getByTestId('state')).toHaveTextContent('on')
  })
})
