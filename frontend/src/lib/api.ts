import type { Task, TaskListResponse, Message, Artifact, AgentListResponse } from '../types'

const API_URL = import.meta.env.VITE_API_URL || ''

async function fetchApi<T>(endpoint: string, options?: RequestInit): Promise<T> {
  const response = await fetch(`${API_URL}${endpoint}`, {
    ...options,
    headers: {
      'Content-Type': 'application/json',
      ...options?.headers,
    },
  })

  if (!response.ok) {
    throw new Error(`API error: ${response.status}`)
  }

  return response.json()
}

export const api = {
  tasks: {
    list: (status?: string) => {
      const params = status ? `?status=${status}` : ''
      return fetchApi<TaskListResponse>(`/api/tasks${params}`)
    },
    get: (id: number) => fetchApi<Task>(`/api/tasks/${id}`),
    create: (data: { title: string; description?: string; acceptance_criteria?: string }) =>
      fetchApi<Task>('/api/tasks', {
        method: 'POST',
        body: JSON.stringify(data),
      }),
    update: (id: number, data: Partial<Task>) =>
      fetchApi<Task>(`/api/tasks/${id}`, {
        method: 'PATCH',
        body: JSON.stringify(data),
      }),
    delete: (id: number) =>
      fetchApi<{ message: string }>(`/api/tasks/${id}`, {
        method: 'DELETE',
      }),
    run: (id: number) =>
      fetchApi<{ message: string; task_id: number }>(`/api/tasks/${id}/run`, {
        method: 'POST',
      }),
    getMessages: (id: number) => fetchApi<Message[]>(`/api/tasks/${id}/messages`),
    getArtifacts: (id: number) => fetchApi<Artifact[]>(`/api/tasks/${id}/artifacts`),
  },
  agents: {
    list: () => fetchApi<AgentListResponse>('/api/agents'),
  },
}
