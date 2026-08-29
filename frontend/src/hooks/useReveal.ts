import { useCallback, useEffect, useRef, useState } from 'react'

/**
 * Scroll-reveal that degrades *open*.
 *
 * Content is visible by default and animation is added on top — never content
 * hidden awaiting an observer that may never run. If `IntersectionObserver` is
 * missing, or the visitor prefers reduced motion, this reports visible
 * immediately and never observes anything.
 */

function prefersReducedMotion(): boolean {
  if (typeof globalThis.matchMedia !== 'function') return false
  return globalThis.matchMedia('(prefers-reduced-motion: reduce)').matches
}

function canAnimate(): boolean {
  return (
    typeof globalThis.IntersectionObserver === 'function' && !prefersReducedMotion()
  )
}

export interface Reveal {
  /** Attach to the element that should reveal. */
  ref: (node: Element | null) => void
  /** True once revealed — or straight away when animation is not appropriate. */
  visible: boolean
}

export function useReveal(rootMargin = '0px 0px -10% 0px'): Reveal {
  // Computed lazily so the first render is already correct: no flash of hidden
  // content for anyone who cannot or does not want to animate.
  const [visible, setVisible] = useState(() => !canAnimate())
  const nodeRef = useRef<Element | null>(null)

  const ref = useCallback((node: Element | null) => {
    nodeRef.current = node
  }, [])

  useEffect(() => {
    // No setState here: the lazy initial state already resolves to visible
    // when animation is not appropriate, so there is nothing to correct.
    if (!canAnimate()) return

    const node = nodeRef.current
    if (!node) return

    const observer = new IntersectionObserver(
      (entries) => {
        for (const entry of entries) {
          if (entry.isIntersecting) {
            setVisible(true)
            observer.unobserve(entry.target)
          }
        }
      },
      { rootMargin, threshold: 0.05 },
    )

    observer.observe(node)

    return () => observer.disconnect()
  }, [rootMargin])

  return { ref, visible }
}
