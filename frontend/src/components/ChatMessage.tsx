import type { Message } from '../types'
import { cn, formatDate, getAgentColor, getAgentName } from '../lib/utils'

interface ChatMessageProps {
  message: Message
}

export default function ChatMessage({ message }: ChatMessageProps) {
  return (
    <div className="flex gap-3 py-4">
      <div
        className={cn(
          'flex-shrink-0 w-8 h-8 rounded-full flex items-center justify-center text-xs font-medium border',
          getAgentColor(message.agent_role)
        )}
      >
        {message.agent_role.charAt(0).toUpperCase()}
      </div>
      <div className="flex-1 min-w-0">
        <div className="flex items-center gap-2">
          <span className="font-medium text-gray-900">
            {getAgentName(message.agent_role)}
          </span>
          <span className="text-xs text-gray-500">
            {formatDate(message.created_at)}
          </span>
        </div>
        <div className="mt-1 text-sm text-gray-700 whitespace-pre-wrap">
          {message.content}
        </div>
      </div>
    </div>
  )
}
