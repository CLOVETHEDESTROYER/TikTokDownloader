'use client';

import React from 'react';
import { Download, Clock, Trash, ExternalLink } from 'lucide-react';
import { useDownloads } from '@/context/DownloadsContext';

const RecentDownloads: React.FC = () => {
  const { downloads, clearDownloads } = useDownloads();

  if (downloads.length === 0) return null;

  // Format date to a readable format
  const formatDate = (dateStr: string) => {
    const date = new Date(dateStr);
    return new Intl.DateTimeFormat('en-US', {
      month: 'short',
      day: 'numeric',
      hour: '2-digit',
      minute: '2-digit',
    }).format(date);
  };

  // Extract domain from URL
  const extractDomain = (url: string): string => {
    try {
      const hostname = new URL(url).hostname;
      if (hostname.includes('tiktok')) return 'TikTok';
      if (hostname.includes('instagram')) return 'Instagram';
      if (hostname.includes('youtube')) return 'YouTube';
      return hostname;
    } catch {
      return 'Unknown';
    }
  };

  return (
    <div className="bg-white dark:bg-gray-800 rounded-xl shadow-lg overflow-hidden">
      <div className="p-6">
        <div className="flex items-center justify-between mb-4">
          <h2 className="text-xl font-bold text-gray-900 dark:text-white flex items-center">
            <Clock className="mr-2 h-5 w-5 text-teal-600 dark:text-teal-400" />
            Recent Downloads
          </h2>
          
          <button 
            onClick={clearDownloads}
            className="flex items-center text-sm text-red-500 hover:text-red-600 dark:text-red-400 dark:hover:text-red-300 transition"
          >
            <Trash className="mr-1 h-4 w-4" />
            Clear All
          </button>
        </div>
        
        <div className="space-y-3">
          {downloads.map((item) => (
            <div 
              key={item.id} 
              className="flex items-center gap-3 p-3 rounded-lg bg-gray-50 dark:bg-gray-900/50 hover:bg-gray-100 dark:hover:bg-gray-900/80 transition"
            >
              <div className="flex-shrink-0 w-10 h-10 rounded-md overflow-hidden bg-gray-200 dark:bg-gray-700">
                {item.thumbnail ? (
                  <img src={item.thumbnail} alt="" className="w-full h-full object-cover" />
                ) : (
                  <div className="w-full h-full flex items-center justify-center bg-teal-100 dark:bg-teal-900/30">
                    <Download className="h-5 w-5 text-teal-600 dark:text-teal-400" />
                  </div>
                )}
              </div>
              
              <div className="flex-1 min-w-0">
                <p className="text-sm font-medium text-gray-900 dark:text-white truncate">
                  {item.title || extractDomain(item.url)}
                </p>
                <div className="flex items-center text-xs text-gray-500 dark:text-gray-400">
                  <span>{formatDate(item.timestamp)}</span>
                  <span className="mx-1">•</span>
                  <span>{extractDomain(item.url)}</span>
                </div>
              </div>
              
              <a 
                href={item.url} 
                target="_blank" 
                rel="noopener noreferrer"
                className="flex-shrink-0 p-1 text-gray-500 hover:text-teal-600 dark:text-gray-400 dark:hover:text-teal-400 transition"
              >
                <ExternalLink className="h-4 w-4" />
              </a>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
};

export default RecentDownloads; 