/**
 * Task card component displaying task information
 */

import { Card, CardContent, CardFooter, CardHeader, CardTitle } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import {
  DropdownMenu,
  DropdownMenuContent,
  DropdownMenuItem,
  DropdownMenuTrigger,
} from "@/components/ui/dropdown-menu";
import { MoreVertical, Edit, Trash2, Clock, Calendar } from "lucide-react";
import { type Task, TaskStatus, TaskPriority } from "@/types/task";
import { formatRelativeTime, getDueDateStatus, truncateText } from "@/utils/formatters";
import { cn } from "@/lib/utils";

interface TaskCardProps {
  task: Task;
  onEdit: (task: Task) => void;
  onDelete: (task: Task) => void;
}

const getStatusColor = (status: TaskStatus): string => {
  switch (status) {
    case TaskStatus.PENDING:
      return "bg-yellow-500/10 text-yellow-700 dark:text-yellow-400 hover:bg-yellow-500/20";
    case TaskStatus.IN_PROGRESS:
      return "bg-blue-500/10 text-blue-700 dark:text-blue-400 hover:bg-blue-500/20";
    case TaskStatus.COMPLETED:
      return "bg-green-500/10 text-green-700 dark:text-green-400 hover:bg-green-500/20";
    default:
      return "";
  }
};

const getPriorityColor = (priority: TaskPriority): string => {
  switch (priority) {
    case TaskPriority.LOW:
      return "bg-gray-500/10 text-gray-700 dark:text-gray-400 hover:bg-gray-500/20";
    case TaskPriority.MEDIUM:
      return "bg-orange-500/10 text-orange-700 dark:text-orange-400 hover:bg-orange-500/20";
    case TaskPriority.HIGH:
      return "bg-red-500/10 text-red-700 dark:text-red-400 hover:bg-red-500/20";
    default:
      return "";
  }
};

export const TaskCard = ({ task, onEdit, onDelete }: TaskCardProps) => {
  const dueDateStatus = getDueDateStatus(task.due_date);

  return (
    <Card className="transition-shadow hover:shadow-lg">
      <CardHeader className="pb-3">
        <div className="flex items-start justify-between gap-2">
          <CardTitle className="line-clamp-2 text-lg">{task.title}</CardTitle>
          <DropdownMenu>
            <DropdownMenuTrigger asChild>
              <Button
                variant="ghost"
                size="icon"
                className="h-8 w-8 shrink-0"
                aria-label={`Actions for ${task.title}`}
              >
                <MoreVertical className="h-4 w-4" />
              </Button>
            </DropdownMenuTrigger>
            <DropdownMenuContent align="end">
              <DropdownMenuItem onClick={() => onEdit(task)}>
                <Edit className="mr-2 h-4 w-4" />
                Edit
              </DropdownMenuItem>
              <DropdownMenuItem
                onClick={() => onDelete(task)}
                className="text-destructive"
              >
                <Trash2 className="mr-2 h-4 w-4" />
                Delete
              </DropdownMenuItem>
            </DropdownMenuContent>
          </DropdownMenu>
        </div>
      </CardHeader>

      <CardContent className="space-y-3 pb-4">
        {/* Description */}
        <p className="line-clamp-3 text-sm text-muted-foreground">
          {truncateText(task.description, 150)}
        </p>

        {/* Status and Priority badges */}
        <div className="flex flex-wrap gap-2">
          <Badge className={cn("capitalize", getStatusColor(task.status))}>
            {task.status.replace("-", " ")}
          </Badge>
          <Badge className={cn("capitalize", getPriorityColor(task.priority))}>
            {task.priority}
          </Badge>
        </div>

        {/* Due date */}
        {task.due_date && (
          <div className="flex items-center gap-2 text-sm">
            <Calendar className="h-4 w-4 text-muted-foreground" />
            <Badge
              variant={dueDateStatus.variant}
              className={cn(
                dueDateStatus.variant === "destructive" && "bg-red-500/10 text-red-700 dark:text-red-400",
                dueDateStatus.isWarning && "bg-orange-500/10 text-orange-700 dark:text-orange-400"
              )}
            >
              {dueDateStatus.label}
            </Badge>
          </div>
        )}
      </CardContent>

      <CardFooter className="border-t pt-3 text-xs text-muted-foreground">
        <div className="flex items-center gap-1">
          <Clock className="h-3 w-3" />
          <span>Updated {formatRelativeTime(task.updated_at)}</span>
        </div>
      </CardFooter>
    </Card>
  );
};
