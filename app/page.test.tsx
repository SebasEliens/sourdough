import { describe, it, expect } from 'vitest'
import { render, screen } from '@testing-library/react'
import userEvent from '@testing-library/user-event'
import { MessagePage } from './components/MessagePage'

describe('MessagePage', () => {
  it('renders message input and empty log', () => {
    render(<MessagePage />)
    expect(screen.getByPlaceholderText(/type a message/i)).toBeInTheDocument()
    expect(screen.getByText(/no messages yet/i)).toBeInTheDocument()
  })

  it('logs message below input when user sends', async () => {
    const user = userEvent.setup()
    render(<MessagePage />)
    const input = screen.getByPlaceholderText(/type a message/i)
    await user.type(input, 'Hello')
    await user.click(screen.getByRole('button', { name: /send/i }))
    expect(screen.getByText('Hello')).toBeInTheDocument()
    expect(screen.getByText(/MOCK/i)).toBeInTheDocument()
  })
})
