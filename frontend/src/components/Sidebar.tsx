import { FolderIcon, PencilIcon, MagnifyingGlassIcon, BookOpenIcon, ListBulletIcon, QuestionMarkCircleIcon, DevicePhoneMobileIcon, UserCircleIcon, ChevronRightIcon, ChevronLeftIcon } from '@heroicons/react/24/outline'

interface SidebarProps {
  isCollapsed: boolean
  onToggle: () => void
}

export default function Sidebar({ isCollapsed, onToggle }: SidebarProps) {
  const icons = [
    { Icon: FolderIcon, label: 'Projects' },
    { Icon: PencilIcon, label: 'Conversations', active: true },
    { Icon: MagnifyingGlassIcon, label: 'Search' },
    { Icon: BookOpenIcon, label: 'Knowledge' },
    { Icon: FolderIcon, label: 'Files' },
    { Icon: ListBulletIcon, label: 'Tasks' },
    { Icon: QuestionMarkCircleIcon, label: 'Help' },
    { Icon: DevicePhoneMobileIcon, label: 'Mobile' },
  ]

  return (
    <div className="h-full bg-forest-darkest flex flex-col py-5 relative">
      {/* Toggle Button */}
      <button
        onClick={onToggle}
        className="absolute -right-3 top-6 z-10 bg-forest-darkest border border-forest-dark rounded-full p-1 text-forest-light/60 hover:text-forest-light hover:bg-forest-dark transition-colors"
        aria-label={isCollapsed ? 'Open sidebar' : 'Close sidebar'}
      >
        {isCollapsed ? (
          <ChevronRightIcon className="w-4 h-4" />
        ) : (
          <ChevronLeftIcon className="w-4 h-4" />
        )}
      </button>

      {/* Icons */}
      <div className="flex-1 flex flex-col space-y-2 px-3">
        {icons.map(({ Icon, label, active }, index) => (
          <button
            key={index}
            className={`flex items-center gap-3 p-2 rounded-lg transition-all duration-200 relative group ${
              active
                ? 'text-emerald bg-forest-darkest/50'
                : 'text-forest-light/60 hover:text-forest-light hover:bg-forest-darkest/50'
            }`}
            aria-label={label}
            title={isCollapsed ? label : undefined}
          >
            {active && (
              <div className="absolute left-0 top-1/2 -translate-y-1/2 w-1 h-8 bg-emerald rounded-r" />
            )}
            <Icon className="w-5 h-5 flex-shrink-0" />
            {!isCollapsed && (
              <span className="text-sm font-medium whitespace-nowrap overflow-hidden transition-opacity duration-200">
                {label}
              </span>
            )}
          </button>
        ))}
      </div>

      {/* User Avatar */}
      <div className="mt-auto px-3">
        <button 
          className="flex items-center gap-3 w-full p-2 rounded-lg bg-forest-dark hover:bg-forest-dark/80 transition-colors" 
          aria-label="User profile"
          title={isCollapsed ? 'User profile' : undefined}
        >
          <UserCircleIcon className="w-8 h-8 text-forest-light flex-shrink-0" />
          {!isCollapsed && (
            <div className="flex flex-col items-start overflow-hidden">
              <span className="text-sm font-medium text-forest-light whitespace-nowrap">User</span>
              <span className="text-xs text-forest-light/60 whitespace-nowrap">View profile</span>
            </div>
          )}
        </button>
      </div>
    </div>
  )
}
