'use client';

import React from 'react';
import { Clipboard, Download, CheckCircle } from 'lucide-react';

const Instructions: React.FC = () => {
  return (
    <div className="w-full max-w-3xl mx-auto mt-10">
      <div className="bg-gray-50 dark:bg-gray-900/50 rounded-xl p-6 md:p-8">
        <h2 className="text-xl font-bold text-gray-900 dark:text-white mb-6 text-center">
          How to Download TikTok Videos Without Watermark
        </h2>
        
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
          <div className="bg-white dark:bg-gray-800 p-5 rounded-lg shadow-sm flex flex-col items-center text-center">
            <div className="w-12 h-12 rounded-full bg-teal-100 dark:bg-teal-900/30 flex items-center justify-center mb-4">
              <Clipboard className="w-6 h-6 text-teal-600 dark:text-teal-400" />
            </div>
            <h3 className="font-medium text-gray-900 dark:text-white mb-2">Step 1: Copy URL</h3>
            <p className="text-sm text-gray-600 dark:text-gray-400">
              Open TikTok app or website and copy the link to the video you want to download
            </p>
          </div>
          
          <div className="bg-white dark:bg-gray-800 p-5 rounded-lg shadow-sm flex flex-col items-center text-center">
            <div className="w-12 h-12 rounded-full bg-purple-100 dark:bg-purple-900/30 flex items-center justify-center mb-4">
              <CheckCircle className="w-6 h-6 text-purple-600 dark:text-purple-400" />
            </div>
            <h3 className="font-medium text-gray-900 dark:text-white mb-2">Step 2: Paste URL</h3>
            <p className="text-sm text-gray-600 dark:text-gray-400">
              Paste the copied TikTok video URL into the input field above
            </p>
          </div>
          
          <div className="bg-white dark:bg-gray-800 p-5 rounded-lg shadow-sm flex flex-col items-center text-center">
            <div className="w-12 h-12 rounded-full bg-blue-100 dark:bg-blue-900/30 flex items-center justify-center mb-4">
              <Download className="w-6 h-6 text-blue-600 dark:text-blue-400" />
            </div>
            <h3 className="font-medium text-gray-900 dark:text-white mb-2">Step 3: Download</h3>
            <p className="text-sm text-gray-600 dark:text-gray-400">
              Click the download button and select your preferred video quality
            </p>
          </div>
        </div>
        
        <div className="mt-8 text-center">
          <p className="text-sm text-gray-600 dark:text-gray-400">
            Our service is completely free and doesn&apos;t add any watermarks to your downloaded videos.
            <br />
            The downloads are fast, secure, and maintain the original video quality.
          </p>
        </div>
      </div>
    </div>
  );
};

export default Instructions; 