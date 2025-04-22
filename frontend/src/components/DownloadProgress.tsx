'use client';

import { useEffect, useState } from 'react';
import { DownloadResponse, DownloadStatus } from '@/types/download';
import { getDownloadStatus } from '@/lib/api';

interface DownloadProgressProps {
  sessionId: string;
  onComplete?: () => void;
}

export default function DownloadProgress({ sessionId, onComplete }: DownloadProgressProps) {
  const [downloadStatus, setDownloadStatus] = useState<DownloadResponse | null>(null);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const pollStatus = async () => {
      try {
        const status = await getDownloadStatus(sessionId);
        setDownloadStatus(status);
        
        if (status.status === DownloadStatus.COMPLETED) {
          onComplete?.();
        } else if (status.status === DownloadStatus.FAILED) {
          setError(status.error_message || 'Download failed');
        } else {
          // Continue polling if not completed or failed
          setTimeout(pollStatus, 1000);
        }
      } catch (error) {
        setError('Failed to fetch download status');
        console.error('Status polling error:', error);
      }
    };

    pollStatus();

    return () => {
      // Cleanup timeout on unmount
      setDownloadStatus(null);
      setError(null);
    };
  }, [sessionId, onComplete]);

  if (!downloadStatus) {
    return null;
  }

  const getStatusColor = (status: DownloadStatus) => {
    switch (status) {
      case DownloadStatus.COMPLETED:
        return 'text-green-600';
      case DownloadStatus.FAILED:
        return 'text-red-600';
      case DownloadStatus.PROCESSING:
        return 'text-blue-600';
      default:
        return 'text-gray-600';
    }
  };

  return (
    <div className="mt-4 p-4 bg-white rounded-lg shadow">
      <div className="flex items-center justify-between mb-2">
        <span className="text-sm font-medium text-gray-700">Download Progress</span>
        <span className={`text-sm font-medium ${getStatusColor(downloadStatus.status)}`}>
          {downloadStatus.status}
        </span>
      </div>

      <div className="w-full bg-gray-200 rounded-full h-2.5">
        <div
          className="bg-blue-600 h-2.5 rounded-full transition-all duration-300"
          style={{ width: `${downloadStatus.progress}%` }}
        />
      </div>

      {error && (
        <p className="mt-2 text-sm text-red-600">{error}</p>
      )}

      {downloadStatus.status === DownloadStatus.COMPLETED && downloadStatus.file_path && (
        <a
          href={`/downloads/${downloadStatus.file_path.split('/').pop()}`}
          download
          className="mt-4 inline-flex items-center px-4 py-2 border border-transparent text-sm font-medium rounded-md shadow-sm text-white bg-indigo-600 hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500"
        >
          Download File
        </a>
      )}
    </div>
  );
} 