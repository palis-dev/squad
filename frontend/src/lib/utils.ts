import { clsx, type ClassValue } from 'clsx'
import { twMerge } from 'tailwind-merge'

export function cn(...inputs: ClassValue[]) {
  return twMerge(clsx(inputs))
}

export function formatDate(dateString: string): string {
  return new Date(dateString).toLocaleDateString('en-US', {
    year: 'numeric',
    month: 'short',
    day: 'numeric',
    hour: '2-digit',
    minute: '2-digit',
  })
}

export function getStatusColor(status: string): string {
  switch (status) {
    case 'pending':
      return 'bg-gray-100 text-gray-800'
    case 'in_progress':
      return 'bg-blue-100 text-blue-800'
    case 'in_review':
      return 'bg-yellow-100 text-yellow-800'
    case 'completed':
      return 'bg-green-100 text-green-800'
    case 'failed':
      return 'bg-red-100 text-red-800'
    default:
      return 'bg-gray-100 text-gray-800'
  }
}

export function getAgentColor(role: string): string {
  switch (role) {
    case 'pm':
      return 'bg-purple-100 text-purple-800 border-purple-200'
    case 'tech_lead':
      return 'bg-blue-100 text-blue-800 border-blue-200'
    case 'frontend_dev':
      return 'bg-green-100 text-green-800 border-green-200'
    case 'backend_dev':
      return 'bg-orange-100 text-orange-800 border-orange-200'
    default:
      return 'bg-gray-100 text-gray-800 border-gray-200'
  }
}

export function getAgentName(role: string): string {
  switch (role) {
    case 'pm':
      return 'Product Manager'
    case 'tech_lead':
      return 'Tech Lead'
    case 'frontend_dev':
      return 'Frontend Dev'
    case 'backend_dev':
      return 'Backend Dev'
    case 'system':
      return 'System'
    default:
      return role
  }
}
