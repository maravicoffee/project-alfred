import QuickActions from '../components/QuickActions'
import FeatureCarousel from '../components/FeatureCarousel'

interface LandingPageProps {
  onStartTask: () => void
}

// Landing Page Component - Updated
export default function LandingPage({ }: LandingPageProps) {
  return (
    <div className="flex-1 bg-forest-dark flex flex-col h-full">
      {/* Main Content */}
      <div className="flex-1 flex flex-col items-center justify-center px-8">
        {/* Hero Section */}
        <div className="w-full max-w-4xl">
          <h1 className="text-4xl md:text-5xl text-forest-light text-center mb-8 font-light">
            What can I do for you?
          </h1>
          
          {/* Large Input Box */}
          <div className="bg-forest-darkest/50 border border-forest-light/20 rounded-2xl p-4 mb-8">
            <div className="flex items-center space-x-3">
              {/* Plus Button */}
              <button className="p-2 text-forest-light/60 hover:text-forest-light hover:bg-forest-light/10 rounded-lg transition-colors">
                <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 4v16m8-8H4" />
                </svg>
              </button>

              {/* Input */}
              <input
                type="text"
                placeholder="Assign a task or ask anything"
                className="flex-1 bg-transparent text-forest-light placeholder-forest-light/40 outline-none text-lg"
              />

              {/* Tool Icons */}
              <div className="flex items-center space-x-2">
                <button className="p-1.5 text-forest-light/60 hover:text-forest-light transition-colors">
                  <svg className="w-5 h-5" fill="currentColor" viewBox="0 0 24 24">
                    <path d="M12 0c-6.626 0-12 5.373-12 12 0 5.302 3.438 9.8 8.207 11.387.599.111.793-.261.793-.577v-2.234c-3.338.726-4.033-1.416-4.033-1.416-.546-1.387-1.333-1.756-1.333-1.756-1.089-.745.083-.729.083-.729 1.205.084 1.839 1.237 1.839 1.237 1.07 1.834 2.807 1.304 3.492.997.107-.775.418-1.305.762-1.604-2.665-.305-5.467-1.334-5.467-5.931 0-1.311.469-2.381 1.236-3.221-.124-.303-.535-1.524.117-3.176 0 0 1.008-.322 3.301 1.23.957-.266 1.983-.399 3.003-.404 1.02.005 2.047.138 3.006.404 2.291-1.552 3.297-1.23 3.297-1.23.653 1.653.242 2.874.118 3.176.77.84 1.235 1.911 1.235 3.221 0 4.609-2.807 5.624-5.479 5.921.43.372.823 1.102.823 2.222v3.293c0 .319.192.694.801.576 4.765-1.589 8.199-6.086 8.199-11.386 0-6.627-5.373-12-12-12z"/>
                  </svg>
                </button>
                <span className="text-forest-light/40 text-sm">+2</span>
              </div>

              {/* Voice Input */}
              <button className="p-2 text-forest-light/60 hover:text-forest-light hover:bg-forest-light/10 rounded-lg transition-colors">
                <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 11a7 7 0 01-7 7m0 0a7 7 0 01-7-7m7 7v4m0 0H8m4 0h4m-4-8a3 3 0 01-3-3V5a3 3 0 116 0v6a3 3 0 01-3 3z" />
                </svg>
              </button>

              {/* Send Button */}
              <button className="p-2 bg-forest-accent text-white rounded-lg hover:bg-forest-accent/90 transition-colors">
                <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 19l9 2-9-18-9 18 9-2zm0 0v-8" />
                </svg>
              </button>
            </div>
          </div>

          {/* Quick Actions */}
          <QuickActions />
        </div>

        {/* Feature Carousel */}
        <FeatureCarousel />
      </div>
    </div>
  )
}
