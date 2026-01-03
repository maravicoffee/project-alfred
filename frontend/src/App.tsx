import { useState } from 'react'
import Sidebar from './components/Sidebar'
import ConversationPanel from './components/ConversationPanel'
import PreviewPanel from './components/PreviewPanel'
import './App.css'

function App() {
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
      
      {/* Middle Panel - Conversation */}
      <ConversationPanel userId={userId} />
      
      {/* Right Panel - Preview */}
      <PreviewPanel />
    </div>
  )
}

export default App
