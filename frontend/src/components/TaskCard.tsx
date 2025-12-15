import { Link } from 'react-router-dom'
import { Clock, ArrowRight } from 'lucide-react'
import type { Task } from '../types'
import { cn, formatDate, getStatusColor } from '../lib/utils'

interface TaskCardProps {
  task: Task
}

export default function TaskCard({ task }: TaskCardProps) {
  return (
    <Link
      to={`/tasks/${task.id}`}
      className="block bg-white rounded-lg shadow hover:shadow-md transition-shadow"
    >
      <div className="p-6">
        <div className="flex items-start justify-between">
          <div className="flex-1 min-w-0">
            <h3 className="text-lg font-medium text-gray-900 truncate">
              {task.title}
            </h3>
            {task.description && (
              <p className="mt-1 text-sm text-gray-500 line-clamp-2">
                {task.description}
              </p>
            )}
          </div>
          <span
            className={cn(
              'ml-4 inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium',
              getStatusColor(task.status)
            )}
          >
            {task.status.replace('_', ' ')}
          </span>
        </div>
        <div className="mt-4 flex items-center justify-between text-sm text-gray-500">
          <div className="flex items-center">
            <Clock className="w-4 h-4 mr-1" />
            {formatDate(task.created_at)}
          </div>
          <ArrowRight className="w-4 h-4" />
        </div>
      </div>
    </Link>
  )
}
