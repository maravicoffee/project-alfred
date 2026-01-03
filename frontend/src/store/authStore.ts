/**
 * Project Alfred - Authentication Store
 * Manages user authentication state using Zustand
 */

import { create } from 'zustand';
import { persist } from 'zustand/middleware';

export interface User {
  id: string;
  email: string;
  name?: string;
  avatar?: string;
}

interface AuthState {
  user: User | null;
  isAnonymous: boolean;
  isAuthenticated: boolean;
  interactionCount: number;
  showSignupNudge: boolean;
  
  // Actions
  setUser: (user: User | null) => void;
  setAnonymous: (isAnonymous: boolean) => void;
  incrementInteraction: () => void;
  setShowSignupNudge: (show: boolean) => void;
  logout: () => void;
}

export const useAuthStore = create<AuthState>()(
  persist(
    (set, get) => ({
      user: null,
      isAnonymous: true,
      isAuthenticated: false,
      interactionCount: 0,
      showSignupNudge: false,
      
      setUser: (user) => set({ 
        user, 
        isAuthenticated: !!user,
        isAnonymous: !user 
      }),
      
      setAnonymous: (isAnonymous) => set({ isAnonymous }),
      
      incrementInteraction: () => {
        const count = get().interactionCount + 1;
        set({ interactionCount: count });
        
        // Show signup nudge after 3 interactions for anonymous users
        if (count >= 3 && get().isAnonymous && !get().showSignupNudge) {
          set({ showSignupNudge: true });
        }
      },
      
      setShowSignupNudge: (show) => set({ showSignupNudge: show }),
      
      logout: () => set({ 
        user: null, 
        isAuthenticated: false,
        isAnonymous: true,
        showSignupNudge: false
      })
    }),
    {
      name: 'alfred-auth-storage'
    }
  )
);
