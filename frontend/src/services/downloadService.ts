// Mock data for development - in a real app, this would call your API
const mockVideoData = {
  id: 'mock-video-id',
  title: 'TikTok Video Example',
  author: '@tiktokcreator',
  duration: 30,
  thumbnail: 'https://placehold.co/600x800/9b5cf6/ffffff?text=TikTok+Thumbnail',
  preview_url: 'https://example.com/sample-video.mp4',
  download_url: 'https://example.com/sample-video-download.mp4',
  session_id: 'mock-session-id',
};

// Simulates API call latency
const delay = (ms: number) => new Promise(resolve => setTimeout(resolve, ms));

export interface TikTokVideoData {
  id: string;
  title: string;
  author: string;
  duration?: number;
  thumbnail: string;
  preview_url?: string;
  download_url: string;
  session_id: string;
}

/**
 * Downloads a TikTok video (mock implementation for frontend development)
 * @param url TikTok video URL
 * @returns Promise with video data
 */
export const downloadTikTokVideo = async (url: string): Promise<TikTokVideoData> => {
  try {
    // Simulate API call delay
    await delay(1500);
    
    // In a real app, this would call your backend API with the url parameter
    // const response = await fetch('/api/download', {
    //   method: 'POST',
    //   headers: { 'Content-Type': 'application/json' },
    //   body: JSON.stringify({ url }),
    // });
    // 
    // if (!response.ok) {
    //   throw new Error('Failed to download video');
    // }
    // 
    // return await response.json();
    
    // For demo purposes, return mock data
    // Using url in console log to avoid linter error
    console.log(`Processing video download for: ${url}`);
    
    return {
      ...mockVideoData,
      id: `mock-${Date.now()}`,
      session_id: `session-${Date.now()}`,
    };
  } catch (error) {
    console.error('Error downloading TikTok video:', error);
    throw new Error('Failed to download video. Please try again.');
  }
}; 