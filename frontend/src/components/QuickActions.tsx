import { 
  PresentationChartBarIcon,
  GlobeAltIcon,
  DevicePhoneMobileIcon,
  PaintBrushIcon,
  EllipsisHorizontalIcon
} from '@heroicons/react/24/outline'

export default function QuickActions() {
  const actions = [
    {
      icon: PresentationChartBarIcon,
      label: 'Create slides',
      onClick: () => console.log('Create slides')
    },
    {
      icon: GlobeAltIcon,
      label: 'Build website',
      onClick: () => console.log('Build website')
    },
    {
      icon: DevicePhoneMobileIcon,
      label: 'Develop apps',
      onClick: () => console.log('Develop apps')
    },
    {
      icon: PaintBrushIcon,
      label: 'Design',
      onClick: () => console.log('Design')
    },
    {
      icon: EllipsisHorizontalIcon,
      label: 'More',
      onClick: () => console.log('More')
    }
  ]

  return (
    <div className="flex items-center justify-center space-x-3 mb-8">
      {actions.map((action, index) => (
        <button
          key={index}
          onClick={action.onClick}
          className="flex items-center space-x-2 px-4 py-2.5 bg-forest-darkest/50 border border-forest-light/20 text-forest-light/80 hover:text-forest-light hover:border-forest-light/40 rounded-xl transition-colors"
        >
          <action.icon className="w-5 h-5" />
          <span className="text-sm">{action.label}</span>
        </button>
      ))}
    </div>
  )
}
