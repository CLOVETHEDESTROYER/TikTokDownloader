'use client';

import React, { useEffect, useRef } from 'react';

interface AdBannerProps {
  location: 'top' | 'bottom' | 'sidebar-top' | 'sidebar-bottom' | 'in-content';
  className?: string;
  adSlot?: string;
  format?: 'auto' | 'horizontal' | 'vertical' | 'rectangle';
}

interface AdsenseWindow extends Window {
  adsbygoogle: unknown[];
}

const AdBanner: React.FC<AdBannerProps> = ({ 
  location, 
  className = '', 
  adSlot,
  format = 'auto'
}) => {
  const adRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    // Only add the ad if we have an adSlot
    if (adSlot && adRef.current && typeof window !== 'undefined') {
      try {
        const adsenseWindow = window as unknown as AdsenseWindow;
        adsenseWindow.adsbygoogle = adsenseWindow.adsbygoogle || [];
        adsenseWindow.adsbygoogle.push({});
      } catch (err) {
        console.error('Error loading advertisement:', err);
      }
    }
  }, [adSlot]);

  // Default sizes for different locations
  const getAdSize = () => {
    switch (location) {
      case 'top':
      case 'bottom':
        return { width: '728px', height: '90px', minHeight: '90px' };
      case 'sidebar-top':
        return { width: '300px', height: '600px', minHeight: '600px' };
      case 'sidebar-bottom':
        return { width: '300px', height: '250px', minHeight: '250px' };
      case 'in-content':
        return { width: '100%', height: 'auto', minHeight: '250px' };
      default:
        return { width: '100%', height: 'auto', minHeight: '90px' };
    }
  };

  if (!adSlot) {
    const size = getAdSize();
    return (
      <div 
        className={`bg-white dark:bg-gray-800 rounded-lg overflow-hidden shadow-sm border border-gray-200 dark:border-gray-700 ${className}`}
        style={{ 
          width: size.width, 
          height: size.height,
          minHeight: size.minHeight
        }}
      >
        <div className="p-4 flex items-center justify-center h-full bg-gray-50 dark:bg-gray-900/50">
          <p className="text-xs text-gray-500 dark:text-gray-400 text-center">
            Advertisement
            <br />
            <span className="text-teal-600 dark:text-teal-400">({location})</span>
          </p>
        </div>
      </div>
    );
  }

  return (
    <div className={`ad-container ${className}`} style={getAdSize()}>
      <ins
        className="adsbygoogle"
        style={{
          display: 'block',
          width: '100%',
          height: '100%',
        }}
        data-ad-client={process.env.NEXT_PUBLIC_ADSENSE_ID}
        data-ad-slot={adSlot}
        data-ad-format={format}
        data-full-width-responsive="true"
      />
    </div>
  );
};

export default AdBanner; 