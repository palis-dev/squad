import { useState, useEffect } from 'react'
import { useParams, useNavigate } from 'react-router-dom'
import { ArrowLeft, Play, Trash2, Clock } from 'lucide-react'
import type { Task, Message, Artifact } from '../types'
import { api } from '../lib/api'
import { cn, formatDate, getStatusColor } from '../lib/utils'
import ChatMessage from '../components/ChatMessage'

export default function TaskDetail() {
  const { taskId } = useParams<{ taskId: string }>()
  const navigate = useNavigate()
  const [task, setTask] = useState<Task | null>(null)
  const [messages, setMessages] = useState<Message[]>([])
  const [artifacts, setArtifacts] = useState<Artifact[]>([])
  const [loading, setLoading] = useState(true)
  const [running, setRunning] = useState(false)
  const [activeTab, setActiveTab] = useState<'messages' | 'artifacts'>('messages')

  useEffect(() => {
    if (!taskId) return

    const fetchData = async () => {
      try {
        setLoading(true)
        const [taskData, messagesData, artifactsData] = await Promise.all([
          api.tasks.get(parseInt(taskId)),
          api.tasks.getMessages(parseInt(taskId)),
          api.tasks.getArtifacts(parseInt(taskId)),
        ])
        setTask(taskData)
        setMessages(messagesData)
        setArtifacts(artifactsData)
      } catch (err) {
        console.error('Failed to fetch task:', err)
      } finally {
        setLoading(false)
      }
    }

    fetchData()
  }, [taskId])

  const handleRunTask = async () => {
    if (!taskId) return
    try {
      setRunning(true)
      await api.tasks.run(parseInt(taskId))
      const updatedTask = await api.tasks.get(parseInt(taskId))
      setTask(updatedTask)
    } catch (err) {
      console.error('Failed to run task:', err)
    } finally {
      setRunning(false)
    }
  }

  const handleDeleteTask = async () => {
    if (!taskId || !confirm('Are you sure you want to delete this task?')) return
    try {
      await api.tasks.delete(parseInt(taskId))
      navigate('/')
    } catch (err) {
      console.error('Failed to delete task:', err)
    }
  }

  if (loading) {
    return (
      <div className="flex items-center justify-center py-12">
        <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-primary-600" />
      </div>
    )
  }

  if (!task) {
    return (
      <div className="text-center py-12">
        <p className="text-gray-500">Task not found</p>
        <button
          onClick={() => navigate('/')}
          className="mt-4 text-primary-600 hover:text-primary-700"
        >
          Go back to dashboard
        </button>
      </div>
    )
  }

  return (
    <div>
      <button
        onClick={() => navigate('/')}
        className="inline-flex items-center text-sm text-gray-500 hover:text-gray-700 mb-4"
      >
        <ArrowLeft className="w-4 h-4 mr-1" />
        Back to tasks
      </button>

      <div className="bg-white rounded-lg shadow">
        <div className="p-6 border-b border-gray-200">
          <div className="flex items-start justify-between">
            <div className="flex-1">
              <div className="flex items-center gap-3">
                <h1 className="text-2xl font-bold text-gray-900">{task.title}</h1>
                <span
                  className={cn(
                    'inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium',
                    getStatusColor(task.status)
                  )}
                >
                  {task.status.replace('_', ' ')}
                </span>
              </div>
              {task.description && (
                <p className="mt-2 text-gray-600">{task.description}</p>
              )}
              <div className="mt-4 flex items-center text-sm text-gray-500">
                <Clock className="w-4 h-4 mr-1" />
                Created {formatDate(task.created_at)}
              </div>
            </div>
            <div className="flex items-center gap-2">
              <button
                onClick={handleRunTask}
                disabled={running || task.status === 'in_progress'}
                className="inline-flex items-center px-4 py-2 border border-transparent shadow-sm text-sm font-medium rounded-md text-white bg-green-600 hover:bg-green-700 disabled:opacity-50 disabled:cursor-not-allowed"
              >
                <Play className="w-4 h-4 mr-2" />
                {running ? 'Starting...' : 'Run with Squad'}
              </button>
              <button
                onClick={handleDeleteTask}
                className="inline-flex items-center px-3 py-2 border border-gray-300 shadow-sm text-sm font-medium rounded-md text-red-600 bg-white hover:bg-red-50"
              >
                <Trash2 className="w-4 h-4" />
              </button>
            </div>
          </div>

          {task.acceptance_criteria && (
            <div className="mt-6">
              <h3 className="text-sm font-medium text-gray-900">Acceptance Criteria</h3>
              <p className="mt-1 text-sm text-gray-600 whitespace-pre-wrap">
                {task.acceptance_criteria}
              </p>
            </div>
          )}
        </div>

        <div className="border-b border-gray-200">
          <nav className="flex -mb-px">
            <button
              onClick={() => setActiveTab('messages')}
              className={cn(
                'px-6 py-3 text-sm font-medium border-b-2',
                activeTab === 'messages'
                  ? 'border-primary-500 text-primary-600'
                  : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300'
              )}
            >
              Messages ({messages.length})
            </button>
            <button
              onClick={() => setActiveTab('artifacts')}
              className={cn(
                'px-6 py-3 text-sm font-medium border-b-2',
                activeTab === 'artifacts'
                  ? 'border-primary-500 text-primary-600'
                  : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300'
              )}
            >
              Artifacts ({artifacts.length})
            </button>
          </nav>
        </div>

        <div className="p-6">
          {activeTab === 'messages' ? (
            messages.length === 0 ? (
              <p className="text-center text-gray-500 py-8">
                No messages yet. Run the task to see agent communications.
              </p>
            ) : (
              <div className="divide-y divide-gray-200">
                {messages.map((message) => (
                  <ChatMessage key={message.id} message={message} />
                ))}
              </div>
            )
          ) : artifacts.length === 0 ? (
            <p className="text-center text-gray-500 py-8">
              No artifacts yet. Artifacts will appear as agents produce outputs.
            </p>
          ) : (
            <div className="space-y-4">
              {artifacts.map((artifact) => (
                <div key={artifact.id} className="bg-gray-50 rounded-lg p-4">
                  <div className="flex items-center justify-between mb-2">
                    <span className="font-medium text-gray-900">{artifact.name}</span>
                    <span className="text-xs text-gray-500 bg-gray-200 px-2 py-1 rounded">
                      {artifact.artifact_type}
                    </span>
                  </div>
                  <pre className="text-sm text-gray-700 whitespace-pre-wrap overflow-x-auto">
                    {artifact.content}
                  </pre>
                </div>
              ))}
            </div>
          )}
        </div>
      </div>
    </div>
  )
}
