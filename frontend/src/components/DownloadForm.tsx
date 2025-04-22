'use client';

import React, { useState } from 'react';
import Link from 'next/link';
import { AlertCircle, Download, ExternalLink, Loader2 } from 'lucide-react';
import { useDownloads } from '@/context/DownloadsContext';
import { downloadTikTokVideo, TikTokVideoData } from '@/services/downloadService';

// Define quality options
type QualityOption = 'HIGH' | 'MEDIUM' | 'LOW';

interface DownloadFormProps {
  onVideoFetched: (videoData: TikTokVideoData) => void;
}

const DownloadForm: React.FC<DownloadFormProps> = ({ onVideoFetched }) => {
  const [url, setUrl] = useState('');
  const [quality, setQuality] = useState<QualityOption>('HIGH');
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const { addDownload } = useDownloads();

  const isValidTikTokUrl = (url: string): boolean => {
    // Basic validation - can be improved
    return url.trim() !== '' && 
      (url.includes('tiktok.com') || 
       url.includes('vm.tiktok.com') || 
       url.includes('vt.tiktok.com'));
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    
    if (!isValidTikTokUrl(url)) {
      setError('Please enter a valid TikTok URL');
      return;
    }
    
    setIsLoading(true);
    setError(null);
    
    try {
      // Call the download service with the selected quality
      const videoData = await downloadTikTokVideo(url, quality);
      onVideoFetched(videoData);
      addDownload({
        id: Date.now().toString(),
        url,
        timestamp: new Date().toISOString(),
        thumbnail: videoData.thumbnail,
        title: videoData.title
      });
    } catch (err: unknown) {
      // Try to extract more specific error messages
      let errorMessage = 'Failed to process this video. Please try again or try another URL.';
      
      if (err instanceof Error && err.message) {
        if (err.message.includes('validation')) {
          errorMessage = 'Invalid URL format. Please make sure you\'re using a correct TikTok video URL.';
        } else if (err.message.includes('status 403')) {
          errorMessage = 'This video is private or restricted. Please try another video.';
        } else if (err.message.includes('status 404')) {
          errorMessage = 'Video not found. The URL may be incorrect or the video has been removed.';
        } else if (err.message.includes('status 429')) {
          errorMessage = 'Too many requests. Please wait a few minutes and try again.';
        } else if (err.message.includes('status 5')) {
          errorMessage = 'Server error. Our backend is having issues. Please try again later.';
        } else {
          errorMessage = `Error: ${err.message}`;
        }
      }
      
      setError(errorMessage);
      console.error('Download error:', err);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="w-full max-w-3xl mx-auto">
      <div className="bg-white dark:bg-gray-800 rounded-xl shadow-lg p-6 md:p-8 transition-all duration-300">
        <h2 className="text-xl md:text-2xl font-bold text-gray-900 dark:text-white mb-2">
          Download TikTok Videos Without Watermark
        </h2>
        <p className="text-gray-600 dark:text-gray-400 mb-6">
          Paste a TikTok URL to download the video in your preferred quality without watermarks.
        </p>
        
        <form onSubmit={handleSubmit} className="space-y-4">
          <div className="relative">
            <input
              type="text"
              value={url}
              onChange={(e) => setUrl(e.target.value)}
              placeholder="https://www.tiktok.com/@username/video/1234567890"
              className="w-full p-4 pr-36 rounded-lg border-2 border-gray-300 dark:border-gray-700 focus:border-teal-500 dark:focus:border-teal-500 bg-gray-50 dark:bg-gray-900 text-gray-900 dark:text-gray-100 placeholder-gray-500 dark:placeholder-gray-500 transition-colors duration-200 focus:outline-none focus:ring-1 focus:ring-teal-500"
              disabled={isLoading}
            />
            <div className="absolute inset-y-0 right-0 flex items-center pr-2">
              <button
                type="submit"
                disabled={isLoading || !url.trim()}
                className={`px-4 py-2 rounded-lg font-medium flex items-center justify-center gap-2 transition-all duration-300 ${
                  isLoading || !url.trim()
                    ? 'bg-gray-300 dark:bg-gray-700 text-gray-600 dark:text-gray-400 cursor-not-allowed'
                    : 'bg-gradient-to-r from-teal-500 to-purple-500 hover:from-teal-600 hover:to-purple-600 text-white shadow-md hover:shadow-lg'
                }`}
              >
                {isLoading ? (
                  <>
                    <Loader2 className="w-5 h-5 animate-spin" />
                    <span>Processing</span>
                  </>
                ) : (
                  <>
                    <Download className="w-5 h-5" />
                    <span>Download</span>
                  </>
                )}
              </button>
            </div>
          </div>
          
          {/* Quality Selection */}
          <div className="flex flex-col md:flex-row gap-3 md:items-center my-4">
            <label className="text-sm font-medium text-gray-700 dark:text-gray-300">
              Video Quality:
            </label>
            <div className="flex flex-wrap gap-2">
              {(['HIGH', 'MEDIUM', 'LOW'] as const).map((q) => (
                <button
                  key={q}
                  type="button"
                  onClick={() => setQuality(q)}
                  className={`px-4 py-2 text-sm rounded-md transition-colors ${
                    quality === q
                      ? 'bg-teal-600 text-white'
                      : 'bg-gray-200 dark:bg-gray-700 text-gray-800 dark:text-gray-200 hover:bg-gray-300 dark:hover:bg-gray-600'
                  }`}
                >
                  {q === 'HIGH' ? 'High (1080p)' : q === 'MEDIUM' ? 'Medium (720p)' : 'Low (480p)'}
                </button>
              ))}
            </div>
          </div>
          
          {error && (
            <div className="bg-red-50 dark:bg-red-900/20 text-red-600 dark:text-red-400 p-3 rounded-lg flex items-start gap-2 text-sm">
              <AlertCircle className="w-5 h-5 flex-shrink-0 mt-0.5" />
              <span>{error}</span>
            </div>
          )}
          
          <div className="bg-gray-50 dark:bg-gray-900/50 rounded-lg p-4 text-xs text-gray-500 dark:text-gray-400">
            <div className="mb-2 border-b border-gray-200 dark:border-gray-700 pb-2">
              <span className="font-semibold">Free Plan:</span> 5 downloads per 30 minutes. <Link href="/premium" className="text-teal-600 dark:text-teal-400 hover:underline">Upgrade to Premium</Link> for unlimited downloads.
            </div>
            <p className="flex items-center">
              <ExternalLink className="w-4 h-4 mr-2 text-gray-400" />
              By using our service, you agree to our <Link href="/privacy-policy" className="text-teal-600 dark:text-teal-400 hover:underline ml-1">Terms of Service</Link>.
            </p>
          </div>
        </form>
      </div>
    </div>
  );
};

export default DownloadForm; 