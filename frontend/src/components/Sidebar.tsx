import { FolderIcon, PencilIcon, MagnifyingGlassIcon, BookOpenIcon, ListBulletIcon, QuestionMarkCircleIcon, DevicePhoneMobileIcon, UserCircleIcon } from '@heroicons/react/24/outline'

export default function Sidebar() {
  const icons = [
    { Icon: FolderIcon, label: 'Folder' },
    { Icon: PencilIcon, label: 'Edit', active: true },
    { Icon: MagnifyingGlassIcon, label: 'Search' },
    { Icon: BookOpenIcon, label: 'Library' },
    { Icon: FolderIcon, label: 'Folder 2' },
    { Icon: ListBulletIcon, label: 'List' },
    { Icon: QuestionMarkCircleIcon, label: 'Help' },
    { Icon: DevicePhoneMobileIcon, label: 'Mobile' },
  ]

  return (
    <div className="w-16 bg-forest-darkest flex flex-col items-center py-5 space-y-6">
      {/* Icons */}
      <div className="flex-1 flex flex-col items-center space-y-4">
        {icons.map(({ Icon, label, active }, index) => (
          <button
            key={index}
            className={`p-2 rounded-lg transition-colors relative ${
              active
                ? 'text-emerald bg-forest-darkest/50'
                : 'text-forest-light/60 hover:text-forest-light hover:bg-forest-darkest/50'
            }`}
            aria-label={label}
          >
            {active && (
              <div className="absolute left-0 top-1/2 -translate-y-1/2 w-1 h-8 bg-emerald rounded-r" />
            )}
            <Icon className="w-5 h-5" />
          </button>
        ))}
      </div>

      {/* User Avatar */}
      <div className="mt-auto">
        <button className="p-2 rounded-full bg-forest-dark" aria-label="User profile">
          <UserCircleIcon className="w-8 h-8 text-forest-light" />
        </button>
      </div>
    </div>
  )
}
