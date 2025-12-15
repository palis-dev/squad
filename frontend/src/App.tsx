import { Routes, Route } from 'react-router-dom'
import Layout from './components/Layout'
import Dashboard from './pages/Dashboard'
import TaskDetail from './pages/TaskDetail'
import Agents from './pages/Agents'

function App() {
  return (
    <Routes>
      <Route path="/" element={<Layout />}>
        <Route index element={<Dashboard />} />
        <Route path="tasks/:taskId" element={<TaskDetail />} />
        <Route path="agents" element={<Agents />} />
      </Route>
    </Routes>
  )
}

export default App
