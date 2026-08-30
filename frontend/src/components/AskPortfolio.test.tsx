import { render, screen } from '@testing-library/react'
import userEvent from '@testing-library/user-event'
import { beforeEach, describe, expect, it, vi } from 'vitest'

import { AskPortfolio } from './AskPortfolio'
import { askPortfolio } from '../lib/api'
import type { ChatAnswer } from '../types/content'

vi.mock('../lib/api', () => ({ askPortfolio: vi.fn() }))
const mockedAsk = vi.mocked(askPortfolio)

const grounded: ChatAnswer = {
  answer: 'She worked as an AI Engineer at Spark New Zealand.',
  grounded: true,
  sources: [{ source: 'AI Engineer · Spark New Zealand', type: 'role' }],
  retrieval_ms: 1.2,
  generation_ms: 3.4,
  provider: 'template',
}

const refused: ChatAnswer = {
  answer: "I don't have evidence of that in the portfolio.",
  grounded: false,
  sources: [],
  retrieval_ms: 1.0,
  generation_ms: 0,
  provider: 'none',
}

const pending = <T,>() => new Promise<T>(() => {})

async function ask(question = 'What AI experience does she have?') {
  const user = userEvent.setup()
  render(<AskPortfolio />)
  await user.type(screen.getByRole('textbox', { name: /ask/i }), question)
  await user.click(screen.getByRole('button', { name: /ask/i }))
  return user
}

describe('AskPortfolio', () => {
  beforeEach(() => vi.clearAllMocks())

  it('renders the answer to a grounded question', async () => {
    mockedAsk.mockResolvedValue(grounded)
    await ask()

    expect(await screen.findByText(/AI Engineer at Spark New Zealand/i)).toBeInTheDocument()
  })

  it('shows the refusal verbatim when the question is out of scope', async () => {
    mockedAsk.mockResolvedValue(refused)
    await ask('What is the capital of France?')

    expect(await screen.findByText(/don't have evidence/i)).toBeInTheDocument()
  })

  it('shows a loading state while the request is in flight', async () => {
    mockedAsk.mockReturnValue(pending<ChatAnswer>())
    await ask()

    expect(screen.getByRole('status')).toBeInTheDocument()
  })

  it('shows an error state when the request fails', async () => {
    mockedAsk.mockRejectedValue(new Error('network down'))
    await ask()

    expect(await screen.findByRole('alert')).toBeInTheDocument()
  })

  it('does not submit an empty question', async () => {
    const user = userEvent.setup()
    render(<AskPortfolio />)

    await user.click(screen.getByRole('button', { name: /ask/i }))

    expect(mockedAsk).not.toHaveBeenCalled()
  })
})
