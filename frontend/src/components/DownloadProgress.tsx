'use client';

import React, { useState, useEffect } from 'react';
import { Download, Check, AlertCircle } from 'lucide-react';
import ExpirationCountdown from './ExpirationCountdown';
import { getDownloadStatus } from '@/utils/api';

interface DownloadProgressProps {
  sessionId: string;
  onComplete: () => void;
  expiresAt?: number;
}

const DownloadProgress: React.FC<DownloadProgressProps> = ({ 
  sessionId,
  onComplete,
  expiresAt
}) => {
  const [progress, setProgress] = useState(0);
  const [status, setStatus] = useState<'pending' | 'processing' | 'completed' | 'error' | 'expired'>('processing');
  const [error, setError] = useState<string | null>(null);

  const handleExpired = () => {
    setStatus('expired');
    setError('Download link has expired. Please request a new download.');
  };

  // Poll for status updates from the API
  useEffect(() => {
    if (status === 'completed' || status === 'expired') return;

    const pollStatus = async () => {
      try {
        // Get real status from API
        const statusData = await getDownloadStatus(sessionId);
        
        console.log('Status update for session', sessionId, ':', statusData);
        
        // Update progress
        setProgress(statusData.progress || 0);
        
        // Update status
        if (statusData.status === 'completed') {
          setStatus('completed');
          onComplete();
        } else if (statusData.status === 'failed') {
          setStatus('error');
          setError(statusData.error || 'Download failed. Please try again.');
        } else if (statusData.status === 'expired') {
          setStatus('expired');
          setError('Download link has expired. Please request a new download.');
        } else {
          // Map the backend status to our component status
          setStatus(
            statusData.status === 'pending' ? 'pending' :
            statusData.status === 'processing' ? 'processing' : 
            'processing'
          );
        }
      } catch (err) {
        console.error('Error checking download status:', err);
        
        // If API call fails, simulate progress in development
        if (process.env.NODE_ENV === 'development') {
          console.log('Simulating progress for development...');
          setProgress((prevProgress) => {
            // Don't go beyond 95% in simulation
            if (prevProgress >= 95) {
              return 95;
            }
            return prevProgress + Math.floor(Math.random() * 10) + 5;
          });
        } else {
          // In production, show error
          setStatus('error');
          setError('Failed to check download status. Please try again.');
        }
      }
    };
    
    // Poll every 2 seconds
    const interval = setInterval(pollStatus, 2000);
    
    // Initial poll
    pollStatus();
    
    return () => clearInterval(interval);
  }, [sessionId, status, onComplete]); // Remove progress from dependency array to prevent rapid updates

  return (
    <div className="bg-white dark:bg-gray-800 rounded-lg shadow-md p-4">
      <div className="flex items-center justify-between mb-2">
        <div className="flex items-center">
          {status === 'completed' ? (
            <div className="w-8 h-8 rounded-full bg-green-100 dark:bg-green-900/20 flex items-center justify-center mr-3">
              <Check className="w-5 h-5 text-green-600 dark:text-green-400" />
            </div>
          ) : status === 'error' || status === 'expired' ? (
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
                  : status === 'expired'
                    ? 'Download Expired'
                    : status === 'pending'
                      ? 'Waiting in Queue...'
                      : 'Downloading Video...'}
            </h3>
            <p className="text-xs text-gray-500 dark:text-gray-400">
              Session ID: {sessionId.substring(0, 8)}...
            </p>
          </div>
        </div>
        <div className="text-sm font-medium">
          {status === 'completed' && expiresAt ? (
            <ExpirationCountdown 
              expiresAt={expiresAt}
              onExpired={handleExpired}
            />
          ) : status === 'completed' 
              ? '100%' 
              : status === 'error' || status === 'expired'
                ? '—' 
                : `${progress}%`}
        </div>
      </div>

      {(status === 'processing' || status === 'pending') && (
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