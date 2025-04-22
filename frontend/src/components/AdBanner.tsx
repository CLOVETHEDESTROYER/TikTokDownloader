'use client';

import React from 'react';

interface AdBannerProps {
  location: 'top' | 'bottom' | 'sidebar-top' | 'sidebar-bottom';
  className?: string;
}

const AdBanner: React.FC<AdBannerProps> = ({ location, className = '' }) => {
  return (
    <div className={`bg-white dark:bg-gray-800 rounded-lg overflow-hidden shadow-sm border border-gray-200 dark:border-gray-700 ${className}`}>
      <div className="p-4 flex items-center justify-center h-full min-h-[90px] bg-gray-50 dark:bg-gray-900/50">
        <p className="text-xs text-gray-500 dark:text-gray-400 text-center">
          Ad Space - {location}
          <br />
          <span className="text-teal-600 dark:text-teal-400">(Placeholder for actual ads)</span>
        </p>
      </div>
    </div>
  );
};

export default AdBanner; 