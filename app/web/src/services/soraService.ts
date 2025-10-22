/**
 * Sora 2 Video Download Service
 * Handles downloading and processing Sora 2 videos without watermarks
 */

export interface SoraVideoData {
  session_id: string;
  status: string;
  message: string;
  download_url?: string;
  description: string;
  author: string;
}

export interface SoraTestResult {
  url: string;
  title: string;
  formats: any[];
  extractor: string;
  webpage_url: string;
  description: string;
  duration: number;
  uploader: string;
  error?: string;
}

const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || '/api/v1';

/**
 * Download a Sora 2 video without watermark
 */
export async function downloadSoraVideo(url: string, quality: 'high' | 'medium' | 'low' = 'high', cookies?: string): Promise<SoraVideoData> {
  const requestBody: any = { url, quality };
  if (cookies) {
    requestBody.cookies = cookies;
  }
  
  const response = await fetch(`${API_BASE_URL}/sora/download`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'X-API-Key': process.env.NEXT_PUBLIC_WEBSITE_API_KEY || '',
    },
    body: JSON.stringify(requestBody),
  });

  if (!response.ok) {
    const errorData = await response.json().catch(() => ({}));
    throw new Error(errorData.detail || `HTTP ${response.status}: ${response.statusText}`);
  }

  return response.json();
}

/**
 * Test Sora 2 video extraction to see available formats
 */
export async function testSoraExtraction(url: string, cookies?: string): Promise<SoraTestResult> {
  const requestBody: any = { url };
  if (cookies) {
    requestBody.cookies = cookies;
  }
  
  const response = await fetch(`${API_BASE_URL}/sora/test`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'X-API-Key': process.env.NEXT_PUBLIC_WEBSITE_API_KEY || '',
    },
    body: JSON.stringify(requestBody),
  });

  if (!response.ok) {
    const errorData = await response.json().catch(() => ({}));
    throw new Error(errorData.detail || `HTTP ${response.status}: ${response.statusText}`);
  }

  return response.json();
}

/**
 * Batch download multiple Sora 2 videos
 */
export async function batchDownloadSoraVideos(urls: string[], quality: 'high' | 'medium' | 'low' = 'high'): Promise<{results: SoraVideoData[]}> {
  const response = await fetch(`${API_BASE_URL}/sora/batch`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'X-API-Key': process.env.NEXT_PUBLIC_WEBSITE_API_KEY || '',
    },
    body: JSON.stringify({
      urls,
      quality,
    }),
  });

  if (!response.ok) {
    const errorData = await response.json().catch(() => ({}));
    throw new Error(errorData.detail || `HTTP ${response.status}: ${response.statusText}`);
  }

  return response.json();
}

/**
 * Get the status of a Sora download
 */
export async function getSoraDownloadStatus(sessionId: string): Promise<SoraVideoData> {
  const response = await fetch(`${API_BASE_URL}/sora/status/${sessionId}`, {
    method: 'GET',
    headers: {
      'X-API-Key': process.env.NEXT_PUBLIC_WEBSITE_API_KEY || '',
    },
  });

  if (!response.ok) {
    const errorData = await response.json().catch(() => ({}));
    throw new Error(errorData.detail || `HTTP ${response.status}: ${response.statusText}`);
  }

  return response.json();
}

/**
 * Check if a URL is a valid Sora 2 URL
 */
export function isValidSoraUrl(url: string): boolean {
  if (!url || typeof url !== 'string') return false;
  
  const soraPatterns = [
    /sora\.chatgpt\.com\/p\/s_/i,      // Actual Sora URL format
    /sora\.openai\.com\/video\//i,      // Legacy format
    /openai\.com\/sora\//i,             // Legacy format
    /sora\.openai\.com\//i,             // Generic format
  ];
  
  return soraPatterns.some(pattern => pattern.test(url));
}

/**
 * Extract video ID from Sora URL
 */
export function extractSoraVideoId(url: string): string | null {
  const patterns = [
    /sora\.chatgpt\.com\/p\/s_([a-zA-Z0-9_-]+)/i,  // Actual Sora URL format
    /sora\.openai\.com\/video\/([a-zA-Z0-9_-]+)/i,  // Legacy format
    /openai\.com\/sora\/([a-zA-Z0-9_-]+)/i,         // Legacy format
    /sora\/([a-zA-Z0-9_-]+)/i,                      // Generic format
  ];
  
  for (const pattern of patterns) {
    const match = url.match(pattern);
    if (match) {
      return match[1];
    }
  }
  
  return null;
}
