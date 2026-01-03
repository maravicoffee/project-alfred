/**
 * Project Alfred - Authentication Service
 * Handles all authentication-related API calls
 */

import API_BASE_URL from '../config/api';

export interface AuthResponse {
  success: boolean;
  message: string;
  user?: {
    id: string;
    email: string;
    name?: string;
  };
  token?: string;
}

export interface MigrationResponse {
  success: boolean;
  message: string;
  migratedConversations?: number;
  migratedMessages?: number;
}

class AuthService {
  /**
   * Send magic link to email
   */
  async sendMagicLink(email: string): Promise<AuthResponse> {
    try {
      const response = await fetch(`${API_BASE_URL}/api/auth/magic-link`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({ email })
      });
      
      return await response.json();
    } catch (error) {
      console.error('Magic link error:', error);
      return {
        success: false,
        message: 'Failed to send magic link. Please try again.'
      };
    }
  }
  
  /**
   * Verify magic link token
   */
  async verifyMagicLink(token: string): Promise<AuthResponse> {
    try {
      const response = await fetch(`${API_BASE_URL}/api/auth/verify?token=${token}`, {
        method: 'GET'
      });
      
      return await response.json();
    } catch (error) {
      console.error('Verification error:', error);
      return {
        success: false,
        message: 'Failed to verify token. Please try again.'
      };
    }
  }
  
  /**
   * Initiate Google OAuth flow
   */
  async initiateGoogleAuth(): Promise<void> {
    window.location.href = `${API_BASE_URL}/api/auth/google`;
  }
  
  /**
   * Handle OAuth callback
   */
  async handleOAuthCallback(code: string): Promise<AuthResponse> {
    try {
      const response = await fetch(`${API_BASE_URL}/api/auth/google/callback?code=${code}`, {
        method: 'GET'
      });
      
      return await response.json();
    } catch (error) {
      console.error('OAuth callback error:', error);
      return {
        success: false,
        message: 'Failed to authenticate with Google. Please try again.'
      };
    }
  }
  
  /**
   * Migrate local data to cloud
   */
  async migrateLocalData(userId: string, localData: any): Promise<MigrationResponse> {
    try {
      const response = await fetch(`${API_BASE_URL}/api/auth/migrate`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({
          userId,
          localData
        })
      });
      
      return await response.json();
    } catch (error) {
      console.error('Migration error:', error);
      return {
        success: false,
        message: 'Failed to migrate data. Please try again.'
      };
    }
  }
  
  /**
   * Logout
   */
  async logout(): Promise<void> {
    try {
      await fetch(`${API_BASE_URL}/api/auth/logout`, {
        method: 'POST'
      });
    } catch (error) {
      console.error('Logout error:', error);
    }
  }
}

export const authService = new AuthService();
