'use client';

import React from 'react';
import { AlertCircle, X } from 'lucide-react';

interface ErrorMessageProps {
  message: string;
  onDismiss?: () => void;
  type?: 'error' | 'warning' | 'info';
}

const ErrorMessage: React.FC<ErrorMessageProps> = ({
  message,
  onDismiss,
  type = 'error'
}) => {
  const colors = {
    error: {
      bg: 'bg-red-50 dark:bg-red-900/20',
      text: 'text-red-600 dark:text-red-400',
      icon: 'text-red-500 dark:text-red-400'
    },
    warning: {
      bg: 'bg-amber-50 dark:bg-amber-900/20',
      text: 'text-amber-600 dark:text-amber-400',
      icon: 'text-amber-500 dark:text-amber-400'
    },
    info: {
      bg: 'bg-blue-50 dark:bg-blue-900/20',
      text: 'text-blue-600 dark:text-blue-400',
      icon: 'text-blue-500 dark:text-blue-400'
    }
  };

  const colorSet = colors[type];

  return (
    <div className={`${colorSet.bg} rounded-lg p-4 flex items-start shadow-sm mb-4`}>
      <AlertCircle className={`${colorSet.icon} h-5 w-5 mt-0.5 mr-3 flex-shrink-0`} />
      <p className={`${colorSet.text} text-sm flex-grow`}>{message}</p>
      {onDismiss && (
        <button
          onClick={onDismiss}
          className={`${colorSet.text} hover:opacity-70 transition-opacity ml-2`}
          aria-label="Dismiss"
        >
          <X className="h-5 w-5" />
        </button>
      )}
    </div>
  );
};

export default ErrorMessage; 