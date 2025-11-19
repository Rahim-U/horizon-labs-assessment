/**
 * Task store using Zustand
 * Manages task state with filtering, sorting, and CRUD operations
 */

import { create } from "zustand";
import * as taskService from "@/services/taskService";
import type { Task, TaskCreate, TaskUpdate, TaskStatus, TaskPriority } from "@/types/task";
import type { ApiError } from "@/types/api";

interface TaskFilters {
  status?: TaskStatus;
  priority?: TaskPriority;
  search?: string;
}

interface TaskSorting {
  sortBy: "created_at" | "updated_at" | "due_date" | "title" | "status" | "priority";
  sortOrder: "asc" | "desc";
}

interface TaskState {
  // State
  tasks: Task[];
  filters: TaskFilters;
  sorting: TaskSorting;
  loading: boolean;
  error: string | null;

  // Actions
  fetchTasks: () => Promise<void>;
  createTask: (taskData: TaskCreate) => Promise<Task>;
  updateTask: (id: number, taskData: TaskUpdate) => Promise<Task>;
  deleteTask: (id: number) => Promise<void>;
  setFilters: (filters: TaskFilters) => void;
  setSorting: (sorting: Partial<TaskSorting>) => void;
  clearError: () => void;
  resetFilters: () => void;
}

/**
 * Task store
 */
export const useTaskStore = create<TaskState>((set, get) => ({
  // Initial state
  tasks: [],
  filters: {},
  sorting: {
    sortBy: "created_at",
    sortOrder: "desc",
  },
  loading: false,
  error: null,

  /**
   * Fetch all tasks with current filters and sorting
   */
  fetchTasks: async () => {
    set({ loading: true, error: null });

    try {
      const { filters, sorting } = get();

      const tasks = await taskService.getTasks({
        status: filters.status,
        priority: filters.priority,
        search: filters.search,
        sort_by: sorting.sortBy,
        sort_order: sorting.sortOrder,
      });

      set({ tasks, loading: false, error: null });
    } catch (err) {
      const error = err as ApiError;
      set({
        loading: false,
        error: typeof error.detail === "string" ? error.detail : "Failed to fetch tasks",
      });
      throw error;
    }
  },

  /**
   * Create a new task
   */
  createTask: async (taskData: TaskCreate) => {
    set({ loading: true, error: null });

    try {
      const newTask = await taskService.createTask(taskData);

      // Add new task to the list
      set((state) => ({
        tasks: [newTask, ...state.tasks],
        loading: false,
        error: null,
      }));

      return newTask;
    } catch (err) {
      const error = err as ApiError;
      set({
        loading: false,
        error: typeof error.detail === "string" ? error.detail : "Failed to create task",
      });
      throw error;
    }
  },

  /**
   * Update an existing task
   */
  updateTask: async (id: number, taskData: TaskUpdate) => {
    set({ loading: true, error: null });

    try {
      const updatedTask = await taskService.updateTask(id, taskData);

      // Update task in the list
      set((state) => ({
        tasks: state.tasks.map((task) => (task.id === id ? updatedTask : task)),
        loading: false,
        error: null,
      }));

      return updatedTask;
    } catch (err) {
      const error = err as ApiError;
      set({
        loading: false,
        error: typeof error.detail === "string" ? error.detail : "Failed to update task",
      });
      throw error;
    }
  },

  /**
   * Delete a task
   */
  deleteTask: async (id: number) => {
    set({ loading: true, error: null });

    try {
      await taskService.deleteTask(id);

      // Remove task from the list
      set((state) => ({
        tasks: state.tasks.filter((task) => task.id !== id),
        loading: false,
        error: null,
      }));
    } catch (err) {
      const error = err as ApiError;
      set({
        loading: false,
        error: typeof error.detail === "string" ? error.detail : "Failed to delete task",
      });
      throw error;
    }
  },

  /**
   * Set task filters
   */
  setFilters: (filters: TaskFilters) => {
    set({ filters });
    // Automatically refetch tasks with new filters
    get().fetchTasks();
  },

  /**
   * Set task sorting
   */
  setSorting: (sorting: Partial<TaskSorting>) => {
    set((state) => ({
      sorting: { ...state.sorting, ...sorting },
    }));
    // Automatically refetch tasks with new sorting
    get().fetchTasks();
  },

  /**
   * Clear error state
   */
  clearError: () => {
    set({ error: null });
  },

  /**
   * Reset filters to default
   */
  resetFilters: () => {
    set({ filters: {} });
    get().fetchTasks();
  },
}));
