# Squad Platform

A multi-agent platform for software development where AI agents with different roles (PM, Tech Lead, Frontend Developer, Backend Developer) collaborate to complete tasks.

## Architecture

### Backend (Python/FastAPI + LangChain/LangGraph)

The backend is built with FastAPI and uses LangGraph for multi-agent orchestration. Each agent has specific responsibilities and can communicate with other agents through a shared state.

**Key Components:**
- **Agents**: PM, Tech Lead, Frontend Dev, Backend Dev - each with defined responsibilities and tools
- **Orchestrator**: LangGraph-based workflow that coordinates agent interactions
- **Tools**: Integrations with external services like Devin for code generation
- **API**: RESTful endpoints for task management and WebSocket for real-time updates

### Frontend (React + TypeScript)

A modern React application with:
- Dashboard for task management
- Task detail view with agent message history
- Agents page showing squad capabilities
- Real-time updates via WebSocket

## Agent Roles

| Role | Description | Tools |
|------|-------------|-------|
| **PM** | Creates tasks, defines acceptance criteria, prioritizes work | task_create, task_update, notify_stakeholder |
| **Tech Lead** | Reviews technical approaches, identifies risks, approves plans | code_review, architecture_review, approve_plan |
| **Frontend Dev** | Implements UI features using React | code_generate, devin_request, file_write, npm_run |
| **Backend Dev** | Implements API endpoints and business logic | code_generate, devin_request, file_write, database_migrate |

## Getting Started

### Prerequisites

- Python 3.11+
- Node.js 18+
- PostgreSQL
- Poetry (Python package manager)

### Backend Setup

```bash
cd backend

# Install dependencies
poetry install

# Copy environment file and configure
cp .env.example .env
# Edit .env with your OpenAI API key and database URL

# Run the development server
poetry run uvicorn app.main:app --reload
```

### Frontend Setup

```bash
cd frontend

# Install dependencies
npm install

# Copy environment file
cp .env.example .env

# Run the development server
npm run dev
```

### Environment Variables

**Backend (.env):**
```
OPENAI_API_KEY=your-openai-api-key
OPENAI_MODEL=gpt-4-turbo-preview
DATABASE_URL=postgresql+asyncpg://user:password@localhost:5432/squad
DEVIN_API_KEY=your-devin-api-key (optional)
```

**Frontend (.env):**
```
VITE_API_URL=http://localhost:8000
```

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | /api/tasks | Create a new task |
| GET | /api/tasks | List all tasks |
| GET | /api/tasks/{id} | Get task details |
| PATCH | /api/tasks/{id} | Update a task |
| DELETE | /api/tasks/{id} | Delete a task |
| POST | /api/tasks/{id}/run | Execute task with agent squad |
| GET | /api/tasks/{id}/messages | Get task messages |
| GET | /api/tasks/{id}/artifacts | Get task artifacts |
| GET | /api/agents | List available agents |
| WS | /ws/tasks/{id} | Real-time task updates |

## How It Works

1. **Create a Task**: Define what you want to build with a title, description, and acceptance criteria
2. **Run with Squad**: Click "Run with Squad" to start the agent workflow
3. **Agent Collaboration**: 
   - PM analyzes the task and creates acceptance criteria
   - Tech Lead reviews and creates an implementation plan
   - Frontend/Backend Dev implements the solution
4. **Review Results**: View agent messages and artifacts in the task detail page

## Project Structure

```
squad/
├── backend/
│   ├── app/
│   │   ├── agents/          # Agent definitions and orchestrator
│   │   │   ├── roles/       # Individual agent implementations
│   │   │   ├── base.py      # Base agent class
│   │   │   └── orchestrator.py  # LangGraph workflow
│   │   ├── api/             # API routes
│   │   ├── models/          # Database models
│   │   ├── schemas/         # Pydantic schemas
│   │   ├── tools/           # Tool integrations (Devin, etc.)
│   │   ├── config.py        # Configuration
│   │   └── main.py          # FastAPI application
│   └── pyproject.toml
├── frontend/
│   ├── src/
│   │   ├── components/      # React components
│   │   ├── pages/           # Page components
│   │   ├── hooks/           # Custom hooks
│   │   ├── lib/             # Utilities and API client
│   │   └── types/           # TypeScript types
│   └── package.json
└── README.md
```

## Future Enhancements

- GitHub/GitLab integration for direct code commits
- More agent roles (QA, DevOps, Designer)
- Custom workflow definitions
- Agent memory and learning
- Multi-project support
- Team collaboration features

## License

MIT
