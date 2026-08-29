import type { ReactNode } from 'react'

import { useReveal } from '../hooks/useReveal'

interface RevealProps {
  children: ReactNode
}

/**
 * Wraps a section in a scroll-triggered fade-and-rise.
 *
 * Degrades open: with no IntersectionObserver, or under
 * `prefers-reduced-motion`, `useReveal` reports visible from the first render
 * and no class that could hide content is ever applied.
 */
export function Reveal({ children }: RevealProps) {
  const { ref, visible } = useReveal()

  return (
    <div ref={ref} className={`reveal ${visible ? 'reveal-in' : 'reveal-armed'}`}>
      {children}
    </div>
  )
}
