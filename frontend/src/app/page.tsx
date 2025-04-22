'use client';

import { useState } from 'react';
import { Toaster } from 'react-hot-toast';
import DownloadForm from '@/components/DownloadForm';
import DownloadProgress from '@/components/DownloadProgress';

export default function Home() {
  const [activeDownloads, setActiveDownloads] = useState<string[]>([]);

  const handleDownloadStart = (sessionId: string) => {
    setActiveDownloads((prev) => [...prev, sessionId]);
  };

  const handleDownloadComplete = (sessionId: string) => {
    setActiveDownloads((prev) => prev.filter((id) => id !== sessionId));
  };

  return (
    <main className="min-h-screen bg-gray-50">
      <Toaster position="top-right" />
      
      <div className="max-w-7xl mx-auto py-12 px-4 sm:px-6 lg:px-8">
        <div className="text-center mb-12">
          <h1 className="text-4xl font-bold text-gray-900 mb-4">
            Social Media Video Downloader
          </h1>
          <p className="text-lg text-gray-600">
            Download videos from TikTok, Instagram, and YouTube
          </p>
        </div>

        <DownloadForm onDownloadStart={handleDownloadStart} />

        <div className="mt-8 space-y-4">
          {activeDownloads.map((sessionId) => (
            <DownloadProgress
              key={sessionId}
              sessionId={sessionId}
              onComplete={() => handleDownloadComplete(sessionId)}
            />
          ))}
        </div>
      </div>
    </main>
  );
}
