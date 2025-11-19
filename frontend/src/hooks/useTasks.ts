/**
 * Custom hook for task management
 * Provides convenient access to task store
 */

import { useTaskStore } from "@/stores/taskStore";

export const useTasks = () => {
  const {
    tasks,
    filters,
    sorting,
    loading,
    error,
    fetchTasks,
    createTask,
    updateTask,
    deleteTask,
    setFilters,
    setSorting,
    clearError,
    resetFilters,
  } = useTaskStore();

  return {
    tasks,
    filters,
    sorting,
    loading,
    error,
    fetchTasks,
    createTask,
    updateTask,
    deleteTask,
    setFilters,
    setSorting,
    clearError,
    resetFilters,
  };
};
