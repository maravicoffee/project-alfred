import { useState } from 'react'
import Sidebar from './components/Sidebar'
import ConversationPanel from './components/ConversationPanel'
import ConversationList from './components/ConversationList'
import PreviewPanel from './components/PreviewPanel'
import './App.css'

function App() {
  const [selectedConversation, setSelectedConversation] = useState<string | null>(null)
  const [userId] = useState<string>(() => {
    // Generate or retrieve user ID
    const stored = localStorage.getItem('alfred_user_id')
    if (stored) return stored
    const newId = crypto.randomUUID()
    localStorage.setItem('alfred_user_id', newId)
    return newId
  })

  return (
    <div className="flex h-screen bg-forest-light">
      {/* Left Sidebar - Collapsed */}
      <Sidebar />
      
      {/* Conversation List */}
      <div className="w-64 bg-forest-dark border-r border-forest-darkest">
        <ConversationList 
          userId={userId}
          onSelectConversation={setSelectedConversation}
        />
      </div>
      
      {/* Middle Panel - Conversation */}
      <ConversationPanel userId={userId} conversationId={selectedConversation} />
      
      {/* Right Panel - Preview */}
      <PreviewPanel />
    </div>
  )
}

export default App
