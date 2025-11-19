/**
 * Task service
 * Handles all task-related API calls
 */

import apiClient from "@/utils/api";
import { API_ENDPOINTS } from "@/utils/constants";
import type { Task, TaskCreate, TaskUpdate, TaskQueryParams } from "@/types/task";

/**
 * Fetch all tasks with optional filtering and sorting
 */
export const getTasks = async (params?: TaskQueryParams): Promise<Task[]> => {
  const response = await apiClient.get<Task[]>(API_ENDPOINTS.TASKS.BASE, {
    params,
  });
  return response.data;
};

/**
 * Fetch a single task by ID
 */
export const getTask = async (id: number): Promise<Task> => {
  const response = await apiClient.get<Task>(API_ENDPOINTS.TASKS.BY_ID(id));
  return response.data;
};

/**
 * Create a new task
 */
export const createTask = async (taskData: TaskCreate): Promise<Task> => {
  const response = await apiClient.post<Task>(API_ENDPOINTS.TASKS.BASE, taskData);
  return response.data;
};

/**
 * Update an existing task
 */
export const updateTask = async (id: number, taskData: TaskUpdate): Promise<Task> => {
  const response = await apiClient.put<Task>(API_ENDPOINTS.TASKS.BY_ID(id), taskData);
  return response.data;
};

/**
 * Delete a task
 */
export const deleteTask = async (id: number): Promise<void> => {
  await apiClient.delete(API_ENDPOINTS.TASKS.BY_ID(id));
};
