import { createDownload as createDirectDownload } from '@/utils/apiDirect';

export interface TikTokVideoData {
  id: string;
  title: string;
  author: string;
  duration?: number;
  thumbnail: string;
  preview_url?: string;
  download_url: string;
  session_id: string;
  downloadLinks?: Array<{
    quality: string;
    size: string;
    url: string;
  }>;
}

/**
 * Downloads a TikTok video by calling the backend API
 * @param url TikTok video URL
 * @param quality Video quality (HIGH, MEDIUM, LOW)
 * @returns Promise with video data
 */
export const downloadTikTokVideo = async (
  url: string, 
  quality: 'HIGH' | 'MEDIUM' | 'LOW' = 'HIGH'
): Promise<TikTokVideoData> => {
  try {
    // In production, use the direct API approach to avoid Next.js API routing issues
    if (process.env.NODE_ENV === 'production') {
      console.log('Using direct API approach in production');
      const headers = {
        'X-API-Key': process.env.NEXT_PUBLIC_WEBSITE_API_KEY
      };
      const data = await createDirectDownload(
        url.trim(),
        'tiktok',
        quality.toLowerCase(),
        headers
      );
      
      // Format the response to match our interface
      return {
        id: data.id || `video-${Date.now()}`,
        title: data.title || 'TikTok Video',
        author: data.author || '@user',
        duration: data.duration,
        thumbnail: data.thumbnail || 'https://placehold.co/600x800/9b5cf6/ffffff?text=TikTok+Thumbnail',
        preview_url: data.preview_url,
        download_url: data.download_url || data.file_path,
        session_id: data.session_id || `session-${Date.now()}`,
        // Create downloadLinks array if it doesn't exist
        downloadLinks: data.downloadLinks || [
          {
            quality: quality,
            size: 'Unknown',
            url: data.download_url || data.file_path || '#'
          }
        ]
      };
    }
    
    // In development, use the Next.js API route approach
    // Call the Next.js API route which proxies to the backend
    const apiUrl = '/api/v1/download';
    
    console.log('Sending request to API:', apiUrl);
    
    const headers = {
      'Content-Type': 'application/json',
      'Accept': 'application/json',
      'X-API-Key': process.env.NEXT_PUBLIC_WEBSITE_API_KEY
    };
    
    const response = await fetch(apiUrl, {
      method: 'POST',
      headers: headers,
      body: JSON.stringify({ 
        url: url.trim(),
        platform: 'tiktok',
        quality: quality.toLowerCase()
      }),
    });
    
    // Check if the response is JSON
    const contentType = response.headers.get('content-type');
    if (!contentType || !contentType.includes('application/json')) {
      // Try to get the text response for debugging
      const textResponse = await response.text();
      console.error('Received non-JSON response:', textResponse.substring(0, 150) + '...');
      throw new Error('The server returned an invalid response. Please try again later.');
    }
    
    const data = await response.json();
    
    if (!response.ok) {
      // Handle 422 validation errors specifically
      if (response.status === 422) {
        console.error('Validation error:', data);
        
        // Check if there are detailed validation errors from FastAPI
        if (data.validation_errors) {
          const errorDetails = Array.isArray(data.validation_errors) 
            ? data.validation_errors.map((e: { msg: string }) => e.msg).join(', ')
            : JSON.stringify(data.validation_errors);
          throw new Error(`Validation error: ${errorDetails}`);
        }
        
        throw new Error('The request was rejected due to validation errors. Please check your URL and try again.');
      }
      
      // Handle rate limiting specifically
      if (response.status === 429) {
        console.error('Rate limit exceeded:', data);
        
        // Check if this is a download limit error
        if (data.detail && typeof data.detail === 'object' && data.detail.error && data.detail.error.includes('Download limit reached')) {
          throw new Error(`Download limit reached. You can download 5 videos per 30 minutes with the free plan. Upgrade to Premium for more downloads.`);
        }
        
        // General rate limiting error
        throw new Error(`Rate limit exceeded. Please try again in ${data.detail?.retry_after_seconds || 'a few minutes'}.`);
      }
      
      throw new Error(data.detail || `Backend returned status ${response.status}`);
    }
    
    console.log('Received successful response:', data);
    
    // Format the response to match our interface
    return {
      id: data.id || `video-${Date.now()}`,
      title: data.title || 'TikTok Video',
      author: data.author || '@user',
      duration: data.duration,
      thumbnail: data.thumbnail || 'https://placehold.co/600x800/9b5cf6/ffffff?text=TikTok+Thumbnail',
      preview_url: data.preview_url,
      download_url: data.download_url || data.file_path,
      session_id: data.session_id || `session-${Date.now()}`,
      // Create downloadLinks array if it doesn't exist
      downloadLinks: data.downloadLinks || [
        {
          quality: quality,
          size: 'Unknown',
          url: data.download_url || data.file_path || '#'
        }
      ]
    };
  } catch (error) {
    console.error('Error downloading TikTok video:', error);
    throw error; // Re-throw the error to be handled by the calling component
  }
}; 