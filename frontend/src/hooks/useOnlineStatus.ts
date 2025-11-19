/**
 * Hook to detect online/offline status
 * Provides real-time updates when network connection changes
 */

import { useState, useEffect } from 'react';
import toast from 'react-hot-toast';

export const useOnlineStatus = () => {
  const [isOnline, setIsOnline] = useState(navigator.onLine);

  useEffect(() => {
    const handleOnline = () => {
      setIsOnline(true);
      toast.success('You are back online', {
        id: 'online-status',
        icon: '🟢',
        duration: 3000,
      });
    };

    const handleOffline = () => {
      setIsOnline(false);
      toast.error('You are offline. Please check your internet connection.', {
        id: 'offline-status',
        icon: '🔴',
        duration: Infinity, // Keep showing until back online
      });
    };

    window.addEventListener('online', handleOnline);
    window.addEventListener('offline', handleOffline);

    return () => {
      window.removeEventListener('online', handleOnline);
      window.removeEventListener('offline', handleOffline);
    };
  }, []);

  return isOnline;
};
