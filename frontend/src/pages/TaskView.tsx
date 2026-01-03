import { useState } from 'react'
import ConversationPanel from '../components/ConversationPanel'
import PreviewPanel from '../components/PreviewPanel'

export default function TaskView() {
  const [isPreviewVisible, setIsPreviewVisible] = useState(false)
  const [userId] = useState<string>(() => {
    const stored = localStorage.getItem('alfred_user_id')
    if (stored) return stored
    const newId = crypto.randomUUID()
    localStorage.setItem('alfred_user_id', newId)
    return newId
  })

  return (
    <div className="flex-1 flex overflow-hidden">
      {/* Main Content Panel */}
      <div className="flex-1 min-w-[400px] h-full overflow-hidden">
        <ConversationPanel 
          userId={userId} 
          conversationId={null}
          onTogglePreview={() => setIsPreviewVisible(!isPreviewVisible)}
          isPreviewVisible={isPreviewVisible}
        />
      </div>
      
      {/* Preview Panel (only when visible) */}
      {isPreviewVisible && (
        <div className="flex-1 min-w-[500px] border-l border-gray-200 h-full overflow-hidden transition-all duration-300 ease-in-out">
          <PreviewPanel />
        </div>
      )}
    </div>
  )
}
