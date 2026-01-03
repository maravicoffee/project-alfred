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
  onNewChat: () => void
}

export default function ConversationList({ userId, onSelectConversation, onNewChat }: ConversationListProps) {
  const [conversations, setConversations] = useState<Conversation[]>([])
  const [selectedId, setSelectedId] = useState<string | null>(null)

  useEffect(() => {
    // Load conversations from localStorage
    const stored = localStorage.getItem(`alfred_conversations_${userId}`)
    if (stored) {
      try {
        setConversations(JSON.parse(stored))
      } catch (error) {
        console.error('Failed to load conversations:', error)
      }
    }
  }, [userId])

  // Save conversations to localStorage whenever they change
  useEffect(() => {
    if (conversations.length > 0) {
      localStorage.setItem(`alfred_conversations_${userId}`, JSON.stringify(conversations))
    }
  }, [conversations, userId])

  const createNewConversation = () => {
    const newConvo: Conversation = {
      id: crypto.randomUUID(),
      title: 'New Chat',
      created_at: new Date().toISOString(),
      updated_at: new Date().toISOString()
    }
    
    setConversations([newConvo, ...conversations])
    setSelectedId(newConvo.id)
    onSelectConversation(newConvo.id)
    onNewChat()
  }

  return (
    <div className="flex flex-col h-full bg-forest-dark">
      {/* Header */}
      <div className="p-4 border-b border-forest-darkest/50">
        <h2 className="text-forest-light font-semibold text-lg mb-3">Alfred 1.0</h2>
        <button
          onClick={createNewConversation}
          className="w-full flex items-center justify-center space-x-2 px-4 py-2.5 bg-emerald hover:bg-emerald/90 text-white rounded-lg transition-colors font-medium"
        >
          <PlusIcon className="w-5 h-5" />
          <span>New Chat</span>
        </button>
      </div>

      {/* Conversations list */}
      <div className="flex-1 overflow-y-auto p-2">
        {conversations.length === 0 ? (
          <div className="p-6 text-center">
            <div className="bg-forest-darkest/30 rounded-lg p-8">
              <ChatBubbleLeftIcon className="w-16 h-16 mx-auto mb-3 text-forest-light/30" />
              <p className="text-forest-light/70 font-medium mb-1">No conversations yet</p>
              <p className="text-forest-light/50 text-sm">Start a new chat to begin</p>
            </div>
          </div>
        ) : (
          <div className="space-y-1">
            {conversations.map((convo) => (
              <button
                key={convo.id}
                onClick={() => {
                  setSelectedId(convo.id)
                  onSelectConversation(convo.id)
                }}
                className={`w-full text-left px-3 py-3 rounded-lg transition-all ${
                  selectedId === convo.id
                    ? 'bg-emerald/20 border-l-2 border-emerald'
                    : 'hover:bg-forest-darkest/30'
                }`}
              >
                <div className="flex items-start space-x-3">
                  <ChatBubbleLeftIcon className={`w-5 h-5 flex-shrink-0 mt-0.5 ${
                    selectedId === convo.id ? 'text-emerald' : 'text-forest-light/40'
                  }`} />
                  <div className="flex-1 min-w-0">
                    <p className={`text-sm font-medium truncate ${
                      selectedId === convo.id ? 'text-emerald' : 'text-forest-light'
                    }`}>
                      {convo.title}
                    </p>
                    <p className="text-xs text-forest-light/50 mt-0.5">
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
