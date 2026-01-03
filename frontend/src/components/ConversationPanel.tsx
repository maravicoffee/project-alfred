import { useState, useRef, useEffect } from 'react'
import { PaperAirplaneIcon, PlusIcon } from '@heroicons/react/24/solid'
import aiService from '../services/ai'

interface Message {
  role: 'user' | 'assistant'
  content: string
  timestamp: string
}

interface ConversationPanelProps {
  userId: string
  conversationId: string | null
  onTogglePreview?: () => void
  isPreviewVisible?: boolean
}

export default function ConversationPanel({ onTogglePreview, isPreviewVisible }: ConversationPanelProps) {
  const [messages, setMessages] = useState<Message[]>([])
  const [input, setInput] = useState('')
  const [isLoading, setIsLoading] = useState(false)
  const messagesEndRef = useRef<HTMLDivElement>(null)

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' })
  }

  useEffect(() => {
    scrollToBottom()
  }, [messages])

  const sendMessage = async () => {
    if (!input.trim() || isLoading) return

    const userMessage: Message = {
      role: 'user',
      content: input,
      timestamp: new Date().toISOString()
    }

    setMessages(prev => [...prev, userMessage])
    setInput('')
    setIsLoading(true)

    try {
      // Use client-side AI service
      const response = await aiService.chat(input)

      const assistantMessage: Message = {
        role: 'assistant',
        content: response.response,
        timestamp: new Date().toISOString()
      }

      setMessages(prev => [...prev, assistantMessage])
    } catch (error) {
      console.error('Error sending message:', error)
      const errorMessage: Message = {
        role: 'assistant',
        content: 'Sorry, I encountered an error. Please try again.',
        timestamp: new Date().toISOString()
      }
      setMessages(prev => [...prev, errorMessage])
    } finally {
      setIsLoading(false)
    }
  }

  const handleKeyPress = (e: React.KeyboardEvent) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault()
      sendMessage()
    }
  }

  return (
    <div className="flex-1 bg-forest-dark flex flex-col h-full">
      {/* Header */}
      <div className="p-4 border-b border-forest-darkest/30">
        <div className="flex items-center justify-between">
          <h2 className="text-forest-light font-medium">Alfred 1.0</h2>
          <div className="flex items-center space-x-2">
            {!isPreviewVisible && (
              <button 
                onClick={onTogglePreview}
                className="px-3 py-1.5 text-sm text-forest-light/80 hover:text-forest-light border border-forest-light/30 rounded-lg transition-colors"
              >
                Show Preview
              </button>
            )}
            <button className="p-1 text-forest-light/60 hover:text-forest-light">
              <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z" />
              </svg>
            </button>
          </div>
        </div>
      </div>

      {/* Messages Area */}
      <div className="flex-1 overflow-y-auto p-4 space-y-4">
        {messages.length === 0 && (
          <div className="text-center text-forest-light/60 mt-8">
            <p className="text-lg">Start a conversation with Alfred</p>
            <p className="text-sm mt-2">Ask me anything!</p>
          </div>
        )}

        {messages.map((message, index) => (
          <div
            key={index}
            className={`flex ${message.role === 'user' ? 'justify-end' : 'justify-start'}`}
          >
            <div
              className={`max-w-[80%] rounded-lg p-3 ${
                message.role === 'user'
                  ? 'bg-emerald/20 text-forest-light'
                  : 'bg-forest-darkest/50 text-forest-light'
              }`}
            >
              <p className="text-sm whitespace-pre-wrap">{message.content}</p>
            </div>
          </div>
        ))}

        {isLoading && (
          <div className="flex justify-start">
            <div className="bg-forest-darkest/50 text-forest-light rounded-lg p-3">
              <div className="flex space-x-2">
                <div className="w-2 h-2 bg-forest-light/60 rounded-full animate-bounce" style={{ animationDelay: '0ms' }}></div>
                <div className="w-2 h-2 bg-forest-light/60 rounded-full animate-bounce" style={{ animationDelay: '150ms' }}></div>
                <div className="w-2 h-2 bg-forest-light/60 rounded-full animate-bounce" style={{ animationDelay: '300ms' }}></div>
              </div>
            </div>
          </div>
        )}

        <div ref={messagesEndRef} />
      </div>



      {/* Input Area */}
      <div className="p-4 border-t border-forest-darkest/30">
        <div className="flex items-center space-x-2 bg-forest-darkest/50 rounded-lg p-2">
          <button className="p-1 text-forest-light/60 hover:text-forest-light">
            <PlusIcon className="w-5 h-5" />
          </button>
          <input
            type="text"
            value={input}
            onChange={(e) => setInput(e.target.value)}
            onKeyPress={handleKeyPress}
            placeholder="Send message to Alfred"
            className="flex-1 bg-transparent text-forest-light placeholder-forest-light/40 outline-none text-sm"
            disabled={isLoading}
          />
          <button
            onClick={sendMessage}
            disabled={!input.trim() || isLoading}
            className="p-2 text-emerald hover:text-emerald/80 disabled:text-forest-light/30 disabled:cursor-not-allowed"
          >
            <PaperAirplaneIcon className="w-5 h-5" />
          </button>
        </div>
      </div>
    </div>
  )
}
