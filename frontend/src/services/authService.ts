/**
 * Authentication service
 * Handles all authentication-related API calls
 */

import apiClient from "@/utils/api";
import { API_ENDPOINTS, STORAGE_KEYS } from "@/utils/constants";
import type { User, LoginCredentials, UserCreate, Token } from "@/types/auth";

/**
 * Register a new user
 */
export const register = async (userData: UserCreate): Promise<{ user: User; token: Token }> => {
  const response = await apiClient.post<{ user: User; token: Token }>(
    API_ENDPOINTS.AUTH.REGISTER,
    userData
  );
  return response.data;
};

/**
 * Login with email and password
 */
export const login = async (credentials: LoginCredentials): Promise<{ user: User; token: Token }> => {
  // Backend expects form data for OAuth2 compatibility
  const formData = new URLSearchParams();
  formData.append("username", credentials.email); // OAuth2 uses 'username' field
  formData.append("password", credentials.password);

  const response = await apiClient.post<{ user: User; token: Token }>(
    API_ENDPOINTS.AUTH.LOGIN,
    formData,
    {
      headers: {
        "Content-Type": "application/x-www-form-urlencoded",
      },
    }
  );

  return response.data;
};

/**
 * Logout (client-side only - clear local storage)
 * SECURITY FIX: Only remove app-specific keys instead of clearing all localStorage
 */
export const logout = (): void => {
  // Only remove app-specific keys to avoid affecting other applications on the same domain
  localStorage.removeItem(STORAGE_KEYS.TOKEN);
  localStorage.removeItem(STORAGE_KEYS.USER);
  // Note: We intentionally keep THEME to preserve user preference
};
