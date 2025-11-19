/**
 * Custom hook for protected routes
 * Redirects to login if user is not authenticated
 */

import { useEffect } from "react";
import { useNavigate } from "react-router-dom";
import { useAuth } from "./useAuth";

export const useProtectedRoute = () => {
  const { isAuthenticated, loading, initializeAuth } = useAuth();
  const navigate = useNavigate();

  useEffect(() => {
    // Initialize auth state from localStorage
    initializeAuth();
  }, [initializeAuth]);

  useEffect(() => {
    // Redirect to login if not authenticated and not loading
    if (!loading && !isAuthenticated) {
      navigate("/login", { replace: true });
    }
  }, [isAuthenticated, loading, navigate]);

  return { isAuthenticated, loading };
};
