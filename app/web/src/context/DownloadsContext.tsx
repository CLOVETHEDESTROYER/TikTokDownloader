'use client';

import React, { createContext, useContext, useState, useEffect } from 'react';

export interface Download {
  id: string;
  url: string;
  timestamp: string;
  thumbnail?: string;
  title?: string;
}

interface DownloadsContextType {
  downloads: Download[];
  addDownload: (download: Download) => void;
  clearDownloads: () => void;
}

const DownloadsContext = createContext<DownloadsContextType>({
  downloads: [],
  addDownload: () => {},
  clearDownloads: () => {},
});

export const useDownloads = () => useContext(DownloadsContext);

export const DownloadsProvider: React.FC<{ children: React.ReactNode }> = ({ children }) => {
  const [downloads, setDownloads] = useState<Download[]>([]);

  // Load downloads from localStorage on mount
  useEffect(() => {
    try {
      const savedDownloads = localStorage.getItem('recentDownloads');
      if (savedDownloads) {
        setDownloads(JSON.parse(savedDownloads));
      }
    } catch (error) {
      console.error('Error loading downloads from localStorage:', error);
    }
  }, []);

  // Save downloads to localStorage whenever they change
  useEffect(() => {
    try {
      localStorage.setItem('recentDownloads', JSON.stringify(downloads));
    } catch (error) {
      console.error('Error saving downloads to localStorage:', error);
    }
  }, [downloads]);

  const addDownload = (download: Download) => {
    setDownloads((prevDownloads) => {
      // Limit to 10 most recent downloads
      const updatedDownloads = [download, ...prevDownloads].slice(0, 10);
      return updatedDownloads;
    });
  };

  const clearDownloads = () => {
    setDownloads([]);
  };

  return (
    <DownloadsContext.Provider value={{ downloads, addDownload, clearDownloads }}>
      {children}
    </DownloadsContext.Provider>
  );
}; 