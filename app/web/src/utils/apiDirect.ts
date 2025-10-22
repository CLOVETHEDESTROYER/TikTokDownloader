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
  // Check if we're in a browser environment
  if (typeof window !== 'undefined') {
    // We're in the browser
    const baseUrl = window.location.origin;
    console.log(`Base URL from window.location.origin: ${baseUrl}`);
    return `${baseUrl}/api/v1`;
  } else {
    // We're on the server
    return process.env.NEXT_PUBLIC_API_URL || '/api/v1';
  }
};

const getHealthUrl = () => {
  if (typeof window !== 'undefined') {
    return window.location.origin + '/health';
  } else {
    // Use a relative URL on the server
    return '/health';
  }
};

// Initialize these safely (handle both SSR and client)
const API_URL = typeof window !== 'undefined' ? getApiUrl() : '/api/v1';

// Only log these values on the client
if (typeof window !== 'undefined') {
  console.log('API URL: ' + getApiUrl());
  console.log('Health URL: ' + getHealthUrl());
  console.log('API URL configured as:', API_URL);
}

// Download status interface matching the backend model
export interface DownloadStatus {
  session_id: string;
  status: 'pending' | 'processing' | 'completed' | 'failed' | 'expired';
  progress: number;
  url: string;
  filename?: string;
  error?: string;
  expires_at?: number;
  // Additional fields from TikTok and extended responses
  id?: string;
  title?: string;
  author?: string;
  duration?: number;
  thumbnail?: string;
  preview_url?: string;
  download_url?: string;
  file_path?: string;
  downloadLinks?: Array<{
    quality: string;
    size: string;
    url: string;
  }>;
}

// Add this debugging at the top of the file
console.log('Environment Variables Debug:');
console.log('NODE_ENV:', process.env.NODE_ENV);
console.log('NEXT_PUBLIC_API_URL:', process.env.NEXT_PUBLIC_API_URL);
console.log('NEXT_PUBLIC_WEBSITE_API_KEY:', process.env.NEXT_PUBLIC_WEBSITE_API_KEY);

/**
 * Create a download for a video URL
 */
export async function createDownload(
  url: string, 
  platform: string, 
  quality: string,
  headers: Record<string, string> = {}
): Promise<DownloadStatus> {
  // Always use the main download endpoint
  const downloadUrl = `${API_URL}/download`;
  
  console.log('Making API request to:', downloadUrl);
  console.log('Using API Key:', process.env.NEXT_PUBLIC_WEBSITE_API_KEY ? 'Key is present' : 'Key is missing');
  
  // Always include platform in request body
  const requestBody = { 
    url, 
    platform, 
    quality 
  };
  
  const response = await fetch(downloadUrl, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'X-API-Key': process.env.NEXT_PUBLIC_WEBSITE_API_KEY || '',
      ...headers
    },
    body: JSON.stringify(requestBody),
  });
  
  if (!response.ok) {
    try {
      const errorData = await response.json();
      console.error('Error response:', errorData);
      throw new Error(errorData.detail || `Failed to create download: ${response.status}`);
    } catch (error) {
      console.error('Error parsing response:', error);
      throw new Error(`Request failed with status ${response.status}`);
    }
  }
  
  return response.json();
}

/**
 * Get the current status of a download
 */
export async function getDownloadStatus(sessionId: string): Promise<DownloadStatus> {
  const response = await fetch(`${API_URL}/download/status/${sessionId}`, {
    headers: {
      'Content-Type': 'application/json'
    }
  });
  
  if (!response.ok) {
    try {
      const errorData = await response.json();
      throw new Error(errorData.detail || `Failed to get status: ${response.status}`);
    } catch {
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
  const response = await fetch(`${API_URL}/download/file/${sessionId}`, {
    method: 'GET',
    headers: {
      'Accept': 'video/mp4'
    },
  });

  if (!response.ok) {
    try {
      const errorData = await response.json();
      throw new Error(errorData.detail || `Download failed with status ${response.status}`);
    } catch {
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
    const response = await fetch('/health');
    if (!response.ok) {
      throw new Error(`Health check failed with status ${response.status}`);
    }
    const data = await response.json();
    if (!data || typeof data.status !== 'string') {
      throw new Error('Invalid health check response format');
    }
    return data;
  } catch (error) {
    console.error('API Health Check Error:', error);
    throw error;
  }
} 