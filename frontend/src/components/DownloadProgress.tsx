'use client';

import React, { useState, useEffect } from 'react';
import { Download, Check, AlertCircle } from 'lucide-react';

interface DownloadProgressProps {
  sessionId: string;
  onComplete: () => void;
}

const DownloadProgress: React.FC<DownloadProgressProps> = ({ 
  sessionId,
  onComplete
}) => {
  const [progress, setProgress] = useState(0);
  const [status, setStatus] = useState<'processing' | 'completed' | 'error'>('processing');
  const [error, setError] = useState<string | null>(null);

  // Simulate download progress
  useEffect(() => {
    if (status !== 'processing') return;

    const interval = setInterval(() => {
      setProgress((prevProgress) => {
        if (prevProgress >= 100) {
          clearInterval(interval);
          return 100;
        }
        return prevProgress + 10;
      });
      
      // Check if progress has reached 100 and update status
      if (progress >= 90) {
        setStatus('completed');
        // Call onComplete in the next tick to avoid rendering issues
        setTimeout(() => {
          onComplete();
        }, 0);
        clearInterval(interval);
      }
    }, 500);

    // Simulate random errors (for testing) - uncomment to test error states
    const simulateError = false; // Set to true to test error state
    if (simulateError) {
      clearInterval(interval);
      setStatus('error');
      setError('Download failed. The server might be busy, please try again.');
    }

    return () => clearInterval(interval);
  }, [status, progress, onComplete]);

  return (
    <div className="bg-white dark:bg-gray-800 rounded-lg shadow-md p-4">
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
            <p className="text-xs text-gray-500 dark:text-gray-400">
              Session ID: {sessionId.substring(0, 8)}...
            </p>
          </div>
        </div>
        <div className="text-sm font-medium">
          {status === 'completed' 
            ? '100%' 
            : status === 'error' 
              ? '—' 
              : `${progress}%`}
        </div>
      </div>

      {status === 'processing' && (
        <div className="w-full bg-gray-200 dark:bg-gray-700 rounded-full h-2 mb-2">
          <div 
            className="bg-gradient-to-r from-teal-500 to-purple-500 h-2 rounded-full transition-all duration-300" 
            style={{ width: `${progress}%` }}
          ></div>
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

export default DownloadProgress; 