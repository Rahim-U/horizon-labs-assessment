/**
 * API client configuration with Axios
 * Handles request/response interceptors, authentication, and error transformation
 */

import axios, { AxiosError, type AxiosInstance, type InternalAxiosRequestConfig } from "axios";
import { API_BASE_URL, STORAGE_KEYS } from "./constants";
import type { ApiError } from "@/types/api";

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
 * Request interceptor - Add JWT token to requests
 */
apiClient.interceptors.request.use(
  (config: InternalAxiosRequestConfig) => {
    // Get token from localStorage
    const token = localStorage.getItem(STORAGE_KEYS.TOKEN);

    if (token && config.headers) {
      config.headers.Authorization = `Bearer ${token}`;
    }

    return config;
  },
  (error: AxiosError) => {
    return Promise.reject(error);
  }
);

/**
 * Response interceptor - Handle errors and transform responses
 */
apiClient.interceptors.response.use(
  (response) => {
    // Return the response data directly for successful requests
    return response;
  },
  (error: AxiosError<ApiError>) => {
    // Handle different error scenarios
    if (error.response) {
      // Server responded with error status
      const apiError: ApiError = {
        detail: error.response.data?.detail || "An unexpected error occurred",
        status: error.response.status,
      };

      // Handle 401 Unauthorized - clear auth data
      if (error.response.status === 401) {
        localStorage.removeItem(STORAGE_KEYS.TOKEN);
        localStorage.removeItem(STORAGE_KEYS.USER);

        // Redirect to login if not already there
        if (!window.location.pathname.includes("/login")) {
          window.location.href = "/login";
        }
      }

      // Handle 403 Forbidden
      if (error.response.status === 403) {
        apiError.detail = "You don't have permission to perform this action";
      }

      // Handle 404 Not Found
      if (error.response.status === 404) {
        apiError.detail = "The requested resource was not found";
      }

      // Handle 500 Internal Server Error
      if (error.response.status >= 500) {
        apiError.detail = "Server error. Please try again later.";
      }

      return Promise.reject(apiError);
    } else if (error.request) {
      // Request was made but no response received
      const networkError: ApiError = {
        detail: "Network error. Please check your connection.",
        status: 0,
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
 * Helper function to format API errors for display
 */
export const formatApiError = (error: ApiError): string => {
  if (typeof error.detail === "string") {
    return error.detail;
  }

  // Handle validation errors (object with field-specific errors)
  if (typeof error.detail === "object") {
    const errors = Object.entries(error.detail)
      .map(([field, messages]) => `${field}: ${messages.join(", ")}`)
      .join("; ");
    return errors || "Validation error occurred";
  }

  return "An unexpected error occurred";
};

export default apiClient;
