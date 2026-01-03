/**
 * Project Alfred - Signup Nudge Component
 * Subtle, non-intrusive nudge to encourage account creation
 */

import React from 'react';
import { CloudIcon, XMarkIcon } from '@heroicons/react/24/outline';
import { useAuthStore } from '../store/authStore';

interface SignupNudgeProps {
  onSignupClick: () => void;
}

export const SignupNudge: React.FC<SignupNudgeProps> = ({ onSignupClick }) => {
  const { showSignupNudge, setShowSignupNudge } = useAuthStore();
  
  if (!showSignupNudge) return null;
  
  return (
    <div className="fixed bottom-4 right-4 max-w-sm bg-white border-2 border-[#2D5F4C] rounded-lg shadow-lg p-4 animate-slide-up">
      <button
        onClick={() => setShowSignupNudge(false)}
        className="absolute top-2 right-2 text-gray-400 hover:text-gray-600"
      >
        <XMarkIcon className="w-5 h-5" />
      </button>
      
      <div className="flex items-start space-x-3">
        <div className="flex-shrink-0">
          <CloudIcon className="w-8 h-8 text-[#2D5F4C]" />
        </div>
        
        <div className="flex-1">
          <h3 className="text-sm font-semibold text-gray-900 mb-1">
            Sync your conversations
          </h3>
          <p className="text-xs text-gray-600 mb-3">
            Create an account to access your conversations from any device and unlock personalized features.
          </p>
          
          <button
            onClick={() => {
              setShowSignupNudge(false);
              onSignupClick();
            }}
            className="w-full bg-gradient-to-r from-[#2D5F4C] to-[#1A3A2E] text-white text-sm font-medium py-2 px-4 rounded-md hover:opacity-90 transition-opacity"
          >
            Create Account
          </button>
        </div>
      </div>
    </div>
  );
};
