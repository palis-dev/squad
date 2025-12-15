import { useState, useEffect } from 'react'
import { RefreshCw } from 'lucide-react'
import type { Agent } from '../types'
import { api } from '../lib/api'
import AgentCard from '../components/AgentCard'

export default function Agents() {
  const [agents, setAgents] = useState<Agent[]>([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)

  const fetchAgents = async () => {
    try {
      setLoading(true)
      setError(null)
      const response = await api.agents.list()
      setAgents(response.agents)
    } catch (err) {
      setError('Failed to load agents')
      console.error(err)
    } finally {
      setLoading(false)
    }
  }

  useEffect(() => {
    fetchAgents()
  }, [])

  return (
    <div>
      <div className="flex items-center justify-between mb-6">
        <div>
          <h1 className="text-2xl font-bold text-gray-900">Squad Agents</h1>
          <p className="text-sm text-gray-500 mt-1">
            Meet your AI development team
          </p>
        </div>
        <button
          onClick={fetchAgents}
          className="inline-flex items-center px-3 py-2 border border-gray-300 shadow-sm text-sm font-medium rounded-md text-gray-700 bg-white hover:bg-gray-50"
        >
          <RefreshCw className="w-4 h-4 mr-2" />
          Refresh
        </button>
      </div>

      {loading ? (
        <div className="flex items-center justify-center py-12">
          <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-primary-600" />
        </div>
      ) : error ? (
        <div className="text-center py-12">
          <p className="text-red-600">{error}</p>
          <button
            onClick={fetchAgents}
            className="mt-4 text-primary-600 hover:text-primary-700"
          >
            Try again
          </button>
        </div>
      ) : (
        <div className="grid gap-6 md:grid-cols-2">
          {agents.map((agent) => (
            <AgentCard key={agent.role} agent={agent} />
          ))}
        </div>
      )}
    </div>
  )
}
