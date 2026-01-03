import { useState } from 'react'
import { BrowserRouter, Routes, Route, useLocation } from 'react-router-dom'
import Sidebar from './components/Sidebar'
import SharedHeader from './components/SharedHeader'
import LandingPage from './pages/LandingPage'
import TaskView from './pages/TaskView'
import './App.css'

function AppContent() {
  const [isSidebarCollapsed, setIsSidebarCollapsed] = useState(false)
  const [isPreviewVisible, setIsPreviewVisible] = useState(false)
  const location = useLocation()
  
  // Determine if we're on landing page or task view
  const isLandingPage = location.pathname === '/'

  return (
    <div className="flex w-screen overflow-hidden bg-forest-light" style={{ height: '100dvh' }}>
      {/* Left Sidebar - Collapsible */}
      <div 
        className={`transition-all duration-300 ease-in-out flex-shrink-0 h-full ${
          isSidebarCollapsed ? 'w-16' : 'w-64'
        }`}
      >
        <Sidebar 
          isCollapsed={isSidebarCollapsed} 
          onToggle={() => setIsSidebarCollapsed(!isSidebarCollapsed)}
          onNewChat={() => {}}
          onShowConversations={() => {}}
        />
      </div>
      
      {/* Right Side - Header + Content Area */}
      <div className="flex-1 flex flex-col h-full overflow-hidden">
        {/* Shared Header */}
        <SharedHeader 
          title="Alfred 1.0"
          isPreviewVisible={isPreviewVisible}
          onTogglePreview={() => setIsPreviewVisible(!isPreviewVisible)}
          variant={isLandingPage ? 'landing' : 'task'}
        />
        
        {/* Content Area */}
        <Routes>
          <Route path="/" element={<LandingPage />} />
          <Route path="/task" element={<TaskView />} />
          <Route path="/task/:id" element={<TaskView />} />
        </Routes>
      </div>
    </div>
  )
}

function App() {
  return (
    <BrowserRouter>
      <AppContent />
    </BrowserRouter>
  )
}

export default App
