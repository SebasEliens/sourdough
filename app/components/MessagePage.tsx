'use client'

import { useState, useCallback } from 'react'
import { AppLayout } from './AppLayout'
import { MessageLog } from './MessageLog'
import { MessageInput } from './MessageInput'
import type { LogEntry } from '@/app/types'

export function MessagePage() {
  const [entries, setEntries] = useState<LogEntry[]>([])

  const handleSend = useCallback((text: string) => {
    if (!text.trim()) return
    const entry: LogEntry = {
      id: crypto.randomUUID(),
      text: text.trim(),
      timestamp: new Date().toISOString(),
      mocked: true,
    }
    setEntries((prev) => [entry, ...prev])
  }, [])

  return (
    <AppLayout>
      <MessageInput onSend={handleSend} />
      <MessageLog entries={entries} />
    </AppLayout>
  )
}
