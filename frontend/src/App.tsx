import { useState } from 'react'
import Sidebar from './components/Sidebar'
import SharedHeader from './components/SharedHeader'
import LandingPage from './pages/LandingPage'
import TaskView from './pages/TaskView'
import './App.css'

type View = 'landing' | 'task' | 'conversations'

function App() {
  const [isSidebarCollapsed, setIsSidebarCollapsed] = useState(false)
  const [isPreviewVisible, setIsPreviewVisible] = useState(false)
  const [currentView, setCurrentView] = useState<View>('landing')
  
  // Determine header variant based on current view
  const headerVariant = currentView === 'landing' ? 'landing' : 'task'

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
          onNewChat={() => setCurrentView('landing')}
          onShowConversations={() => setCurrentView('conversations')}
        />
      </div>
      
      {/* Right Side - Header + Content Area */}
      <div className="flex-1 flex flex-col h-full overflow-hidden">
        {/* Shared Header */}
        <SharedHeader 
          title="Alfred 1.0"
          isPreviewVisible={isPreviewVisible}
          onTogglePreview={() => setIsPreviewVisible(!isPreviewVisible)}
          variant={headerVariant}
        />
        
        {/* Content Area - Switch based on current view */}
        {currentView === 'landing' && (
          <LandingPage onStartTask={() => setCurrentView('task')} />
        )}
        
        {(currentView === 'task' || currentView === 'conversations') && (
          <TaskView 
            isPreviewVisible={isPreviewVisible}
            onTogglePreview={() => setIsPreviewVisible(!isPreviewVisible)}
          />
        )}
      </div>
    </div>
  )
}

export default App
