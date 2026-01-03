export default function PreviewPanel() {
  return (
    <div className="w-full bg-forest-light flex flex-col h-full">
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
