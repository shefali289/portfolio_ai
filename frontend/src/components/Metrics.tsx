import type { AgentStep } from '../types/content'

interface MetricsProps {
  endpoint: string
  chunks?: number
  retrievalMs?: number
  generationMs?: number
  provider?: string
  tools?: string[]
  steps?: AgentStep[]
}

/**
 * What the response actually cost and cited. Rendered only in Engineer Mode.
 *
 * **A metric that is absent is omitted, never shown as zero.** Rendering
 * `0.0 ms` would present a fabricated measurement as a real one — the same
 * failure as inventing portfolio content, wearing a different costume. Every
 * row below is conditional on the value actually being present.
 */
export function Metrics({
  endpoint,
  chunks,
  retrievalMs,
  generationMs,
  provider,
  tools,
  steps,
}: MetricsProps) {
  const rows: Array<[string, string]> = []

  if (endpoint) rows.push(['Endpoint', endpoint])
  if (typeof chunks === 'number') rows.push(['Chunks retrieved', String(chunks)])
  if (typeof retrievalMs === 'number') rows.push(['Retrieval', `${retrievalMs.toFixed(2)} ms`])
  if (typeof generationMs === 'number') rows.push(['Generation', `${generationMs.toFixed(2)} ms`])
  if (provider) rows.push(['Provider', provider])
  if (tools && tools.length > 0) rows.push(['Tool used', tools.join(', ')])

  const chain = steps ?? []
  if (rows.length === 0 && chain.length === 0) return null

  return (
    <div
      className="mt-5 rounded-2xl p-4"
      style={{
        border: '1px dashed var(--border-subtle)',
        backgroundColor: 'var(--surface-sunken)',
      }}
    >
      <p className="eyebrow">Engineer Mode</p>

      <dl className="mt-3 grid gap-x-6 gap-y-2 sm:grid-cols-2">
        {rows.map(([label, value]) => (
          <div key={label} className="flex items-baseline justify-between gap-3">
            <dt className="meta">{label}</dt>
            <dd className="meta" style={{ color: 'var(--text-primary)' }}>
              {value}
            </dd>
          </div>
        ))}
      </dl>

      {chain.length > 0 && (
        <ul className="mt-4 list-none space-y-1 p-0">
          {chain.map((step) => (
            <li key={step.name} className="flex items-baseline justify-between gap-3">
              <span className="meta">{step.label}</span>
              <span className="meta" style={{ color: 'var(--text-primary)' }}>
                {step.ms.toFixed(2)} ms
              </span>
            </li>
          ))}
        </ul>
      )}
    </div>
  )
}
