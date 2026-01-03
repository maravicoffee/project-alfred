import { EyeIcon, CodeBracketIcon, ClockIcon, ListBulletIcon, LockClosedIcon, Cog6ToothIcon, ShareIcon, XMarkIcon } from '@heroicons/react/24/outline'

interface PreviewPanelProps {
  onClose?: () => void
}

export default function PreviewPanel({ onClose }: PreviewPanelProps) {
  return (
    <div className="w-96 bg-forest-light flex flex-col h-full flex-shrink-0">
      {/* Header */}
      <div className="bg-white border-b border-gray-200 px-6 py-3">
        <div className="flex items-center justify-between">
          <div className="flex items-center space-x-4">
            <button className="flex items-center space-x-2 px-3 py-1.5 bg-emerald/10 text-emerald rounded-lg font-medium text-sm">
              <EyeIcon className="w-4 h-4" />
              <span>Preview</span>
            </button>
            <button className="p-1.5 text-gray-500 hover:text-gray-700">
              <CodeBracketIcon className="w-5 h-5" />
            </button>
            <button className="p-1.5 text-gray-500 hover:text-gray-700">
              <ClockIcon className="w-5 h-5" />
            </button>
            <button className="p-1.5 text-gray-500 hover:text-gray-700">
              <ListBulletIcon className="w-5 h-5" />
            </button>
            <button className="p-1.5 text-gray-500 hover:text-gray-700">
              <LockClosedIcon className="w-5 h-5" />
            </button>
            <button className="p-1.5 text-gray-500 hover:text-gray-700">
              <Cog6ToothIcon className="w-5 h-5" />
            </button>
          </div>
          <div className="flex items-center space-x-2">
            <button className="px-4 py-1.5 border border-gray-300 text-gray-700 rounded-lg font-medium text-sm hover:bg-gray-50">
              <ShareIcon className="w-4 h-4 inline mr-1" />
              Share
            </button>
            <button className="px-4 py-1.5 bg-forest-dark text-white rounded-lg font-medium text-sm hover:bg-forest-darkest">
              Published
            </button>
            {onClose && (
              <button 
                onClick={onClose}
                className="p-1.5 text-gray-500 hover:text-gray-700 hover:bg-gray-100 rounded-lg transition-colors"
                aria-label="Close preview"
              >
                <XMarkIcon className="w-5 h-5" />
              </button>
            )}
          </div>
        </div>
      </div>

      {/* Sub-header with navigation */}
      <div className="bg-white border-b border-gray-200 px-6 py-2">
        <div className="flex items-center justify-between">
          <div className="flex items-center space-x-4 text-sm">
            <button className="p-1 text-gray-500 hover:text-gray-700">
              <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9.75 17L9 20l-1 1h8l-1-1-.75-3M3 13h18M5 17h14a2 2 0 002-2V5a2 2 0 00-2-2H5a2 2 0 00-2 2v10a2 2 0 002 2z" />
              </svg>
            </button>
            <button className="p-1 text-gray-500 hover:text-gray-700">
              <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 18h.01M8 21h8a2 2 0 002-2V5a2 2 0 00-2-2H8a2 2 0 00-2 2v14a2 2 0 002 2z" />
              </svg>
            </button>
            <span className="text-gray-400">›</span>
            <span className="text-gray-600">Home › Dashboard › Project</span>
          </div>
          <div className="flex items-center space-x-2">
            <button className="p-1 text-gray-500 hover:text-gray-700">
              <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15" />
              </svg>
            </button>
            <button className="px-3 py-1 border border-gray-300 text-gray-700 rounded text-sm hover:bg-gray-50">
              Edit
            </button>
            <button className="p-1 text-gray-500 hover:text-gray-700">
              <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 8V4m0 0h4M4 4l5 5m11-1V4m0 0h-4m4 0l-5 5M4 16v4m0 0h4m-4 0l5-5m11 5l-5-5m5 5v-4m0 4h-4" />
              </svg>
            </button>
          </div>
        </div>
      </div>

      {/* Main Content Area */}
      <div className="flex-1 overflow-auto bg-gray-50 p-8">
        <div className="max-w-4xl mx-auto">
          {/* Welcome Card */}
          <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-8 mb-6">
            <div className="text-center">
              <div className="inline-flex items-center justify-center w-16 h-16 bg-forest-dark/10 rounded-full mb-4">
                <svg className="w-8 h-8 text-forest-dark" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M3 15a4 4 0 004 4h9a5 5 0 10-.1-9.999 5.002 5.002 0 10-9.78 2.096A4.001 4.001 0 003 15z" />
                </svg>
              </div>
              <h1 className="text-3xl font-bold text-gray-900 mb-2">Welcome to Alfred</h1>
              <p className="text-gray-600 text-lg">
                Bridging the gap between thought and action
              </p>
            </div>
          </div>

          {/* Info Cards */}
          <div className="grid grid-cols-3 gap-4">
            <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-6">
              <div className="flex items-center justify-between mb-3">
                <h3 className="font-semibold text-gray-900">Status</h3>
                <div className="w-2 h-2 bg-emerald rounded-full"></div>
              </div>
              <p className="text-sm text-gray-600">System operational</p>
            </div>

            <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-6">
              <div className="flex items-center justify-between mb-3">
                <h3 className="font-semibold text-gray-900">Core Engine</h3>
                <div className="w-2 h-2 bg-emerald rounded-full"></div>
              </div>
              <p className="text-sm text-gray-600">Ready to assist</p>
            </div>

            <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-6">
              <div className="flex items-center justify-between mb-3">
                <h3 className="font-semibold text-gray-900">Tools</h3>
                <span className="text-xs bg-forest-dark/10 text-forest-dark px-2 py-1 rounded-full">2</span>
              </div>
              <p className="text-sm text-gray-600">Available</p>
            </div>
          </div>

          {/* Getting Started */}
          <div className="mt-6 bg-white rounded-lg shadow-sm border border-gray-200 p-6">
            <h3 className="font-semibold text-gray-900 mb-4">Getting Started</h3>
            <ul className="space-y-3">
              <li className="flex items-start">
                <span className="flex-shrink-0 w-6 h-6 bg-emerald/10 text-emerald rounded-full flex items-center justify-center text-sm font-medium mr-3">1</span>
                <div>
                  <p className="text-gray-900 font-medium">Start a conversation</p>
                  <p className="text-sm text-gray-600">Use the conversation panel to interact with Alfred</p>
                </div>
              </li>
              <li className="flex items-start">
                <span className="flex-shrink-0 w-6 h-6 bg-emerald/10 text-emerald rounded-full flex items-center justify-center text-sm font-medium mr-3">2</span>
                <div>
                  <p className="text-gray-900 font-medium">Ask questions</p>
                  <p className="text-sm text-gray-600">Alfred will analyze, plan, and execute tasks for you</p>
                </div>
              </li>
              <li className="flex items-start">
                <span className="flex-shrink-0 w-6 h-6 bg-emerald/10 text-emerald rounded-full flex items-center justify-center text-sm font-medium mr-3">3</span>
                <div>
                  <p className="text-gray-900 font-medium">View results</p>
                  <p className="text-sm text-gray-600">See the cognitive loop in action with detailed metadata</p>
                </div>
              </li>
            </ul>
          </div>
        </div>
      </div>
    </div>
  )
}
