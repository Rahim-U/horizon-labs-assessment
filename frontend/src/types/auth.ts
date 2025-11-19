/**
 * Authentication-related type definitions
 */

/**
 * User entity representing an authenticated user
 */
export interface User {
  id: number;
  email: string;
  username: string;
  created_at: string;
  updated_at: string;
}

/**
 * Credentials required for user login
 */
export interface LoginCredentials {
  email: string;
  password: string;
}

/**
 * Data required for user registration
 */
export interface UserCreate {
  email: string;
  username: string;
  password: string;
}

/**
 * Authentication token response from the server
 */
export interface Token {
  access_token: string;
  token_type: string;
}

/**
 * Complete authentication response including user data
 */
export interface AuthResponse {
  user: User;
  token: Token;
}
