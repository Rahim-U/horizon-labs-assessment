/**
 * Empty state component for when there are no tasks
 */

import { Button } from "@/components/ui/button";
import { CheckSquare, Plus } from "lucide-react";

interface EmptyStateProps {
  onCreateTask?: () => void;
  filtered?: boolean;
}

export const EmptyState = ({ onCreateTask, filtered = false }: EmptyStateProps) => {
  return (
    <div className="flex min-h-[400px] flex-col items-center justify-center rounded-lg border-2 border-dashed border-border p-8 text-center">
      <div className="mx-auto flex h-20 w-20 items-center justify-center rounded-full bg-muted">
        <CheckSquare className="h-10 w-10 text-muted-foreground" />
      </div>

      <h3 className="mt-6 text-lg font-semibold">
        {filtered ? "No tasks match your filters" : "No tasks yet"}
      </h3>

      <p className="mt-2 max-w-sm text-sm text-muted-foreground">
        {filtered
          ? "Try adjusting your filters to see more tasks."
          : "Get started by creating your first task to stay organized and productive."}
      </p>

      {!filtered && onCreateTask && (
        <Button onClick={onCreateTask} className="mt-6">
          <Plus className="mr-2 h-4 w-4" />
          Create Your First Task
        </Button>
      )}
    </div>
  );
};
