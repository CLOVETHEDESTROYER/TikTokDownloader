/**
 * API Configuration
 * This file centralizes API configuration for easier production deployment
 */

// Production API URL - This should be the full URL to your backend API in production
const PRODUCTION_API_URL = '/api/v1';

// Development API URL - Local development URL
const DEVELOPMENT_API_URL = 'http://localhost:8000';

// API version
const API_VERSION = 'v1';

/**
 * Get the environment the app is running in
 */
export const getEnvironment = (): 'development' | 'production' => {
  return process.env.NODE_ENV === 'production' ? 'production' : 'development';
};

/**
 * Get the base API URL without version
 */
export const getBaseApiUrl = (): string => {
  const env = getEnvironment();
  if (env === 'production') {
    return process.env.NEXT_PUBLIC_API_URL?.split('/api/')[0] || PRODUCTION_API_URL;
  }
  return process.env.NEXT_PUBLIC_API_URL?.split('/api/')[0] || DEVELOPMENT_API_URL;
};

/**
 * Get the complete API URL with version
 */
export const getApiUrl = (): string => {
  return `${getBaseApiUrl()}/api/${API_VERSION}`;
};

/**
 * Get the health check URL
 */
export const getHealthUrl = (): string => {
  return `${getBaseApiUrl()}/health`;
};

/**
 * Get the WebSocket URL
 */
export const getWebSocketUrl = (): string => {
  const baseUrl = getBaseApiUrl();
  const wsProtocol = baseUrl.startsWith('https') ? 'wss' : 'ws';
  return `${wsProtocol}://${baseUrl.split('://')[1]}/ws`;
};

/**
 * Get endpoint URLs for specific API operations
 */
export const getEndpoints = () => ({
  download: `${getApiUrl()}/download`,
  status: (sessionId: string) => `${getApiUrl()}/status/${sessionId}`,
  file: (sessionId: string) => `${getApiUrl()}/file/${sessionId}`,
  health: getHealthUrl(),
  websocket: getWebSocketUrl(),
});

// Export a complete config object for convenience
export const apiConfig = {
  environment: getEnvironment(),
  baseUrl: getBaseApiUrl(),
  apiUrl: getApiUrl(),
  healthUrl: getHealthUrl(),
  wsUrl: getWebSocketUrl(),
  endpoints: getEndpoints(),
  version: API_VERSION,
  
  // Log API configuration in development
  logConfig: () => {
    console.log('API Configuration:', {
      environment: getEnvironment(),
      baseUrl: getBaseApiUrl(),
      apiUrl: getApiUrl(),
      healthUrl: getHealthUrl(),
      wsUrl: getWebSocketUrl(),
      version: API_VERSION,
    });
  }
};

// Log configuration in development
if (getEnvironment() === 'development') {
  apiConfig.logConfig();
}

export default apiConfig; 