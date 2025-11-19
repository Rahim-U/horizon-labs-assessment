/**
 * Custom hook for authentication
 * Provides convenient access to auth store
 */

import { useAuthStore } from "@/stores/authStore";

export const useAuth = () => {
  const {
    user,
    token,
    isAuthenticated,
    loading,
    error,
    login,
    register,
    logout,
    clearError,
    initializeAuth,
  } = useAuthStore();

  return {
    user,
    token,
    isAuthenticated,
    loading,
    error,
    login,
    register,
    logout,
    clearError,
    initializeAuth,
  };
};
