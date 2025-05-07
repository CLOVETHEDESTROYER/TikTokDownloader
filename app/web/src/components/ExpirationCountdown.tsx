'use client';

import React, { useState, useEffect } from 'react';
import { Clock, AlertCircle } from 'lucide-react';

interface ExpirationCountdownProps {
  expiresAt: number;  // Unix timestamp in seconds
  onExpired?: () => void;
  isAlreadyExpired?: boolean;
}

const ExpirationCountdown: React.FC<ExpirationCountdownProps> = ({ 
  expiresAt,
  onExpired,
  isAlreadyExpired = false
}) => {
  const [timeLeft, setTimeLeft] = useState<number>(0);
  const [isExpired, setIsExpired] = useState(isAlreadyExpired);

  useEffect(() => {
    // If already marked as expired, don't start the countdown
    if (isAlreadyExpired) {
      setIsExpired(true);
      return;
    }

    const calculateTimeLeft = () => {
      const now = Math.floor(Date.now() / 1000);
      const difference = expiresAt - now;
      
      if (difference <= 0) {
        setIsExpired(true);
        onExpired?.();
        return 0;
      }
      
      return difference;
    };

    // Initial calculation
    setTimeLeft(calculateTimeLeft());

    // Update every second
    const timer = setInterval(() => {
      const remaining = calculateTimeLeft();
      setTimeLeft(remaining);
      
      if (remaining <= 0) {
        clearInterval(timer);
      }
    }, 1000);

    return () => clearInterval(timer);
  }, [expiresAt, onExpired, isAlreadyExpired]);

  const formatTime = (seconds: number): string => {
    if (seconds <= 0) return '0:00';
    const minutes = Math.floor(seconds / 60);
    const remainingSeconds = seconds % 60;
    return `${minutes}:${remainingSeconds.toString().padStart(2, '0')}`;
  };

  if (isExpired) {
    return (
      <div className="flex items-center text-red-500 dark:text-red-400">
        <AlertCircle className="w-4 h-4 mr-1" />
        <span className="text-sm">Download expired</span>
      </div>
    );
  }

  // Determine urgency color based on time left
  const getTimerColor = () => {
    if (timeLeft < 60) return "text-red-500 dark:text-red-400"; // Less than 1 minute
    if (timeLeft < 120) return "text-orange-500 dark:text-orange-400"; // Less than 2 minutes
    return "text-gray-600 dark:text-gray-400"; // More than 2 minutes
  };

  return (
    <div className={`flex items-center ${getTimerColor()}`}>
      <Clock className="w-4 h-4 mr-1" />
      <span className="text-sm">
        Available for {formatTime(timeLeft)}
      </span>
    </div>
  );
};

export default ExpirationCountdown; 