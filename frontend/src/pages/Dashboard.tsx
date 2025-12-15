import { useState, useEffect } from 'react'
import { Plus, RefreshCw } from 'lucide-react'
import type { Task } from '../types'
import { api } from '../lib/api'
import TaskCard from '../components/TaskCard'
import CreateTaskModal from '../components/CreateTaskModal'

export default function Dashboard() {
  const [tasks, setTasks] = useState<Task[]>([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)
  const [isModalOpen, setIsModalOpen] = useState(false)
  const [filter, setFilter] = useState<string>('')

  const fetchTasks = async () => {
    try {
      setLoading(true)
      setError(null)
      const response = await api.tasks.list(filter || undefined)
      setTasks(response.tasks)
    } catch (err) {
      setError('Failed to load tasks')
      console.error(err)
    } finally {
      setLoading(false)
    }
  }

  useEffect(() => {
    fetchTasks()
  }, [filter])

  const handleCreateTask = async (data: { title: string; description: string; acceptance_criteria: string }) => {
    try {
      await api.tasks.create(data)
      fetchTasks()
    } catch (err) {
      console.error('Failed to create task:', err)
    }
  }

  return (
    <div>
      <div className="flex items-center justify-between mb-6">
        <div>
          <h1 className="text-2xl font-bold text-gray-900">Tasks</h1>
          <p className="text-sm text-gray-500 mt-1">
            Manage and track your squad's tasks
          </p>
        </div>
        <div className="flex items-center gap-3">
          <button
            onClick={fetchTasks}
            className="inline-flex items-center px-3 py-2 border border-gray-300 shadow-sm text-sm font-medium rounded-md text-gray-700 bg-white hover:bg-gray-50"
          >
            <RefreshCw className="w-4 h-4 mr-2" />
            Refresh
          </button>
          <button
            onClick={() => setIsModalOpen(true)}
            className="inline-flex items-center px-4 py-2 border border-transparent shadow-sm text-sm font-medium rounded-md text-white bg-primary-600 hover:bg-primary-700"
          >
            <Plus className="w-4 h-4 mr-2" />
            New Task
          </button>
        </div>
      </div>

      <div className="mb-6">
        <div className="flex gap-2">
          {['', 'pending', 'in_progress', 'in_review', 'completed', 'failed'].map((status) => (
            <button
              key={status}
              onClick={() => setFilter(status)}
              className={`px-3 py-1.5 text-sm font-medium rounded-md ${
                filter === status
                  ? 'bg-primary-100 text-primary-700'
                  : 'text-gray-500 hover:text-gray-700 hover:bg-gray-100'
              }`}
            >
              {status === '' ? 'All' : status.replace('_', ' ')}
            </button>
          ))}
        </div>
      </div>

      {loading ? (
        <div className="flex items-center justify-center py-12">
          <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-primary-600" />
        </div>
      ) : error ? (
        <div className="text-center py-12">
          <p className="text-red-600">{error}</p>
          <button
            onClick={fetchTasks}
            className="mt-4 text-primary-600 hover:text-primary-700"
          >
            Try again
          </button>
        </div>
      ) : tasks.length === 0 ? (
        <div className="text-center py-12 bg-white rounded-lg shadow">
          <p className="text-gray-500">No tasks found</p>
          <button
            onClick={() => setIsModalOpen(true)}
            className="mt-4 text-primary-600 hover:text-primary-700"
          >
            Create your first task
          </button>
        </div>
      ) : (
        <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-3">
          {tasks.map((task) => (
            <TaskCard key={task.id} task={task} />
          ))}
        </div>
      )}

      <CreateTaskModal
        isOpen={isModalOpen}
        onClose={() => setIsModalOpen(false)}
        onSubmit={handleCreateTask}
      />
    </div>
  )
}
