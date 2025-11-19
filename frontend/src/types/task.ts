/**
 * Task-related type definitions matching backend schemas
 */

/**
 * Task status enumeration
 */
export const TaskStatus = {
  PENDING: "pending",
  IN_PROGRESS: "in-progress",
  COMPLETED: "completed",
} as const;

export type TaskStatus = (typeof TaskStatus)[keyof typeof TaskStatus];

/**
 * Task priority enumeration
 */
export const TaskPriority = {
  LOW: "low",
  MEDIUM: "medium",
  HIGH: "high",
} as const;

export type TaskPriority = (typeof TaskPriority)[keyof typeof TaskPriority];

/**
 * Complete task entity
 */
export interface Task {
  id: number;
  title: string;
  description: string;
  status: TaskStatus;
  priority: TaskPriority;
  due_date: string | null;
  user_id: number;
  created_at: string;
  updated_at: string;
}

/**
 * Data required for creating a new task
 */
export interface TaskCreate {
  title: string;
  description: string;
  status?: TaskStatus;
  priority?: TaskPriority;
  due_date?: string | null;
}

/**
 * Data for updating an existing task
 */
export interface TaskUpdate {
  title?: string;
  description?: string;
  status?: TaskStatus;
  priority?: TaskPriority;
  due_date?: string | null;
}

/**
 * Query parameters for filtering and sorting tasks
 */
export interface TaskQueryParams {
  status?: TaskStatus;
  priority?: TaskPriority;
  search?: string;
  sort_by?: "created_at" | "updated_at" | "due_date" | "title" | "status" | "priority";
  sort_order?: "asc" | "desc";
  limit?: number;
  offset?: number;
}
