'use client';

import React, { useState, useEffect } from 'react';
import { ExternalLink, FileDown, CheckCircle, Share2, User, Clock, AlertCircle, Download } from 'lucide-react';
import Image from 'next/image';
import ExpirationCountdown from './ExpirationCountdown';
import { downloadVideoWithProgress } from '../utils/api';

interface VideoData {
  id: string;
  thumbnail: string;
  title: string;
  author: string;
  duration?: number;
  preview_url?: string;
  download_url: string;
  downloadLinks?: {
    quality: string;
    size: string;
    url: string;
  }[];
  session_id: string;
  status?: string;
  expires_at?: number;
  filename?: string;
}

interface VideoPreviewProps {
  videoData: VideoData | null;
}

const VideoPreview: React.FC<VideoPreviewProps> = ({ videoData }) => {
  const [selectedQuality, setSelectedQuality] = useState<string | null>(null);
  const [downloadStarted, setDownloadStarted] = useState(false);
  const [isExpired, setIsExpired] = useState(false);
  const [downloadProgress, setDownloadProgress] = useState(0);
  const [error, setError] = useState<string | null>(null);
  const [showProgressBar, setShowProgressBar] = useState(false);

  // Check for expiration when component mounts or data changes
  useEffect(() => {
    if (videoData?.status === 'expired') {
      setIsExpired(true);
    }
  }, [videoData?.status]);

  if (!videoData) return null;

  const handleExpired = () => {
    setIsExpired(true);
    setError('This download has expired. Please request a new download.');
  };

  // Format duration to MM:SS
  const formatDuration = (seconds?: number) => {
    if (!seconds) return '--:--';
    const mins = Math.floor(seconds / 60);
    const secs = Math.floor(seconds % 60);
    return `${mins}:${secs.toString().padStart(2, '0')}`;
  };

  const handleDownload = async (url: string, quality: string) => {
    if (isExpired) {
      alert('This download has expired. Please request a new download.');
      return;
    }

    setSelectedQuality(quality);
    setDownloadStarted(true);
    setDownloadProgress(0);
    setError(null);
    setShowProgressBar(true);
    
    try {
      // Use the downloadVideoWithProgress to track progress
      const blob = await downloadVideoWithProgress(
        videoData.session_id,
        (progress) => setDownloadProgress(progress)
      );
      
      // Create a URL for the blob
      const downloadUrl = window.URL.createObjectURL(blob);
      
      // Create a temporary link element
      const link = document.createElement('a');
      link.href = downloadUrl;
      
      // Set filename - prefer filename from server, fallback to video title
      const filename = videoData.filename || 
                      `${videoData.title || 'video'}_${videoData.session_id.substring(0, 8)}.mp4`;
      
      link.download = filename;
      
      // Append to body, click, and remove
      document.body.appendChild(link);
      link.click();
      document.body.removeChild(link);
      
      // Clean up the URL
      window.URL.revokeObjectURL(downloadUrl);
      
      // Update UI - don't reset immediately to show 100% progress
      setTimeout(() => {
        setDownloadStarted(false);
        setSelectedQuality(null);
        setShowProgressBar(false);
      }, 3000);
    } catch (error) {
      console.error('Download failed:', error);
      setError(error instanceof Error ? error.message : 'Failed to download the video. Please try again.');
      setDownloadStarted(false);
      setSelectedQuality(null);
      setShowProgressBar(false);
    }
  };

  const handleShare = () => {
    if (navigator.share) {
      navigator.share({
        title: videoData.title,
        text: `Check out this video: ${videoData.title}`,
        url: `https://www.tiktok.com/@${videoData.author}/video/${videoData.id}`
      });
    }
  };

  return (
    <div className="bg-white dark:bg-gray-800 rounded-xl shadow-lg overflow-hidden">
      <div className="p-6">
        <div className="flex justify-between items-center mb-4">
          <h2 className="text-xl font-bold text-gray-900 dark:text-white">Video Preview</h2>
          {videoData.expires_at && (
            <ExpirationCountdown 
              expiresAt={videoData.expires_at}
              onExpired={handleExpired}
              isAlreadyExpired={videoData.status === 'expired' || isExpired}
            />
          )}
        </div>
        
        {/* Show error message if present */}
        {error && (
          <div className="bg-red-50 dark:bg-red-900/20 border border-red-200 dark:border-red-800 rounded-lg p-4 mb-4 text-red-600 dark:text-red-400 flex items-start">
            <AlertCircle className="w-5 h-5 mr-2 mt-0.5 flex-shrink-0" />
            <p>{error}</p>
          </div>
        )}
        
        {/* Show progress bar when download is in progress */}
        {showProgressBar && (
          <div className="mb-6">
            <div className="flex items-center justify-between mb-2">
              <div className="flex items-center">
                <div className="w-8 h-8 rounded-full bg-blue-100 dark:bg-blue-900/20 flex items-center justify-center mr-3">
                  <Download className="w-5 h-5 text-blue-600 dark:text-blue-400" />
                </div>
                <div>
                  <h3 className="text-sm font-medium text-gray-900 dark:text-white">
                    {downloadProgress < 100 ? 'Downloading Video...' : 'Download Complete'}
                  </h3>
                  <p className="text-xs text-gray-500 dark:text-gray-400">
                    {downloadProgress < 100 
                      ? 'Please wait while your video is being prepared...'
                      : 'Your video is ready to save locally'}
                  </p>
                </div>
              </div>
              <div className="text-sm font-medium text-blue-600 dark:text-blue-400">
                {downloadProgress}%
              </div>
            </div>
            <div className="w-full bg-gray-200 dark:bg-gray-700 rounded-full h-2 overflow-hidden">
              <div 
                className="bg-gradient-to-r from-teal-500 to-purple-500 h-2 rounded-full transition-all duration-300" 
                style={{ width: `${downloadProgress}%` }}
              ></div>
            </div>
          </div>
        )}
        
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
          {/* Thumbnail */}
          <div className="md:col-span-1">
            <div className="relative rounded-lg overflow-hidden bg-gray-100 dark:bg-gray-900 aspect-[9/16]">
              <div className="relative w-full h-full">
                {videoData.thumbnail ? (
                  <div className="w-full h-full">
                    {/* Using unoptimized prop for external images that aren't in the config */}
                    <Image 
                      src={videoData.thumbnail}
                      alt={videoData.title}
                      className="w-full h-full object-cover"
                      width={400}
                      height={600}
                      unoptimized
                      onError={(e) => {
                        // Set a transparent SVG as fallback to avoid further errors
                        e.currentTarget.src = "data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='100' height='100' viewBox='0 0 100 100'%3E%3Crect width='100' height='100' fill='%23f3f4f6'/%3E%3Ctext x='50' y='50' font-family='sans-serif' font-size='10' text-anchor='middle' alignment-baseline='middle' fill='%23a1a1aa'%3ENo Image%3C/text%3E%3C/svg%3E";
                      }}
                    />
                  </div>
                ) : (
                  <div className="w-full h-full flex items-center justify-center bg-gray-200 dark:bg-gray-800">
                    <p className="text-gray-500 dark:text-gray-400 text-sm">No thumbnail available</p>
                  </div>
                )}
              </div>
              {/* Platform badge */}
              <div className="absolute top-2 left-2 bg-black/70 text-white text-xs px-2 py-1 rounded-full z-10">
                {videoData.id?.includes('youtube') ? 'YouTube' : 
                 videoData.id?.includes('instagram') ? 'Instagram' : 'TikTok'}
              </div>
              {/* Duration badge - if available */}
              {videoData.duration && (
                <div className="absolute top-2 right-2 bg-black/70 text-white text-xs px-2 py-1 rounded-full z-10">
                  {formatDuration(videoData.duration)}
                </div>
              )}
              {/* Gradient overlay and title */}
              <div className="absolute inset-0 bg-gradient-to-t from-black/80 via-black/40 to-transparent flex flex-col justify-end p-3 z-10">
                <p className="text-white text-sm font-semibold line-clamp-2 mb-0.5">
                  {videoData.title}
                </p>
                <div className="flex items-center text-gray-300 text-xs mt-1">
                  <User className="w-3 h-3 mr-1" />
                  <span>@{videoData.author}</span>
                </div>
              </div>
            </div>
          </div>
          
          {/* Video Details */}
          <div className="md:col-span-2 flex flex-col">
            <h3 className="text-lg font-semibold text-gray-900 dark:text-white mb-2">{videoData.title}</h3>
            
            <div className="flex items-center text-sm text-gray-500 dark:text-gray-400 mb-2">
              <User className="w-4 h-4 mr-1" />
              <span>{videoData.author}</span>
            </div>
            
            {videoData.duration && (
              <div className="flex items-center text-sm text-gray-500 dark:text-gray-400 mb-4">
                <Clock className="w-4 h-4 mr-1" />
                <span>{formatDuration(videoData.duration)}</span>
              </div>
            )}
            
            {/* Download Options */}
            <div className="mt-4">
              <h4 className="text-sm font-semibold text-gray-700 dark:text-gray-300 mb-3">
                Select Quality:
              </h4>
              
              {isExpired ? (
                <div className="bg-red-50 dark:bg-red-900/20 border border-red-200 dark:border-red-800 rounded-lg p-4 text-red-600 dark:text-red-400">
                  This download has expired. Please request a new download.
                </div>
              ) : (
                <div className="space-y-3">
                  {(videoData.downloadLinks || [
                    // If no download links provided, create a default option
                    {
                      quality: 'Original',
                      size: 'Unknown',
                      url: '' // We'll use session_id instead
                    }
                  ]).map((link) => (
                    <div 
                      key={link.quality}
                      className="bg-gray-50 dark:bg-gray-900 border border-gray-200 dark:border-gray-700 rounded-lg p-4 flex items-center justify-between transition-all duration-200 hover:border-teal-500 dark:hover:border-teal-500"
                    >
                      <div>
                        <span className="text-sm font-medium text-gray-900 dark:text-gray-100">
                          {link.quality} Quality
                        </span>
                        <p className="text-xs text-gray-500 dark:text-gray-400 mt-1">
                          Approx. size: {link.size}
                        </p>
                      </div>
                      <button
                        onClick={() => handleDownload(link.url, link.quality)}
                        disabled={downloadStarted}
                        className={`px-4 py-2 rounded-lg text-sm font-medium flex items-center gap-2 transition-all duration-300 ${
                          downloadStarted
                            ? selectedQuality === link.quality
                              ? 'bg-green-100 dark:bg-green-900/30 text-green-600 dark:text-green-400'
                              : 'bg-gray-100 dark:bg-gray-800 text-gray-400 dark:text-gray-600 cursor-not-allowed'
                            : 'bg-teal-100 dark:bg-teal-900/20 text-teal-600 dark:text-teal-400 hover:bg-teal-200 dark:hover:bg-teal-900/30'
                        }`}
                      >
                        {downloadStarted && selectedQuality === link.quality ? (
                          <>
                            {downloadProgress < 100 ? (
                              <div className="w-4 h-4 border-2 border-current border-t-transparent rounded-full animate-spin mr-1" />
                            ) : (
                              <CheckCircle className="w-4 h-4" />
                            )}
                            <span>
                              {downloadProgress < 100 ? 'Downloading...' : 'Download Complete'}
                            </span>
                          </>
                        ) : (
                          <>
                            <FileDown className="w-4 h-4" />
                            <span>Download</span>
                          </>
                        )}
                      </button>
                    </div>
                  ))}
                </div>
              )}
            </div>
            
            <div className="mt-6 flex justify-between items-center">
              <button
                onClick={handleShare}
                className="text-sm text-gray-600 dark:text-gray-400 hover:text-teal-600 dark:hover:text-teal-400 transition-colors flex items-center gap-1"
              >
                <Share2 className="w-4 h-4" />
                <span>Share</span>
              </button>
              
              <a 
                href={`https://www.tiktok.com/@${videoData.author}/video/${videoData.id}`}
                target="_blank"
                rel="noopener noreferrer"
                className="text-sm text-gray-600 dark:text-gray-400 hover:text-teal-600 dark:hover:text-teal-400 transition-colors flex items-center gap-1"
              >
                <ExternalLink className="w-4 h-4" />
                <span>View Original</span>
              </a>
            </div>
          </div>
        </div>
        
        {/* Ad Banner */}
        <div className="mt-6 p-4 bg-gray-100 dark:bg-gray-700 rounded-lg text-center text-sm text-gray-700 dark:text-gray-300">
          Ad: Support our free service by viewing this advertisement
        </div>
      </div>
    </div>
  );
};

export default VideoPreview; 