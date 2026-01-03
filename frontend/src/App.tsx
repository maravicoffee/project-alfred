import { useState } from 'react'
import Sidebar from './components/Sidebar'
import ConversationPanel from './components/ConversationPanel'
import ConversationList from './components/ConversationList'
import PreviewPanel from './components/PreviewPanel'
import './App.css'

function App() {
  const [selectedConversation, setSelectedConversation] = useState<string | null>(null)
  const [isSidebarCollapsed, setIsSidebarCollapsed] = useState(false)
  const [isPreviewVisible, setIsPreviewVisible] = useState(false)
  const [currentView, setCurrentView] = useState<'list' | 'chat'>('chat')
  const [userId] = useState<string>(() => {
    // Generate or retrieve user ID
    const stored = localStorage.getItem('alfred_user_id')
    if (stored) return stored
    const newId = crypto.randomUUID()
    localStorage.setItem('alfred_user_id', newId)
    return newId
  })

  const handleSelectConversation = (conversationId: string) => {
    setSelectedConversation(conversationId)
    setCurrentView('chat')
  }

  const handleNewChat = () => {
    setSelectedConversation(null)
    setCurrentView('chat')
  }

  const handleShowConversations = () => {
    setCurrentView('list')
  }

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
          onNewChat={handleNewChat}
          onShowConversations={handleShowConversations}
        />
      </div>
      
      {/* Main Content Area - Single panel that switches between views */}
      <div className="flex-1 max-w-4xl min-w-0 h-full overflow-hidden">
        {currentView === 'list' ? (
          <ConversationList 
            userId={userId}
            onSelectConversation={handleSelectConversation}
            onNewChat={handleNewChat}
          />
        ) : (
          <ConversationPanel 
            userId={userId} 
            conversationId={selectedConversation}
            onTogglePreview={() => setIsPreviewVisible(!isPreviewVisible)}
            isPreviewVisible={isPreviewVisible}
          />
        )}
      </div>
      
      {/* Right Panel - Preview (Toggleable) */}
      {isPreviewVisible && (
        <div className="flex-1 min-w-[300px] max-w-md border-l border-gray-200 h-full overflow-hidden transition-all duration-300 ease-in-out">
          <PreviewPanel onClose={() => setIsPreviewVisible(false)} />
        </div>
      )}
    </div>
  )
}

export default App
