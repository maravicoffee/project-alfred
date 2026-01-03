import { useState } from 'react'

export default function FeatureCarousel() {
  const [currentSlide, setCurrentSlide] = useState(0)

  const features = [
    {
      title: 'Intelligent Task Management',
      description: 'Alfred understands your goals and breaks them down into actionable steps automatically.',
      image: '🎯'
    },
    {
      title: 'Seamless Integration',
      description: 'Connect with your favorite tools and services for a unified workflow experience.',
      image: '🔗'
    },
    {
      title: 'AI-Powered Insights',
      description: 'Get intelligent suggestions and insights based on your work patterns and preferences.',
      image: '💡'
    }
  ]

  return (
    <div className="w-full max-w-4xl mx-auto mt-12">
      {/* Feature Card */}
      <div className="bg-forest-darkest/30 border border-forest-light/10 rounded-2xl p-8 mb-4">
        <div className="flex items-center space-x-8">
          {/* Text Content */}
          <div className="flex-1">
            <h3 className="text-xl font-medium text-forest-light mb-3">
              {features[currentSlide].title}
            </h3>
            <p className="text-forest-light/70 leading-relaxed">
              {features[currentSlide].description}
            </p>
          </div>

          {/* Visual */}
          <div className="flex-shrink-0 w-32 h-32 bg-forest-accent/20 rounded-xl flex items-center justify-center text-6xl">
            {features[currentSlide].image}
          </div>
        </div>
      </div>

      {/* Pagination Dots */}
      <div className="flex items-center justify-center space-x-2">
        {features.map((_, index) => (
          <button
            key={index}
            onClick={() => setCurrentSlide(index)}
            className={`w-2 h-2 rounded-full transition-all ${
              index === currentSlide 
                ? 'bg-forest-accent w-6' 
                : 'bg-forest-light/30 hover:bg-forest-light/50'
            }`}
            aria-label={`Go to slide ${index + 1}`}
          />
        ))}
      </div>
    </div>
  )
}
