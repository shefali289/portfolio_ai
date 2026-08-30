import { renderHook } from '@testing-library/react'
import { afterEach, describe, expect, it, vi } from 'vitest'

import { useReveal } from './useReveal'

const originalObserver = globalThis.IntersectionObserver
const originalMatchMedia = globalThis.matchMedia

function mockMatchMedia(reducedMotion: boolean) {
  globalThis.matchMedia = vi.fn().mockImplementation((query: string) => ({
    matches: query.includes('reduce') ? reducedMotion : false,
    media: query,
    addEventListener: vi.fn(),
    removeEventListener: vi.fn(),
    addListener: vi.fn(),
    removeListener: vi.fn(),
    dispatchEvent: vi.fn(),
    onchange: null,
  })) as unknown as typeof globalThis.matchMedia
}

afterEach(() => {
  globalThis.IntersectionObserver = originalObserver
  globalThis.matchMedia = originalMatchMedia
  vi.restoreAllMocks()
})

describe('useReveal', () => {
  it('reports visible when IntersectionObserver is unavailable', () => {
    // @ts-expect-error deliberately removing the API to simulate an old browser
    delete globalThis.IntersectionObserver
    mockMatchMedia(false)

    const { result } = renderHook(() => useReveal())

    // Content must never be left hidden behind an observer that cannot run.
    expect(result.current.visible).toBe(true)
  })

  it('reports visible immediately when reduced motion is preferred', () => {
    mockMatchMedia(true)
    const observe = vi.fn()
    globalThis.IntersectionObserver = vi.fn().mockImplementation(() => ({
      observe,
      unobserve: vi.fn(),
      disconnect: vi.fn(),
    })) as unknown as typeof IntersectionObserver

    const { result } = renderHook(() => useReveal())

    expect(result.current.visible).toBe(true)
    expect(observe).not.toHaveBeenCalled()
  })

  it('starts hidden and observes when motion is allowed', () => {
    mockMatchMedia(false)
    const observe = vi.fn()
    globalThis.IntersectionObserver = vi.fn().mockImplementation(() => ({
      observe,
      unobserve: vi.fn(),
      disconnect: vi.fn(),
    })) as unknown as typeof IntersectionObserver

    const { result } = renderHook(() => useReveal())
    // The ref has to be attached for observation to begin.
    expect(result.current.ref).toBeDefined()
    expect(result.current.visible).toBe(false)
  })
})
