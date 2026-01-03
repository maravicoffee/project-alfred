/**
 * Project Alfred - Welcome Message Component
 * Displays a warm welcome message for new users
 */

import React from 'react';
import { SparklesIcon } from '@heroicons/react/24/outline';

interface WelcomeMessageProps {
  userName?: string;
  onDismiss: () => void;
}

export const WelcomeMessage: React.FC<WelcomeMessageProps> = ({ userName, onDismiss }) => {
  return (
    <div className="flex items-start space-x-3 p-4 bg-gradient-to-r from-[#E8F3ED] to-white border-l-4 border-[#2D5F4C] rounded-r-lg shadow-sm animate-fade-in">
      <div className="flex-shrink-0">
        <SparklesIcon className="w-6 h-6 text-[#2D5F4C]" />
      </div>
      
      <div className="flex-1">
        <h3 className="text-lg font-semibold text-gray-900 mb-2">
          Welcome{userName ? `, ${userName}` : ''}! 🎉
        </h3>
        
        <p className="text-sm text-gray-700 mb-3">
          Your conversations are now synced across all your devices. I'll also start learning your preferences to give you a more personalized experience.
        </p>
        
        <div className="bg-white p-3 rounded-md border border-gray-200 mb-3">
          <p className="text-xs font-medium text-gray-900 mb-2">Here's what I can help you with:</p>
          <ul className="text-xs text-gray-600 space-y-1">
            <li>• Search the web for current information</li>
            <li>• Execute Python code and analyze data</li>
            <li>• Manage files and documents</li>
            <li>• Learn your preferences and provide proactive suggestions</li>
          </ul>
        </div>
        
        <button
          onClick={onDismiss}
          className="text-sm text-[#2D5F4C] font-medium hover:underline"
        >
          Got it, let's get started →
        </button>
      </div>
    </div>
  );
};
