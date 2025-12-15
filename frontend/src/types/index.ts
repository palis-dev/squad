export type TaskStatus = 'pending' | 'in_progress' | 'in_review' | 'completed' | 'failed'

export interface Task {
  id: number
  title: string
  description: string | null
  status: TaskStatus
  acceptance_criteria: string | null
  created_at: string
  updated_at: string
}

export interface Message {
  id: number
  task_id: number
  agent_role: string
  content: string
  message_type: string
  created_at: string
}

export interface Artifact {
  id: number
  task_id: number
  artifact_type: string
  name: string
  content: string
  created_at: string
}

export interface Agent {
  role: string
  name: string
  description: string
  responsibilities: string[]
  tools: string[]
}

export interface TaskListResponse {
  tasks: Task[]
  total: number
}

export interface AgentListResponse {
  agents: Agent[]
}
