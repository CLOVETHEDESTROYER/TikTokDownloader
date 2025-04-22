// API Base URL with fallback to localhost
export const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000/api/v1';

// Use the Next.js API routes for frontend requests
export const FRONTEND_API_BASE_URL = '/api/v1';

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
 * Download a video file by session ID
 * @param sessionId The session ID of the download
 * @returns A Promise resolving to a Blob containing the video data
 */
export const downloadVideo = async (sessionId: string): Promise<Blob> => {
  // Use the Next.js API route for file downloads to avoid CORS issues
  const response = await fetch(`${FRONTEND_API_BASE_URL}/file/${sessionId}`, {
    method: 'GET',
    headers: {
      'Accept': 'video/mp4',
    },
  });

  if (!response.ok) {
    // Try to parse error details if available
    try {
      const error = await response.json();
      throw new Error(error.detail || `Download failed with status ${response.status}`);
    } catch {
      // If we can't parse JSON, use a generic error
      throw new Error(`Download failed with status ${response.status}`);
    }
  }

  return response.blob();
};

/**
 * Get the current status of a download
 * @param sessionId The session ID of the download
 * @returns A Promise resolving to the download status
 */
export const getDownloadStatus = async (sessionId: string): Promise<DownloadStatus> => {
  // Use the Next.js API route for status requests
  const response = await fetch(`${FRONTEND_API_BASE_URL}/status/${sessionId}`);
  
  if (!response.ok) {
    try {
      const error = await response.json();
      throw new Error(error.detail || `Failed to get download status: ${response.status}`);
    } catch {
      throw new Error(`Failed to get download status: ${response.status}`);
    }
  }

  return response.json();
};

/**
 * Create a download for a video URL
 * @param url The URL of the video to download
 * @param platform The platform of the video (tiktok, youtube, instagram)
 * @param quality The desired quality of the video
 * @returns A Promise resolving to the download status
 */
export const createDownload = async (
  url: string, 
  platform: string, 
  quality: string
): Promise<DownloadStatus> => {
  const response = await fetch(`${FRONTEND_API_BASE_URL}/download`, {
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
      const error = await response.json();
      throw new Error(error.detail || `Failed to create download: ${response.status}`);
    } catch {
      throw new Error(`Failed to create download: ${response.status}`);
    }
  }

  return response.json();
}; 