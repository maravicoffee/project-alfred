import { useState } from 'react'
import Sidebar from './components/Sidebar'
import ConversationPanel from './components/ConversationPanel'
import ConversationList from './components/ConversationList'
import PreviewPanel from './components/PreviewPanel'
import './App.css'

function App() {
  const [selectedConversation, setSelectedConversation] = useState<string | null>(null)
  const [isSidebarCollapsed, setIsSidebarCollapsed] = useState(true)
  const [isPreviewVisible, setIsPreviewVisible] = useState(false)
  const [userId] = useState<string>(() => {
    // Generate or retrieve user ID
    const stored = localStorage.getItem('alfred_user_id')
    if (stored) return stored
    const newId = crypto.randomUUID()
    localStorage.setItem('alfred_user_id', newId)
    return newId
  })

  return (
    <div className="flex w-screen overflow-hidden bg-forest-light" style={{ height: '100dvh' }}>
      {/* Icon Sidebar - Collapsible */}
      <div 
        className={`h-full transition-all duration-300 ease-in-out flex-shrink-0 ${
          isSidebarCollapsed ? 'w-16' : 'w-64'
        }`}
        onMouseEnter={() => setIsSidebarCollapsed(false)}
        onMouseLeave={() => setIsSidebarCollapsed(true)}
      >
        <Sidebar 
          isCollapsed={isSidebarCollapsed} 
          onToggle={() => setIsSidebarCollapsed(!isSidebarCollapsed)}
        />
      </div>
      
      {/* Conversation List */}
      <div className="w-64 bg-forest-dark border-r border-forest-darkest flex-shrink-0 h-full overflow-hidden">
        <ConversationList 
          userId={userId}
          onSelectConversation={setSelectedConversation}
        />
      </div>
      
      {/* Middle Panel - Main Conversation Area */}
      <div className="flex-1 min-w-0 h-full overflow-hidden">
        <ConversationPanel 
          userId={userId} 
          conversationId={selectedConversation}
          onTogglePreview={() => setIsPreviewVisible(!isPreviewVisible)}
          isPreviewVisible={isPreviewVisible}
        />
      </div>
      
      {/* Right Panel - Preview (Collapsible) */}
      {isPreviewVisible && (
        <div className="w-96 border-l border-gray-200 flex-shrink-0 h-full overflow-hidden transition-all duration-300 ease-in-out">
          <PreviewPanel onClose={() => setIsPreviewVisible(false)} />
        </div>
      )}
    </div>
  )
}

export default App
