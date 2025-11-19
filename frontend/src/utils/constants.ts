/**
 * Application constants and configuration
 */

/**
 * API base URL - can be overridden by environment variable
 */
export const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || "http://localhost:8000";

/**
 * API endpoints
 */
export const API_ENDPOINTS = {
  // Auth endpoints
  AUTH: {
    REGISTER: "/auth/register",
    LOGIN: "/auth/login",
  },
  // Task endpoints
  TASKS: {
    BASE: "/tasks",
    BY_ID: (id: number) => `/tasks/${id}`,
  },
} as const;

/**
 * Responsive breakpoints matching Tailwind config
 */
export const BREAKPOINTS = {
  sm: 640,
  md: 768,
  lg: 1024,
  xl: 1280,
  "2xl": 1536,
} as const;

/**
 * Local storage keys
 */
export const STORAGE_KEYS = {
  TOKEN: "task_manager_token",
  THEME: "task_manager_theme",
  USER: "task_manager_user",
} as const;

/**
 * Toast notification duration (ms)
 */
export const TOAST_DURATION = 3000;

/**
 * Default pagination limits
 */
export const DEFAULT_PAGE_LIMIT = 50;
