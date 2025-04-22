'use client';

import { useState } from 'react';
import { Platform, Quality, DownloadRequest } from '@/types/download';
import { downloadVideo } from '@/lib/api';
import toast from 'react-hot-toast';

interface DownloadFormProps {
  onDownloadStart: (sessionId: string) => void;
}

export default function DownloadForm({ onDownloadStart }: DownloadFormProps) {
  const [url, setUrl] = useState('');
  const [platform, setPlatform] = useState<Platform>(Platform.TIKTOK);
  const [quality, setQuality] = useState<Quality>(Quality.HIGH);
  const [isLoading, setIsLoading] = useState(false);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!url.trim()) {
      toast.error('Please enter a valid URL');
      return;
    }

    setIsLoading(true);
    try {
      const request: DownloadRequest = {
        url: url.trim(),
        platform,
        quality,
      };
      const response = await downloadVideo(request);
      onDownloadStart(response.session_id);
      toast.success('Download started!');
      setUrl('');
    } catch (error) {
      toast.error('Failed to start download. Please try again.');
      console.error('Download error:', error);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <form onSubmit={handleSubmit} className="space-y-4 w-full max-w-2xl mx-auto p-6 bg-white rounded-lg shadow-md">
      <div>
        <label htmlFor="url" className="block text-sm font-medium text-gray-700">
          Video URL
        </label>
        <input
          type="url"
          id="url"
          value={url}
          onChange={(e) => setUrl(e.target.value)}
          placeholder="Enter video URL"
          className="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500 sm:text-sm"
          required
        />
      </div>

      <div className="grid grid-cols-2 gap-4">
        <div>
          <label htmlFor="platform" className="block text-sm font-medium text-gray-700">
            Platform
          </label>
          <select
            id="platform"
            value={platform}
            onChange={(e) => setPlatform(e.target.value as Platform)}
            className="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500 sm:text-sm"
          >
            {Object.values(Platform).map((p) => (
              <option key={p} value={p}>
                {p}
              </option>
            ))}
          </select>
        </div>

        <div>
          <label htmlFor="quality" className="block text-sm font-medium text-gray-700">
            Quality
          </label>
          <select
            id="quality"
            value={quality}
            onChange={(e) => setQuality(e.target.value as Quality)}
            className="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500 sm:text-sm"
          >
            {Object.values(Quality).map((q) => (
              <option key={q} value={q}>
                {q}
              </option>
            ))}
          </select>
        </div>
      </div>

      <button
        type="submit"
        disabled={isLoading}
        className={`w-full flex justify-center py-2 px-4 border border-transparent rounded-md shadow-sm text-sm font-medium text-white bg-indigo-600 hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500 ${
          isLoading ? 'opacity-50 cursor-not-allowed' : ''
        }`}
      >
        {isLoading ? 'Starting Download...' : 'Download'}
      </button>
    </form>
  );
} 