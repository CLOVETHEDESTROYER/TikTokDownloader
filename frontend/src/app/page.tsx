'use client';

import { useState } from 'react';
import { Toaster } from 'react-hot-toast';
import DownloadForm from '@/components/DownloadForm';
import VideoPreview from '@/components/VideoPreview';
import RecentDownloads from '@/components/RecentDownloads';
import Instructions from '@/components/Instructions';
import AdBanner from '@/components/AdBanner';
import DownloadProgress from '@/components/DownloadProgress';
import Script from 'next/script';
import { TikTokVideoData } from '@/services/downloadService';

// Define the VideoData interface
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
}

export default function Home() {
  const [activeDownloads, setActiveDownloads] = useState<string[]>([]);
  const [videoData, setVideoData] = useState<VideoData | null>(null);

  const handleDownloadComplete = (sessionId: string) => {
    setActiveDownloads((prev) => prev.filter((id) => id !== sessionId));
  };

  const handleVideoFetched = (data: TikTokVideoData) => {
    // Add the download to active downloads
    setActiveDownloads((prev) => [...prev, data.session_id]);
    
    // Set the video data for preview
    setVideoData({
      id: data.id,
      thumbnail: data.thumbnail,
      title: data.title,
      author: data.author,
      duration: data.duration,
      preview_url: data.preview_url,
      download_url: data.download_url,
      downloadLinks: data.downloadLinks || [
        {
          quality: 'High Quality',
          size: 'Unknown',
          url: data.download_url
        }
      ],
      session_id: data.session_id
    });
    
    // Scroll to the video preview section
    setTimeout(() => {
      const previewElement = document.getElementById('video-preview');
      if (previewElement) {
        window.scrollTo({
          top: previewElement.offsetTop,
          behavior: 'smooth'
        });
      }
    }, 200);
  };

  return (
    <>
      <Script
        async
        src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client=YOUR-AD-CLIENT-ID"
        crossOrigin="anonymous"
      />
      
      <main className="container mx-auto px-4 py-8">
        <Toaster position="top-right" />
        
        {/* Hero Section */}
        <div className="text-center mb-10">
          <h1 className="text-3xl md:text-4xl lg:text-5xl font-bold mb-4 bg-gradient-to-r from-teal-600 to-purple-600 bg-clip-text text-transparent">
          TikTok Video Downloader
        </h1>
          <p className="text-lg text-gray-700 dark:text-gray-300 max-w-2xl mx-auto">
            Download TikTok videos without watermark in seconds. Free, fast, and easy to use.
          </p>
        </div>
        
        {/* Ad Banner - Top */}
        <AdBanner location="top" className="mb-8 mx-auto max-w-3xl" />
        
        {/* Main Content */}
        <div className="flex flex-col lg:flex-row gap-8">
          {/* Main Content */}
          <div className="flex-1 space-y-8">
            {/* Download Form */}
            <DownloadForm onVideoFetched={handleVideoFetched} />

            {/* Video Preview */}
            <div id="video-preview" className="max-w-3xl mx-auto">
              <VideoPreview videoData={videoData} />
            </div>
            
            {/* Active Downloads */}
            <div className="space-y-6 max-w-3xl mx-auto">
              {activeDownloads.map((sessionId) => (
                <DownloadProgress
                  key={sessionId}
                  sessionId={sessionId}
                  onComplete={() => handleDownloadComplete(sessionId)}
                />
              ))}
            </div>
            
            {/* Recent Downloads */}
            <RecentDownloads />
            
            {/* Instructions */}
            <Instructions />
            
            {/* Ad Banner - Bottom */}
            <AdBanner location="bottom" className="mt-10 mx-auto max-w-3xl" />
          </div>

          {/* Sidebar Ads (Desktop) */}
          <div className="hidden lg:block w-[300px] space-y-6">
            <div className="sticky top-4">
              <AdBanner location="sidebar-top" className="h-[600px]" />
              <AdBanner location="sidebar-bottom" className="mt-6 h-[250px]" />
            </div>
          </div>
        </div>
      </main>
    </>
  );
}
