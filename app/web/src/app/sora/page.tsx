'use client';

import { useState } from 'react';
import { Toaster } from 'react-hot-toast';
import SoraDownloadForm from '@/components/SoraDownloadForm';
import VideoPreview from '@/components/VideoPreview';
import { SoraVideoData } from '@/services/soraService';

export default function SoraPage() {
  const [videoData, setVideoData] = useState<SoraVideoData | null>(null);
  const [activeDownloads, setActiveDownloads] = useState<string[]>([]);

  const handleVideoFetched = (data: SoraVideoData) => {
    setVideoData(data);
    setActiveDownloads((prev) => [...prev, data.session_id]);
  };

  const handleDownloadComplete = (sessionId: string) => {
    setActiveDownloads((prev) => prev.filter((id) => id !== sessionId));
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100 dark:from-gray-900 dark:to-gray-800">
      <Toaster position="top-right" />
      
      <div className="container mx-auto px-4 py-8">
        {/* Header */}
        <div className="text-center mb-8">
          <h1 className="text-4xl md:text-5xl font-bold text-gray-900 dark:text-white mb-4">
            🎬 Sora 2 Video Downloader
          </h1>
          <p className="text-xl text-gray-600 dark:text-gray-400 max-w-3xl mx-auto">
            Download AI-generated videos from OpenAI Sora 2 without watermarks. 
            Test and extract high-quality videos for your content creation needs.
          </p>
        </div>

        {/* Main Content */}
        <div className="space-y-8">
          {/* Download Form */}
          <SoraDownloadForm onVideoFetched={handleVideoFetched} />

          {/* Video Preview */}
          {videoData && (
            <VideoPreview
              videoData={{
                id: videoData.session_id,
                thumbnail: '', // Sora videos might not have thumbnails
                title: videoData.description || 'Sora Generated Video',
                author: videoData.author || 'OpenAI Sora',
                download_url: videoData.download_url || '',
                session_id: videoData.session_id,
              }}
              onDownloadComplete={handleDownloadComplete}
            />
          )}

          {/* Instructions */}
          <div className="max-w-4xl mx-auto">
            <div className="bg-white dark:bg-gray-800 rounded-xl shadow-lg p-6 md:p-8">
              <h2 className="text-2xl font-bold text-gray-900 dark:text-white mb-4">
                📋 How to Use
              </h2>
              <div className="space-y-4 text-gray-600 dark:text-gray-400">
                <div className="flex items-start space-x-3">
                  <span className="flex-shrink-0 w-6 h-6 bg-blue-100 dark:bg-blue-900 text-blue-600 dark:text-blue-400 rounded-full flex items-center justify-center text-sm font-bold">1</span>
                  <p>
                    <strong>Get a Sora 2 Video URL:</strong> Copy the URL from sora.openai.com when you view a generated video
                  </p>
                </div>
                <div className="flex items-start space-x-3">
                  <span className="flex-shrink-0 w-6 h-6 bg-blue-100 dark:bg-blue-900 text-blue-600 dark:text-blue-400 rounded-full flex items-center justify-center text-sm font-bold">2</span>
                  <p>
                    <strong>Test the URL:</strong> Click the "Test" button to see what video formats are available and if watermark removal is possible
                  </p>
                </div>
                <div className="flex items-start space-x-3">
                  <span className="flex-shrink-0 w-6 h-6 bg-blue-100 dark:bg-blue-900 text-blue-600 dark:text-blue-400 rounded-full flex items-center justify-center text-sm font-bold">3</span>
                  <p>
                    <strong>Download:</strong> Choose your preferred quality and click "Download Without Watermark" to get your clean video
                  </p>
                </div>
              </div>
            </div>
          </div>

          {/* Features */}
          <div className="max-w-4xl mx-auto">
            <div className="bg-white dark:bg-gray-800 rounded-xl shadow-lg p-6 md:p-8">
              <h2 className="text-2xl font-bold text-gray-900 dark:text-white mb-4">
                ✨ Features
              </h2>
              <div className="grid md:grid-cols-2 gap-6">
                <div className="space-y-3">
                  <div className="flex items-center space-x-3">
                    <span className="text-green-500">✓</span>
                    <span className="text-gray-600 dark:text-gray-400">Watermark removal</span>
                  </div>
                  <div className="flex items-center space-x-3">
                    <span className="text-green-500">✓</span>
                    <span className="text-gray-600 dark:text-gray-400">Multiple quality options</span>
                  </div>
                  <div className="flex items-center space-x-3">
                    <span className="text-green-500">✓</span>
                    <span className="text-gray-600 dark:text-gray-400">Format testing</span>
                  </div>
                </div>
                <div className="space-y-3">
                  <div className="flex items-center space-x-3">
                    <span className="text-green-500">✓</span>
                    <span className="text-gray-600 dark:text-gray-400">Batch processing</span>
                  </div>
                  <div className="flex items-center space-x-3">
                    <span className="text-green-500">✓</span>
                    <span className="text-gray-600 dark:text-gray-400">High-quality output</span>
                  </div>
                  <div className="flex items-center space-x-3">
                    <span className="text-green-500">✓</span>
                    <span className="text-gray-600 dark:text-gray-400">Fast processing</span>
                  </div>
                </div>
              </div>
            </div>
          </div>

          {/* Important Notes */}
          <div className="max-w-4xl mx-auto">
            <div className="bg-yellow-50 dark:bg-yellow-900/20 border border-yellow-200 dark:border-yellow-800 rounded-xl p-6 md:p-8">
              <h2 className="text-xl font-bold text-yellow-800 dark:text-yellow-200 mb-3">
                ⚠️ Important Notes
              </h2>
              <div className="space-y-2 text-yellow-700 dark:text-yellow-300">
                <p>• This tool is for testing and educational purposes</p>
                <p>• Ensure you have rights to download and use the content</p>
                <p>• Respect OpenAI's terms of service and content policies</p>
                <p>• Some videos may not be downloadable due to restrictions</p>
                <p>• Always check platform policies before reposting content</p>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
