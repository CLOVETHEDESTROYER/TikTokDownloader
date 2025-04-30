'use client';

import React from 'react';
import { Loader2 } from 'lucide-react';

interface ProcessingProgressProps {
  isVisible: boolean;
  stage: 'analyzing' | 'downloading' | 'processing';
}

const ProcessingProgress: React.FC<ProcessingProgressProps> = ({
  isVisible,
  stage
}) => {
  if (!isVisible) return null;

  const stages = {
    analyzing: {
      text: 'Analyzing TikTok URL...',
      progress: 33
    },
    downloading: {
      text: 'Downloading video data...',
      progress: 66
    },
    processing: {
      text: 'Processing video...',
      progress: 90
    }
  };

  const currentStage = stages[stage];

  return (
    <div className="fixed inset-x-0 top-4 mx-auto max-w-sm z-50 transform transition-all duration-300 ease-in-out">
      <div className="bg-white dark:bg-gray-800 rounded-lg shadow-lg p-4 mx-4">
        <div className="flex items-center gap-3 mb-3">
          <div className="w-8 h-8 rounded-full bg-blue-100 dark:bg-blue-900/20 flex items-center justify-center">
            <Loader2 className="w-5 h-5 text-blue-600 dark:text-blue-400 animate-spin" />
          </div>
          <div>
            <h3 className="text-sm font-medium text-gray-900 dark:text-white">
              {currentStage.text}
            </h3>
            <p className="text-xs text-gray-500 dark:text-gray-400">
              Please wait while we process your video...
            </p>
          </div>
        </div>
        
        <div className="w-full bg-gray-200 dark:bg-gray-700 rounded-full h-2">
          <div 
            className="bg-gradient-to-r from-blue-500 to-purple-500 h-2 rounded-full transition-all duration-500"
            style={{ width: `${currentStage.progress}%` }}
          />
        </div>
      </div>
    </div>
  );
};

export default ProcessingProgress; 