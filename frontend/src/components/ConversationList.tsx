import { useState, useEffect } from 'react'
import { ChatBubbleLeftIcon, PlusIcon } from '@heroicons/react/24/outline'

interface Conversation {
  id: string
  title: string
  created_at: string
  updated_at: string
}

interface ConversationListProps {
  userId: string
  onSelectConversation: (conversationId: string) => void
}

export default function ConversationList({ userId, onSelectConversation }: ConversationListProps) {
  const [conversations, setConversations] = useState<Conversation[]>([])
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    loadConversations()
  }, [userId])

  const loadConversations = async () => {
    try {
      const response = await fetch(`http://localhost:8000/api/conversations/${userId}`)
      if (response.ok) {
        const data = await response.json()
        setConversations(data)
      }
    } catch (error) {
      console.error('Failed to load conversations:', error)
    } finally {
      setLoading(false)
    }
  }

  const createNewConversation = async () => {
    try {
      const response = await fetch('http://localhost:8000/api/conversations/', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ user_id: userId, title: 'New Chat' })
      })
      
      if (response.ok) {
        const newConvo = await response.json()
        setConversations([newConvo, ...conversations])
        onSelectConversation(newConvo.id)
      }
    } catch (error) {
      console.error('Failed to create conversation:', error)
    }
  }

  if (loading) {
    return (
      <div className="p-4 text-center text-gray-400">
        Loading conversations...
      </div>
    )
  }

  return (
    <div className="flex flex-col h-full">
      {/* New conversation button */}
      <div className="p-3 border-b border-forest-dark/20">
        <button
          onClick={createNewConversation}
          className="w-full flex items-center justify-center space-x-2 px-4 py-2 bg-emerald/10 hover:bg-emerald/20 text-emerald rounded-lg transition-colors"
        >
          <PlusIcon className="w-5 h-5" />
          <span className="font-medium">New Chat</span>
        </button>
      </div>

      {/* Conversations list */}
      <div className="flex-1 overflow-y-auto">
        {conversations.length === 0 ? (
          <div className="p-4 text-center text-gray-400">
            <ChatBubbleLeftIcon className="w-12 h-12 mx-auto mb-2 opacity-50" />
            <p>No conversations yet</p>
            <p className="text-sm">Start a new chat to begin</p>
          </div>
        ) : (
          <div className="space-y-1 p-2">
            {conversations.map((convo) => (
              <button
                key={convo.id}
                onClick={() => onSelectConversation(convo.id)}
                className="w-full text-left px-3 py-2 rounded-lg hover:bg-forest-dark/10 transition-colors group"
              >
                <div className="flex items-start space-x-2">
                  <ChatBubbleLeftIcon className="w-5 h-5 text-gray-400 flex-shrink-0 mt-0.5" />
                  <div className="flex-1 min-w-0">
                    <p className="text-sm font-medium text-gray-200 truncate group-hover:text-emerald">
                      {convo.title}
                    </p>
                    <p className="text-xs text-gray-400">
                      {new Date(convo.updated_at).toLocaleDateString()}
                    </p>
                  </div>
                </div>
              </button>
            ))}
          </div>
        )}
      </div>
    </div>
  )
}
