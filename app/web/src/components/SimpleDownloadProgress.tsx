'use client';

import React from 'react';
import { Download, Check, AlertCircle } from 'lucide-react';

interface SimpleDownloadProgressProps {
  progress: number;
  status: 'downloading' | 'completed' | 'error';
  error?: string;
}

const SimpleDownloadProgress: React.FC<SimpleDownloadProgressProps> = ({
  progress,
  status,
  error
}) => {
  return (
    <div className="bg-white dark:bg-gray-800 rounded-lg shadow-md p-4 mb-4">
      <div className="flex items-center justify-between mb-2">
        <div className="flex items-center">
          {status === 'completed' ? (
            <div className="w-8 h-8 rounded-full bg-green-100 dark:bg-green-900/20 flex items-center justify-center mr-3">
              <Check className="w-5 h-5 text-green-600 dark:text-green-400" />
            </div>
          ) : status === 'error' ? (
            <div className="w-8 h-8 rounded-full bg-red-100 dark:bg-red-900/20 flex items-center justify-center mr-3">
              <AlertCircle className="w-5 h-5 text-red-600 dark:text-red-400" />
            </div>
          ) : (
            <div className="w-8 h-8 rounded-full bg-blue-100 dark:bg-blue-900/20 flex items-center justify-center mr-3">
              <Download className="w-5 h-5 text-blue-600 dark:text-blue-400" />
            </div>
          )}
          <div>
            <h3 className="text-sm font-medium text-gray-900 dark:text-white">
              {status === 'completed' 
                ? 'Download Complete' 
                : status === 'error'
                  ? 'Download Failed'
                  : 'Downloading Video...'}
            </h3>
            {status === 'downloading' && (
              <p className="text-xs text-gray-500 dark:text-gray-400">
                Please wait while your video is being prepared...
              </p>
            )}
          </div>
        </div>
        <div className="text-sm font-medium">
          {status === 'error' ? '—' : `${progress}%`}
        </div>
      </div>

      {status !== 'error' && (
        <div className="w-full bg-gray-200 dark:bg-gray-700 rounded-full h-2">
          <div 
            className={`h-2 rounded-full transition-all duration-300 ${
              status === 'completed'
                ? 'bg-green-500'
                : 'bg-gradient-to-r from-teal-500 to-purple-500'
            }`}
            style={{ width: `${progress}%` }}
          />
        </div>
      )}

      {error && (
        <div className="mt-2 text-xs text-red-600 dark:text-red-400">
          {error}
        </div>
      )}
    </div>
  );
};

export default SimpleDownloadProgress; 