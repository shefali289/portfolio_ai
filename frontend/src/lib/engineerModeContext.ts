import { createContext, useContext } from 'react'

/**
 * Engineer Mode state, shared by the toggle and every AI surface.
 *
 * Context and hook live apart from the components that use them so this file
 * exports no component — which is what keeps fast refresh working, and the
 * reason for the split rather than an eslint suppression.
 */
export interface EngineerModeValue {
  enabled: boolean
  toggle: () => void
}

export const STORAGE_KEY = 'engineer-mode'

export const EngineerModeContext = createContext<EngineerModeValue>({
  enabled: false,
  toggle: () => {},
})

export function useEngineerMode(): EngineerModeValue {
  return useContext(EngineerModeContext)
}
