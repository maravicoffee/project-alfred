import { XMarkIcon, EyeIcon } from '@heroicons/react/24/outline'

interface SharedHeaderProps {
  title: string
  isPreviewVisible: boolean
  onTogglePreview: () => void
}

export default function SharedHeader({ title, isPreviewVisible, onTogglePreview }: SharedHeaderProps) {
  return (
    <div className="w-full bg-forest-dark border-b border-forest-darkest/30 p-4">
      <div className="flex items-center justify-between">
        <h2 className="text-forest-light font-medium">{title}</h2>
        
        <div className="flex items-center space-x-3">
          {/* Preview Toggle Button */}
          <button
            onClick={onTogglePreview}
            className={`flex items-center space-x-2 px-3 py-1.5 text-sm rounded-lg transition-colors ${
              isPreviewVisible
                ? 'bg-forest-accent text-white'
                : 'text-forest-light/80 hover:text-forest-light border border-forest-light/30'
            }`}
          >
            <EyeIcon className="w-4 h-4" />
            <span>Preview</span>
          </button>

          {/* Share Button */}
          <button className="px-3 py-1.5 text-sm text-forest-light/80 hover:text-forest-light border border-forest-light/30 rounded-lg transition-colors">
            Share
          </button>

          {/* Published Button */}
          <button className="px-3 py-1.5 text-sm bg-forest-accent text-white rounded-lg hover:bg-forest-accent/90 transition-colors">
            Published
          </button>

          {/* Close Preview X (only when preview is open) */}
          {isPreviewVisible && (
            <button
              onClick={onTogglePreview}
              className="p-1.5 text-forest-light/60 hover:text-forest-light hover:bg-forest-light/10 rounded-lg transition-colors"
              aria-label="Close preview"
            >
              <XMarkIcon className="w-5 h-5" />
            </button>
          )}

          {/* User Profile Icon */}
          <button className="p-1 text-forest-light/60 hover:text-forest-light">
            <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z" />
            </svg>
          </button>
        </div>
      </div>
    </div>
  )
}
