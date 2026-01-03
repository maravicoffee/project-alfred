import { 
  XMarkIcon, 
  EyeIcon, 
  UserGroupIcon,
  LinkIcon,
  DocumentDuplicateIcon,
  CodeBracketIcon,
  ClockIcon,
  ListBulletIcon,
  LockClosedIcon,
  Cog6ToothIcon,
  ArrowDownTrayIcon,
  EllipsisHorizontalIcon,
  FolderIcon,
  ChevronDownIcon
} from '@heroicons/react/24/outline'

interface SharedHeaderProps {
  title: string
  isPreviewVisible: boolean
  onTogglePreview: () => void
  variant?: 'landing' | 'task'
}

export default function SharedHeader({ title, isPreviewVisible, onTogglePreview, variant = 'task' }: SharedHeaderProps) {
  return (
    <div className="w-full bg-forest-dark border-b border-forest-darkest/30 px-4 py-3">
      <div className="flex items-center justify-between">
        {/* Left Side - Title */}
        <div className="flex items-center space-x-2">
          <FolderIcon className="w-5 h-5 text-forest-light/60" />
          <span className="text-forest-light font-medium">{title}</span>
          <ChevronDownIcon className="w-4 h-4 text-forest-light/60" />
        </div>
        
        {/* Right Side - Buttons (changes based on variant and preview state) */}
        <div className="flex items-center space-x-2">
          {variant === 'landing' ? (
            /* Landing Page - Minimal Buttons */
            <>
              {/* Notifications */}
              <button className="p-2 text-forest-light/60 hover:text-forest-light hover:bg-forest-light/10 rounded-lg transition-colors relative">
                <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15 17h5l-1.405-1.405A2.032 2.032 0 0118 14.158V11a6.002 6.002 0 00-4-5.659V5a2 2 0 10-4 0v.341C7.67 6.165 6 8.388 6 11v3.159c0 .538-.214 1.055-.595 1.436L4 17h5m6 0v1a3 3 0 11-6 0v-1m6 0H9" />
                </svg>
              </button>

              {/* Credits */}
              <button className="flex items-center space-x-1 px-3 py-1.5 text-sm text-forest-light/80 hover:text-forest-light hover:bg-forest-light/10 rounded-lg transition-colors">
                <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M13 10V3L4 14h7v7l9-11h-7z" />
                </svg>
                <span>86,301</span>
              </button>
            </>
          ) : !isPreviewVisible ? (
            /* Preview Closed - Minimal Button Set */
            <>
              {/* Collaborate */}
              <button className="flex items-center space-x-1 px-2 py-1.5 text-sm text-forest-light/80 hover:text-forest-light hover:bg-forest-light/10 rounded-lg transition-colors">
                <UserGroupIcon className="w-4 h-4" />
                <span className="text-xs">2</span>
              </button>

              {/* Share */}
              <button className="px-3 py-1.5 text-sm text-forest-light/80 hover:text-forest-light hover:bg-forest-light/10 rounded-lg transition-colors">
                Share
              </button>

              {/* Export/Download */}
              <button className="p-1.5 text-forest-light/60 hover:text-forest-light hover:bg-forest-light/10 rounded-lg transition-colors">
                <ArrowDownTrayIcon className="w-5 h-5" />
              </button>

              {/* Menu */}
              <button className="p-1.5 text-forest-light/60 hover:text-forest-light hover:bg-forest-light/10 rounded-lg transition-colors">
                <EllipsisHorizontalIcon className="w-5 h-5" />
              </button>
            </>
          ) : (
            /* Preview Open - Full Button Set */
            <>
              {/* Collaborate */}
              <button className="p-1.5 text-forest-light/60 hover:text-forest-light hover:bg-forest-light/10 rounded-lg transition-colors">
                <UserGroupIcon className="w-4 h-4" />
              </button>

              {/* Link */}
              <button className="p-1.5 text-forest-light/60 hover:text-forest-light hover:bg-forest-light/10 rounded-lg transition-colors">
                <LinkIcon className="w-4 h-4" />
              </button>

              {/* Copy */}
              <button className="p-1.5 text-forest-light/60 hover:text-forest-light hover:bg-forest-light/10 rounded-lg transition-colors">
                <DocumentDuplicateIcon className="w-4 h-4" />
              </button>

              {/* Menu */}
              <button className="p-1.5 text-forest-light/60 hover:text-forest-light hover:bg-forest-light/10 rounded-lg transition-colors">
                <EllipsisHorizontalIcon className="w-4 h-4" />
              </button>

              {/* Divider */}
              <div className="w-px h-6 bg-forest-light/20"></div>

              {/* Preview Button (Highlighted/Active) */}
              <button
                onClick={onTogglePreview}
                className="flex items-center space-x-2 px-3 py-1.5 text-sm bg-forest-accent text-white rounded-lg hover:bg-forest-accent/90 transition-colors"
              >
                <EyeIcon className="w-4 h-4" />
                <span>Preview</span>
              </button>

              {/* Code */}
              <button className="p-1.5 text-forest-light/60 hover:text-forest-light hover:bg-forest-light/10 rounded-lg transition-colors">
                <CodeBracketIcon className="w-4 h-4" />
              </button>

              {/* Clock */}
              <button className="p-1.5 text-forest-light/60 hover:text-forest-light hover:bg-forest-light/10 rounded-lg transition-colors">
                <ClockIcon className="w-4 h-4" />
              </button>

              {/* List */}
              <button className="p-1.5 text-forest-light/60 hover:text-forest-light hover:bg-forest-light/10 rounded-lg transition-colors">
                <ListBulletIcon className="w-4 h-4" />
              </button>

              {/* Lock */}
              <button className="p-1.5 text-forest-light/60 hover:text-forest-light hover:bg-forest-light/10 rounded-lg transition-colors">
                <LockClosedIcon className="w-4 h-4" />
              </button>

              {/* Settings */}
              <button className="p-1.5 text-forest-light/60 hover:text-forest-light hover:bg-forest-light/10 rounded-lg transition-colors">
                <Cog6ToothIcon className="w-4 h-4" />
              </button>

              {/* Menu */}
              <button className="p-1.5 text-forest-light/60 hover:text-forest-light hover:bg-forest-light/10 rounded-lg transition-colors">
                <EllipsisHorizontalIcon className="w-4 h-4" />
              </button>

              {/* GitHub Icon (placeholder - using code icon) */}
              <button className="p-1.5 text-forest-light/60 hover:text-forest-light hover:bg-forest-light/10 rounded-lg transition-colors">
                <svg className="w-4 h-4" fill="currentColor" viewBox="0 0 24 24">
                  <path d="M12 0c-6.626 0-12 5.373-12 12 0 5.302 3.438 9.8 8.207 11.387.599.111.793-.261.793-.577v-2.234c-3.338.726-4.033-1.416-4.033-1.416-.546-1.387-1.333-1.756-1.333-1.756-1.089-.745.083-.729.083-.729 1.205.084 1.839 1.237 1.839 1.237 1.07 1.834 2.807 1.304 3.492.997.107-.775.418-1.305.762-1.604-2.665-.305-5.467-1.334-5.467-5.931 0-1.311.469-2.381 1.236-3.221-.124-.303-.535-1.524.117-3.176 0 0 1.008-.322 3.301 1.23.957-.266 1.983-.399 3.003-.404 1.02.005 2.047.138 3.006.404 2.291-1.552 3.297-1.23 3.297-1.23.653 1.653.242 2.874.118 3.176.77.84 1.235 1.911 1.235 3.221 0 4.609-2.807 5.624-5.479 5.921.43.372.823 1.102.823 2.222v3.293c0 .319.192.694.801.576 4.765-1.589 8.199-6.086 8.199-11.386 0-6.627-5.373-12-12-12z"/>
                </svg>
              </button>

              {/* Divider */}
              <div className="w-px h-6 bg-forest-light/20"></div>

              {/* Share */}
              <button className="px-3 py-1.5 text-sm text-forest-light/80 hover:text-forest-light hover:bg-forest-light/10 rounded-lg transition-colors">
                Share
              </button>

              {/* Published */}
              <button className="px-3 py-1.5 text-sm bg-forest-accent text-white rounded-lg hover:bg-forest-accent/90 transition-colors">
                Published
              </button>

              {/* Close Preview X */}
              <button
                onClick={onTogglePreview}
                className="p-1.5 text-forest-light/60 hover:text-forest-light hover:bg-forest-light/10 rounded-lg transition-colors"
                aria-label="Close preview"
              >
                <XMarkIcon className="w-5 h-5" />
              </button>
            </>
          )}

          {/* User Profile Icon (always visible) */}
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
