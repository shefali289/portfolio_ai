import { render, screen } from '@testing-library/react'
import { describe, expect, it } from 'vitest'

import { Metrics } from './Metrics'

const full = {
  endpoint: '/api/ai/chat',
  chunks: 4,
  retrievalMs: 1.24,
  generationMs: 3.5,
  provider: 'template',
  tools: ['portfolio_ai'],
}

describe('Metrics', () => {
  it('renders every metric it is given', () => {
    render(<Metrics {...full} />)

    expect(screen.getByText('/api/ai/chat')).toBeInTheDocument()
    expect(screen.getByText(/chunks retrieved/i)).toBeInTheDocument()
    expect(screen.getByText(/template/)).toBeInTheDocument()
    expect(screen.getByText(/portfolio_ai/)).toBeInTheDocument()
  })

  it('shows both timings', () => {
    render(<Metrics {...full} />)

    expect(screen.getByText(/retrieval/i)).toBeInTheDocument()
    expect(screen.getByText(/generation/i)).toBeInTheDocument()
  })

  it('omits a metric that is absent rather than showing zero', () => {
    // The load-bearing case. A rendered "0.0 ms" would present a fabricated
    // measurement as a real one - inventing content in a different costume.
    render(<Metrics {...full} generationMs={undefined} />)

    expect(screen.queryByText(/generation/i)).not.toBeInTheDocument()
    expect(screen.queryByText(/0\.0/)).not.toBeInTheDocument()
  })

  it('omits the tool row when no tool was used', () => {
    render(<Metrics {...full} tools={[]} />)

    expect(screen.queryByText(/tool used/i)).not.toBeInTheDocument()
  })

  it('renders chain steps with their timings when given', () => {
    render(
      <Metrics
        endpoint="/api/ai/job-match"
        provider="template"
        steps={[
          { name: 'requirement', label: 'Understanding the role', status: 'done', ms: 2.1 },
          { name: 'portfolio', label: 'Searching the portfolio', status: 'done', ms: 5.4 },
        ]}
      />,
    )

    expect(screen.getByText(/Understanding the role/)).toBeInTheDocument()
    expect(screen.getByText(/Searching the portfolio/)).toBeInTheDocument()
  })

  it('renders nothing at all when it has no metrics to show', () => {
    const { container } = render(<Metrics endpoint="" />)

    expect(container).toBeEmptyDOMElement()
  })
})
