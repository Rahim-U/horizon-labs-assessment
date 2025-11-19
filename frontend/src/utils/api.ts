/**
 * API client configuration with Axios
 * Handles request/response interceptors, authentication, error transformation,
 * retry logic, request cancellation, and offline detection
 *
 * IMPROVEMENTS:
 * - Replaced hard redirects with custom events for React Router
 * - Added retry logic with exponential backoff
 * - Added offline detection and handling
 * - Added request cancellation support
 * - Fixed localStorage to only remove app-specific keys
 */

import axios, { AxiosError, type AxiosInstance, type InternalAxiosRequestConfig, type AxiosResponse } from "axios";
import { API_BASE_URL, STORAGE_KEYS } from "./constants";
import type { ApiError } from "@/types/api";

// Retry configuration
const MAX_RETRIES = 3;
const INITIAL_RETRY_DELAY = 1000; // 1 second
const MAX_RETRY_DELAY = 10000; // 10 seconds

// Track request cancellation tokens
const pendingRequests = new Map<string, AbortController>();

/**
 * Generate a unique key for a request
 */
const getRequestKey = (config: InternalAxiosRequestConfig): string => {
  return `${config.method}:${config.url}`;
};

/**
 * Exponential backoff delay calculation
 */
const getRetryDelay = (retryCount: number): number => {
  const delay = Math.min(INITIAL_RETRY_DELAY * Math.pow(2, retryCount), MAX_RETRY_DELAY);
  // Add some randomness to prevent thundering herd
  return delay + Math.random() * 1000;
};

/**
 * Check if error is retryable
 */
const isRetryableError = (error: AxiosError): boolean => {
  if (!error.response) {
    // Network errors are retryable
    return true;
  }

  const status = error.response.status;
  // Retry on 5xx errors and 429 (rate limit)
  return status >= 500 || status === 429;
};

/**
 * Check if user is online
 */
export const isOnline = (): boolean => {
  return navigator.onLine;
};

/**
 * Create and configure Axios instance
 */
const apiClient: AxiosInstance = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    "Content-Type": "application/json",
  },
  timeout: 30000, // 30 seconds
});

/**
 * Request interceptor - Add JWT token and setup cancellation
 */
apiClient.interceptors.request.use(
  (config: InternalAxiosRequestConfig) => {
    // Check if offline
    if (!isOnline()) {
      return Promise.reject({
        detail: "You are currently offline. Please check your internet connection.",
        status: 0,
        isOffline: true,
      } as ApiError);
    }

    // Get token from localStorage
    const token = localStorage.getItem(STORAGE_KEYS.TOKEN);

    if (token && config.headers) {
      config.headers.Authorization = `Bearer ${token}`;
    }

    // Setup cancellation for this request
    const requestKey = getRequestKey(config);

    // Cancel previous request with same key if exists
    if (pendingRequests.has(requestKey)) {
      const controller = pendingRequests.get(requestKey);
      controller?.abort();
    }

    // Create new abort controller for this request
    const controller = new AbortController();
    config.signal = controller.signal;
    pendingRequests.set(requestKey, controller);

    return config;
  },
  (error: AxiosError) => {
    return Promise.reject(error);
  }
);

/**
 * Response interceptor - Handle errors, transform responses, and implement retry logic
 */
apiClient.interceptors.response.use(
  (response: AxiosResponse) => {
    // Clear the pending request
    const requestKey = getRequestKey(response.config);
    pendingRequests.delete(requestKey);

    return response;
  },
  async (error: AxiosError<ApiError>) => {
    const config = error.config as InternalAxiosRequestConfig & { _retryCount?: number };

    // Clear the pending request
    if (config) {
      const requestKey = getRequestKey(config);
      pendingRequests.delete(requestKey);
    }

    // Handle request cancellation
    if (axios.isCancel(error)) {
      return Promise.reject({
        detail: "Request was cancelled",
        status: 0,
        isCancelled: true,
      } as ApiError);
    }

    // Implement retry logic
    if (config && isRetryableError(error)) {
      config._retryCount = config._retryCount || 0;

      if (config._retryCount < MAX_RETRIES) {
        config._retryCount += 1;
        const delay = getRetryDelay(config._retryCount);

        console.log(`Retrying request (${config._retryCount}/${MAX_RETRIES}) after ${delay}ms`);

        await new Promise(resolve => setTimeout(resolve, delay));
        return apiClient(config);
      }
    }

    // Handle different error scenarios
    if (error.response) {
      // Server responded with error status
      const apiError: ApiError = {
        detail: error.response.data?.detail || "An unexpected error occurred",
        status: error.response.status,
      };

      // Handle 401 Unauthorized - dispatch custom event for React Router navigation
      if (error.response.status === 401) {
        // Only remove app-specific keys
        localStorage.removeItem(STORAGE_KEYS.TOKEN);
        localStorage.removeItem(STORAGE_KEYS.USER);

        // Dispatch custom event instead of hard redirect
        // This will be handled by the App component
        window.dispatchEvent(new CustomEvent('auth:logout'));
      }

      // Handle 403 Forbidden
      if (error.response.status === 403) {
        apiError.detail = "You don't have permission to perform this action";
      }

      // Handle 404 Not Found
      if (error.response.status === 404) {
        apiError.detail = "The requested resource was not found";
      }

      // Handle 429 Rate Limit
      if (error.response.status === 429) {
        apiError.detail = "Too many requests. Please slow down.";
      }

      // Handle 500 Internal Server Error
      if (error.response.status >= 500) {
        apiError.detail = "Server error. Please try again later.";
      }

      return Promise.reject(apiError);
    } else if (error.request) {
      // Request was made but no response received
      const networkError: ApiError = {
        detail: isOnline()
          ? "Network error. Please check your connection."
          : "You are offline. Please check your internet connection.",
        status: 0,
        isOffline: !isOnline(),
      };
      return Promise.reject(networkError);
    } else {
      // Something else happened
      const unknownError: ApiError = {
        detail: error.message || "An unexpected error occurred",
      };
      return Promise.reject(unknownError);
    }
  }
);

/**
 * Cancel all pending requests
 */
export const cancelAllRequests = (): void => {
  pendingRequests.forEach((controller) => {
    controller.abort();
  });
  pendingRequests.clear();
};

/**
 * Cancel specific request by key
 */
export const cancelRequest = (method: string, url: string): void => {
  const key = `${method}:${url}`;
  const controller = pendingRequests.get(key);
  if (controller) {
    controller.abort();
    pendingRequests.delete(key);
  }
};

/**
 * Helper function to format API errors for display
 */
export const formatApiError = (error: ApiError): string => {
  if (typeof error.detail === "string") {
    return error.detail;
  }

  // Handle validation errors (object with field-specific errors)
  if (typeof error.detail === "object") {
    const errors = Object.entries(error.detail)
      .map(([field, messages]) => `${field}: ${Array.isArray(messages) ? messages.join(", ") : messages}`)
      .join("; ");
    return errors || "Validation error occurred";
  }

  return "An unexpected error occurred";
};

export default apiClient;
