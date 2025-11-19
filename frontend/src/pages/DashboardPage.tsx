/**
 * Dashboard page component with task management
 * Optimized with useCallback for event handlers
 */

import { useEffect, useState, useCallback } from "react";
import { Button } from "@/components/ui/button";
import { Dialog, DialogContent, DialogHeader, DialogTitle } from "@/components/ui/dialog";
import {
  AlertDialog,
  AlertDialogAction,
  AlertDialogCancel,
  AlertDialogContent,
  AlertDialogDescription,
  AlertDialogFooter,
  AlertDialogHeader,
  AlertDialogTitle,
} from "@/components/ui/alert-dialog";
import { TaskForm } from "@/components/forms/TaskForm";
import { TaskTable } from "@/components/TaskTable";
import { TaskFilters } from "@/components/TaskFilters";
import { EmptyState } from "@/components/EmptyState";
import { TaskTableSkeleton } from "@/components/LoadingSkeleton";
import { Sidebar } from "@/components/layout/Sidebar";
import { Plus } from "lucide-react";
import { useTasks } from "@/hooks/useTasks";
import { useProtectedRoute } from "@/hooks/useProtectedRoute";
import toast from "react-hot-toast";
import type { Task, TaskCreate, TaskUpdate } from "@/types/task";

export const DashboardPage = () => {
  const { isAuthenticated, loading: authLoading } = useProtectedRoute();
  const {
    tasks,
    loading: tasksLoading,
    fetchTasks,
    createTask,
    updateTask,
    deleteTask,
    filters,
  } = useTasks();

  const [isCreateDialogOpen, setIsCreateDialogOpen] = useState(false);
  const [isEditDialogOpen, setIsEditDialogOpen] = useState(false);
  const [isDeleteDialogOpen, setIsDeleteDialogOpen] = useState(false);
  const [selectedTask, setSelectedTask] = useState<Task | null>(null);
  const [isSidebarOpen, setIsSidebarOpen] = useState(false);

  // Fetch tasks on mount
  useEffect(() => {
    if (isAuthenticated && !authLoading) {
      fetchTasks();
    }
  }, [isAuthenticated, authLoading, fetchTasks]);

  // Listen for header menu click event
  useEffect(() => {
    const handleHeaderMenuClick = () => {
      setIsSidebarOpen(true);
    };

    window.addEventListener('toggle-mobile-sidebar', handleHeaderMenuClick);
    return () => {
      window.removeEventListener('toggle-mobile-sidebar', handleHeaderMenuClick);
    };
  }, []);

  const handleCreateTask = useCallback(async (data: TaskCreate) => {
    try {
      await createTask(data);
      toast.success("Task created successfully!");
      setIsCreateDialogOpen(false);
    } catch {
      toast.error("Failed to create task");
    }
  }, [createTask]);

  const handleEditTask = useCallback(async (data: TaskUpdate) => {
    if (!selectedTask) return;

    try {
      await updateTask(selectedTask.id, data);
      toast.success("Task updated successfully!");
      setIsEditDialogOpen(false);
      setSelectedTask(null);
    } catch {
      toast.error("Failed to update task");
    }
  }, [selectedTask, updateTask]);

  const handleDeleteTask = useCallback(async () => {
    if (!selectedTask) return;

    try {
      await deleteTask(selectedTask.id);
      toast.success("Task deleted successfully!");
      setIsDeleteDialogOpen(false);
      setSelectedTask(null);
    } catch {
      toast.error("Failed to delete task");
    }
  }, [selectedTask, deleteTask]);

  const openEditDialog = useCallback((task: Task) => {
    setSelectedTask(task);
    setIsEditDialogOpen(true);
  }, []);

  const openDeleteDialog = useCallback((task: Task) => {
    setSelectedTask(task);
    setIsDeleteDialogOpen(true);
  }, []);

  // Show loading state
  if (authLoading) {
    return null;
  }

  const hasActiveFilters = !!(filters.status || filters.priority || filters.search);

  return (
    <div className="flex min-h-screen flex-col w-full overflow-x-hidden">
      <div className="flex flex-1 relative w-full">
        {/* Sidebar - Mobile Only (Full Screen Overlay) */}
        {isSidebarOpen && (
          <>
            {/* Backdrop */}
            <div
              className="fixed inset-0 bg-black/50 z-40 md:hidden"
              onClick={() => setIsSidebarOpen(false)}
            />
            {/* Sidebar */}
            <div className="fixed inset-0 z-50 md:hidden">
              <Sidebar
                isOpen={isSidebarOpen}
                onClose={() => setIsSidebarOpen(false)}
              />
            </div>
          </>
        )}

        {/* Main Content */}
        <main className="flex-1 w-full min-w-0">
          <div className="container mx-auto p-4 md:p-6 lg:p-8 w-full max-w-full">
            {/* Header */}
            <div className="mb-6">
              <div className="flex flex-col gap-4 sm:flex-row sm:items-center sm:justify-between mb-4">
                <div>
                  <h1 className="text-3xl font-bold">My Tasks</h1>
                  <p className="mt-1 text-muted-foreground">
                    Manage your tasks and stay organized
                  </p>
                </div>
                <div className="flex gap-2">
                  <Button
                    variant="outline"
                    className="md:hidden"
                    onClick={() => setIsSidebarOpen(!isSidebarOpen)}
                    aria-label={isSidebarOpen ? "Hide filters" : "Show filters"}
                  >
                    {isSidebarOpen ? "Hide" : "Show"} Filters
                  </Button>
                  <Button onClick={() => setIsCreateDialogOpen(true)} aria-label="Create new task">
                    <Plus className="mr-2 h-4 w-4" />
                    New Task
                  </Button>
                </div>
              </div>

              {/* Inline Filters - Medium/Large screens only */}
              <div className="hidden md:block">
                <TaskFilters />
              </div>
            </div>

            {/* Task Table */}
            {tasksLoading ? (
              <TaskTableSkeleton />
            ) : tasks.length === 0 ? (
              <EmptyState
                onCreateTask={() => setIsCreateDialogOpen(true)}
                filtered={hasActiveFilters}
              />
            ) : (
              <TaskTable
                tasks={tasks}
                onEdit={openEditDialog}
                onDelete={openDeleteDialog}
              />
            )}
          </div>
        </main>
      </div>

      {/* Create Task Dialog */}
      <Dialog open={isCreateDialogOpen} onOpenChange={setIsCreateDialogOpen}>
        <DialogContent className="max-h-[90vh] overflow-y-auto sm:max-w-[500px]">
          <DialogHeader>
            <DialogTitle>Create New Task</DialogTitle>
          </DialogHeader>
          <TaskForm onSubmit={handleCreateTask} mode="create" />
        </DialogContent>
      </Dialog>

      {/* Edit Task Dialog */}
      <Dialog open={isEditDialogOpen} onOpenChange={setIsEditDialogOpen}>
        <DialogContent className="max-h-[90vh] overflow-y-auto sm:max-w-[500px]">
          <DialogHeader>
            <DialogTitle>Edit Task</DialogTitle>
          </DialogHeader>
          {selectedTask && (
            <TaskForm
              onSubmit={handleEditTask}
              mode="edit"
              initialData={selectedTask}
            />
          )}
        </DialogContent>
      </Dialog>

      {/* Delete Confirmation Dialog */}
      <AlertDialog open={isDeleteDialogOpen} onOpenChange={setIsDeleteDialogOpen}>
        <AlertDialogContent>
          <AlertDialogHeader>
            <AlertDialogTitle>Are you sure?</AlertDialogTitle>
            <AlertDialogDescription>
              This action cannot be undone. This will permanently delete the task
              "{selectedTask?.title}".
            </AlertDialogDescription>
          </AlertDialogHeader>
          <AlertDialogFooter>
            <AlertDialogCancel>Cancel</AlertDialogCancel>
            <AlertDialogAction
              onClick={handleDeleteTask}
              className="bg-destructive text-destructive-foreground hover:bg-destructive/90"
            >
              Delete
            </AlertDialogAction>
          </AlertDialogFooter>
        </AlertDialogContent>
      </AlertDialog>
    </div>
  );
};
