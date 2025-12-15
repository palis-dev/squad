import type { Agent } from '../types'
import { cn, getAgentColor } from '../lib/utils'
import { Wrench } from 'lucide-react'

interface AgentCardProps {
  agent: Agent
}

export default function AgentCard({ agent }: AgentCardProps) {
  return (
    <div className="bg-white rounded-lg shadow p-6">
      <div className="flex items-start gap-4">
        <div
          className={cn(
            'flex-shrink-0 w-12 h-12 rounded-full flex items-center justify-center text-lg font-bold border-2',
            getAgentColor(agent.role)
          )}
        >
          {agent.name.charAt(0)}
        </div>
        <div className="flex-1 min-w-0">
          <h3 className="text-lg font-medium text-gray-900">{agent.name}</h3>
          <p className="text-sm text-gray-500">{agent.description}</p>
        </div>
      </div>
      
      <div className="mt-4">
        <h4 className="text-sm font-medium text-gray-900 mb-2">Responsibilities</h4>
        <ul className="space-y-1">
          {agent.responsibilities.map((responsibility, index) => (
            <li key={index} className="text-sm text-gray-600 flex items-start">
              <span className="text-primary-500 mr-2">-</span>
              {responsibility}
            </li>
          ))}
        </ul>
      </div>
      
      <div className="mt-4">
        <h4 className="text-sm font-medium text-gray-900 mb-2 flex items-center">
          <Wrench className="w-4 h-4 mr-1" />
          Tools
        </h4>
        <div className="flex flex-wrap gap-2">
          {agent.tools.map((tool) => (
            <span
              key={tool}
              className="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-gray-100 text-gray-800"
            >
              {tool}
            </span>
          ))}
        </div>
      </div>
    </div>
  )
}
