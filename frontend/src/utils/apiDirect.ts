// Direct API access without using Next.js API routes
// Use this in production environments to call the backend directly

// Explicitly set production API URL with the correct domain
const API_URL = process.env.NODE_ENV === 'production'
  ? 'https://api-tiksave-wk4wf.ondigitalocean.app/api/v1'  // Replace with your actual API domain
  : process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000/api/v1';

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
  console.log('Sending direct API request to:', `${API_URL}/download`);
  
  const response = await fetch(`${API_URL}/download`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
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
    } catch (e) {
      throw new Error(`Request failed with status ${response.status}`);
    }
  }
  
  return response.json();
}

/**
 * Get the current status of a download
 */
export async function getDownloadStatus(sessionId: string): Promise<DownloadStatus> {
  const response = await fetch(`${API_URL}/status/${sessionId}`);
  
  if (!response.ok) {
    try {
      const errorData = await response.json();
      throw new Error(errorData.detail || `Failed to get status: ${response.status}`);
    } catch (e) {
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
    },
  });

  if (!response.ok) {
    try {
      const errorData = await response.json();
      throw new Error(errorData.detail || `Download failed with status ${response.status}`);
    } catch (e) {
      throw new Error(`Download failed with status ${response.status}`);
    }
  }

  return response.blob();
}

/**
 * Check the health of the API
 */
export async function checkApiHealth(): Promise<any> {
  try {
    const response = await fetch(`${API_URL.replace('/api/v1', '')}/health`);
    if (!response.ok) {
      throw new Error(`Health check failed with status ${response.status}`);
    }
    return response.json();
  } catch (error) {
    console.error('API Health Check Error:', error);
    throw error;
  }
} 