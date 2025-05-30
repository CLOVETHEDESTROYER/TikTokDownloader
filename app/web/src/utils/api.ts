// API Base URL with fallback to localhost
export const API_URL = process.env.NODE_ENV === 'production'
  ? '/api/v1'  // Use relative URL in production
  : process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000/api/v1';

// Use the Next.js API routes for frontend requests - no need to include /api/v1 since it's in the rewrite rule
export const FRONTEND_API_BASE_URL = '';

// Website API key from environment variables
export const WEBSITE_API_KEY = process.env.NEXT_PUBLIC_WEBSITE_API_KEY || '';

// Default headers for API requests
export const getDefaultHeaders = () => {
  const headers: Record<string, string> = {
    'Content-Type': 'application/json',
    'Accept': 'application/json',
  };
  
  // Add API key if available
  if (WEBSITE_API_KEY) {
    headers['X-API-Key'] = WEBSITE_API_KEY;
  }
  
  return headers;
};

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
  // Log the download attempt
  console.log(`Attempting to download file with session ID: ${sessionId}`);
  
  // Use direct backend URL to avoid routing issues
  const fileUrl = `${API_URL}/file/${sessionId}`;
  console.log(`Downloading directly from backend: ${fileUrl}`);
  
  const response = await fetch(fileUrl, {
    method: 'GET',
    headers: {
      'Accept': 'video/mp4',
      ...(WEBSITE_API_KEY ? { 'X-API-Key': WEBSITE_API_KEY } : {}),
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
  // Use the direct backend URL for status requests, just like we do for file downloads
  const response = await fetch(`${API_URL}/status/${sessionId}`, {
    headers: getDefaultHeaders(),
  });
  
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
  const response = await fetch(`/api/v1/download`, {
    method: 'POST',
    headers: getDefaultHeaders(),
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

/**
 * Download a video file with progress tracking
 * @param sessionId The session ID of the download
 * @param onProgress Optional callback for progress updates (0-100)
 * @returns A Promise resolving to a Blob containing the video data
 */
export const downloadVideoWithProgress = async (
  sessionId: string, 
  onProgress?: (progress: number) => void
): Promise<Blob> => {
  return new Promise(async (resolve, reject) => {
    try {
      // Use direct backend URL to avoid routing issues
      const fileUrl = `${API_URL}/file/${sessionId}`;
      console.log(`Downloading with progress directly from backend: ${fileUrl}`);
      
      // First, get the status to get an estimated size (if available)
      const estimatedSize = 0;
      try {
        const status = await getDownloadStatus(sessionId);
        if (status && status.filename) {
          console.log(`Download status for ${sessionId}:`, status);
        }
      } catch (e) {
        console.warn('Could not get download status for size estimation:', e);
      }
      
      // Now fetch the actual file
      const response = await fetch(fileUrl, {
        method: 'GET',
        headers: {
          'Accept': 'video/mp4',
          ...(WEBSITE_API_KEY ? { 'X-API-Key': WEBSITE_API_KEY } : {}),
        },
      });

      if (!response.ok) {
        // Try to parse error details if available
        try {
          const error = await response.json();
          reject(new Error(error.detail || `Download failed with status ${response.status}`));
        } catch {
          reject(new Error(`Download failed with status ${response.status}`));
        }
        return;
      }

      // Read the body as a stream
      const reader = response.body?.getReader();
      if (!reader) {
        reject(new Error('Unable to read response body'));
        return;
      }

      // Get content length from headers if available
      const contentLength = Number(response.headers.get('Content-Length')) || estimatedSize;
      
      // If no content length is available, we'll simulate progress
      const hasRealProgress = contentLength > 0;
      console.log(`Content length: ${contentLength}, has real progress: ${hasRealProgress}`);
      
      // For simulated progress, we'll update in 10 steps
      let simulatedProgress = 0;
      let simulatedInterval: number | null = null;
      
      if (!hasRealProgress && onProgress) {
        // Start simulated progress updates
        simulatedInterval = window.setInterval(() => {
          simulatedProgress += 10;
          if (simulatedProgress > 90) {
            if (simulatedInterval) {
              clearInterval(simulatedInterval);
              simulatedInterval = null;
            }
            return;
          }
          onProgress(simulatedProgress);
        }, 500) as unknown as number;
      }
      
      // Create array to store chunks
      const chunks: Uint8Array[] = [];
      let receivedLength = 0;

      // Process stream
      while (true) {
        const { done, value } = await reader.read();
        
        if (done) {
          break;
        }
        
        chunks.push(value);
        receivedLength += value.length;
        
        // Report progress if callback provided and content length is known
        if (onProgress && hasRealProgress) {
          const progress = Math.min(Math.round((receivedLength / contentLength) * 100), 100);
          onProgress(progress);
        }
      }
      
      // Clear any simulation interval if it exists
      if (simulatedInterval) {
        clearInterval(simulatedInterval);
      }
      
      // Report 100% progress when done
      if (onProgress) {
        onProgress(100);
      }
      
      // Concatenate chunks into a single Uint8Array
      const allChunks = new Uint8Array(receivedLength);
      let position = 0;
      for (const chunk of chunks) {
        allChunks.set(chunk, position);
        position += chunk.length;
      }
      
      // Convert to blob and resolve
      const blob = new Blob([allChunks], { type: response.headers.get('Content-Type') || 'video/mp4' });
      console.log(`Download completed for ${sessionId}, total size: ${receivedLength} bytes`);
      resolve(blob);
      
    } catch (error) {
      reject(error);
    }
  });
}; 