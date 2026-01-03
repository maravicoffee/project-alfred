/**
 * Project Alfred - API Configuration
 * Centralized API endpoint configuration
 */

// Get API base URL from environment variable or default to production API
export const API_BASE_URL = import.meta.env.VITE_API_URL || '/api';

// API endpoints
export const API_ENDPOINTS = {
  chat: `${API_BASE_URL}/chat`,
  conversations: `${API_BASE_URL}/conversations`,
  health: `${API_BASE_URL}/health`,
  tools: `${API_BASE_URL}/tools`,
};

export default API_BASE_URL;
