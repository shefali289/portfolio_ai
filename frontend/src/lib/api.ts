/**
 * The single typed API client.
 *
 * Components never call `fetch` directly (conventions.md) — every request goes
 * through a method here, so error handling, the base URL and response typing
 * live in exactly one place.
 */

import type { Profile } from '../types/content'

const BASE_URL = import.meta.env.VITE_API_BASE_URL ?? ''

export class ApiError extends Error {
  constructor(
    message: string,
    readonly status?: number,
    options?: ErrorOptions,
  ) {
    super(message, options)
    this.name = 'ApiError'
  }
}

async function request<T>(path: string): Promise<T> {
  let response: Response
  try {
    response = await fetch(`${BASE_URL}${path}`)
  } catch (cause) {
    // Network-level failure: the API is unreachable rather than unhappy.
    // Keep the original error as `cause` so the real reason is not lost.
    throw new ApiError(`Could not reach the API at ${path}`, undefined, { cause })
  }

  if (!response.ok) {
    throw new ApiError(`Request to ${path} failed`, response.status)
  }

  return (await response.json()) as T
}

export function getProfile(): Promise<Profile> {
  return request<Profile>('/api/profile')
}

export function getHealth(): Promise<{ status: string }> {
  return request<{ status: string }>('/api/health')
}
