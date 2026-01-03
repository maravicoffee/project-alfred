import { useState } from 'react'
import Sidebar from './components/Sidebar'
import ConversationPanel from './components/ConversationPanel'
import ConversationList from './components/ConversationList'
import PreviewPanel from './components/PreviewPanel'
import './App.css'

function App() {
  const [selectedConversation, setSelectedConversation] = useState<string | null>(null)
  const [isSidebarCollapsed, setIsSidebarCollapsed] = useState(true)
  const [isPreviewVisible, setIsPreviewVisible] = useState(true)
  const [userId] = useState<string>(() => {
    // Generate or retrieve user ID
    const stored = localStorage.getItem('alfred_user_id')
    if (stored) return stored
    const newId = crypto.randomUUID()
    localStorage.setItem('alfred_user_id', newId)
    return newId
  })

  return (
    <div className="flex h-screen w-screen overflow-hidden bg-forest-light">
      {/* Left Sidebar - Collapsible */}
      <div 
        className={`transition-all duration-300 ease-in-out ${
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
      <div className={`transition-all duration-300 ease-in-out ${
        isSidebarCollapsed ? 'w-64' : 'w-72'
      } bg-forest-dark border-r border-forest-darkest flex-shrink-0`}>
        <ConversationList 
          userId={userId}
          onSelectConversation={setSelectedConversation}
        />
      </div>
      
      {/* Middle Panel - Conversation (Main Area) */}
      <div className="flex-1 min-w-0">
        <ConversationPanel 
          userId={userId} 
          conversationId={selectedConversation}
          onTogglePreview={() => setIsPreviewVisible(!isPreviewVisible)}
          isPreviewVisible={isPreviewVisible}
        />
      </div>
      
      {/* Right Panel - Preview (Collapsible) */}
      {isPreviewVisible && (
        <div className="w-96 border-l border-gray-200 flex-shrink-0 transition-all duration-300 ease-in-out">
          <PreviewPanel onClose={() => setIsPreviewVisible(false)} />
        </div>
      )}
    </div>
  )
}

export default App
