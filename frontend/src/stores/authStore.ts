/**
 * Authentication store using Zustand
 * Manages user authentication state with localStorage persistence
 */

import { create } from "zustand";
import { persist } from "zustand/middleware";
import * as authService from "@/services/authService";
import { STORAGE_KEYS } from "@/utils/constants";
import type { User, LoginCredentials, UserCreate, Token } from "@/types/auth";
import type { ApiError } from "@/types/api";

interface AuthState {
  // State
  user: User | null;
  token: Token | null;
  isAuthenticated: boolean;
  loading: boolean;
  error: string | null;

  // Actions
  login: (credentials: LoginCredentials) => Promise<void>;
  register: (userData: UserCreate) => Promise<void>;
  logout: () => void;
  clearError: () => void;
  initializeAuth: () => Promise<void>;
}

/**
 * Authentication store
 */
export const useAuthStore = create<AuthState>()(
  persist(
    (set) => ({
      // Initial state
      user: null,
      token: null,
      isAuthenticated: false,
      loading: false,
      error: null,

      /**
       * Login user with credentials
       */
      login: async (credentials: LoginCredentials) => {
        set({ loading: true, error: null });

        try {
          const { user, token } = await authService.login(credentials);

          // Store token in localStorage
          localStorage.setItem(STORAGE_KEYS.TOKEN, token.access_token);

          set({
            user,
            token,
            isAuthenticated: true,
            loading: false,
            error: null,
          });
        } catch (err) {
          const error = err as ApiError;
          set({
            loading: false,
            error: typeof error.detail === "string" ? error.detail : "Login failed",
            isAuthenticated: false,
            user: null,
            token: null,
          });
          throw error;
        }
      },

      /**
       * Register new user
       */
      register: async (userData: UserCreate) => {
        set({ loading: true, error: null });

        try {
          const { user, token } = await authService.register(userData);

          // Store token in localStorage
          localStorage.setItem(STORAGE_KEYS.TOKEN, token.access_token);

          set({
            user,
            token,
            isAuthenticated: true,
            loading: false,
            error: null,
          });
        } catch (err) {
          const error = err as ApiError;
          set({
            loading: false,
            error: typeof error.detail === "string" ? error.detail : "Registration failed",
            isAuthenticated: false,
            user: null,
            token: null,
          });
          throw error;
        }
      },

      /**
       * Logout user and clear state
       */
      logout: () => {
        authService.logout();
        set({
          user: null,
          token: null,
          isAuthenticated: false,
          loading: false,
          error: null,
        });
      },

      /**
       * Clear error state
       */
      clearError: () => {
        set({ error: null });
      },

      /**
       * Initialize auth state from localStorage
       */
      initializeAuth: async () => {
        // The persist middleware automatically restores state from localStorage
        // We just need to validate that we have a token, otherwise clear auth state
        const token = localStorage.getItem(STORAGE_KEYS.TOKEN);

        if (!token) {
          set({ isAuthenticated: false, user: null, token: null });
        }
      },
    }),
    {
      name: STORAGE_KEYS.USER,
      partialize: (state) => ({
        user: state.user,
        token: state.token,
        isAuthenticated: state.isAuthenticated,
      }),
    }
  )
);
