// Direct API access without using Next.js API routes
// Use this in production environments to call the backend directly

// Health check response type
interface HealthCheckResponse {
  status: string;
  version: string;
  env: string;
}

// Use environment variables for API URL or fallback to relative path in production
const getApiUrl = () => {
  // In production, use relative URLs to work with the proxy setup
  if (process.env.NODE_ENV === 'production') {
    return '/api/v1';
  }
  // In development, use the environment variable or fallback to localhost
  return process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000/api/v1';
};

const getHealthUrl = () => {
  // In production, just return empty string (base path)
  if (process.env.NODE_ENV === 'production') {
    return '';
  }
  // In development, use the base URL
  return process.env.NEXT_PUBLIC_API_URL?.replace('/api/v1', '') || 'http://localhost:8000';
};

const API_URL = getApiUrl();

console.log('API URL configured as:', API_URL);

// Download status interface matching the backend model
export interface DownloadStatus {
  session_id: string;
  status: 'pending' | 'processing' | 'completed' | 'failed' | 'expired';
  progress: number;
  url: string;
  filename?: string;
  error?: string;
  expires_at?: number;
}

/**
 * Create a download for a video URL
 */
export async function createDownload(url: string, platform: string, quality: string): Promise<DownloadStatus> {
  // Use absolute path
  const downloadUrl = '/api/v1/download';
  console.log('Sending direct API request to:', downloadUrl);
  
  const response = await fetch(downloadUrl, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'X-API-Key': process.env.NEXT_PUBLIC_WEBSITE_API_KEY || '',
    },
    body: JSON.stringify({
      url,
      platform,
      quality,
    }),
  });
  
  if (!response.ok) {
    try {
      const errorData = await response.json();
      throw new Error(errorData.detail || `Failed to create download: ${response.status}`);
    } catch (_error) {
      // If parsing the error response fails, throw a generic error
      throw new Error(`Request failed with status ${response.status}`);
    }
  }
  
  return response.json();
}

/**
 * Get the current status of a download
 */
export async function getDownloadStatus(sessionId: string): Promise<DownloadStatus> {
  const response = await fetch(`${API_URL}/status/${sessionId}`, {
    headers: {
      'X-API-Key': process.env.NEXT_PUBLIC_WEBSITE_API_KEY || '',
    }
  });
  
  if (!response.ok) {
    try {
      const errorData = await response.json();
      throw new Error(errorData.detail || `Failed to get status: ${response.status}`);
    } catch (_error) {
      // If parsing the error response fails, throw a generic error
      throw new Error(`Request failed with status ${response.status}`);
    }
  }
  
  return response.json();
}

/**
 * Download a video file by session ID
 */
export async function downloadVideo(sessionId: string): Promise<Blob> {
  const response = await fetch(`${API_URL}/file/${sessionId}`, {
    method: 'GET',
    headers: {
      'Accept': 'video/mp4',
      'X-API-Key': process.env.NEXT_PUBLIC_WEBSITE_API_KEY || '',
    },
  });

  if (!response.ok) {
    try {
      const errorData = await response.json();
      throw new Error(errorData.detail || `Download failed with status ${response.status}`);
    } catch (_error) {
      // If parsing the error response fails, throw a generic error
      throw new Error(`Download failed with status ${response.status}`);
    }
  }

  return response.blob();
}

/**
 * Check the health of the API
 */
export async function checkApiHealth(): Promise<HealthCheckResponse> {
  try {
    // Don't append /health to getHealthUrl() if it already returns /health
    const healthUrl = '/health';  // Use absolute path directly
    console.log('Checking API health at:', healthUrl);
    const response = await fetch(healthUrl);
    if (!response.ok) {
      throw new Error(`Health check failed with status ${response.status}`);
    }
    return response.json();
  } catch (error: unknown) {
    console.error('API Health Check Error:', error);
    throw error;
  }
} 