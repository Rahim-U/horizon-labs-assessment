/**
 * API-related type definitions for error handling and responses
 */

/**
 * Standard API error response structure
 */
export interface ApiError {
  detail: string | Record<string, string[]>;
  status?: number;
}

/**
 * Generic API response wrapper
 */
export interface ApiResponse<T> {
  data: T;
  message?: string;
}

/**
 * Pagination metadata for list responses
 */
export interface PaginationMeta {
  total: number;
  limit: number;
  offset: number;
  has_more: boolean;
}

/**
 * Paginated response wrapper
 */
export interface PaginatedResponse<T> {
  data: T[];
  meta: PaginationMeta;
}

/**
 * HTTP methods
 */
export type HttpMethod = "GET" | "POST" | "PUT" | "PATCH" | "DELETE";

/**
 * Request configuration
 */
export interface RequestConfig {
  method: HttpMethod;
  url: string;
  data?: unknown;
  params?: Record<string, unknown>;
  headers?: Record<string, string>;
}
