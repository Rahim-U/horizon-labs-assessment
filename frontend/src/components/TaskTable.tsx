/**
 * Task table component displaying tasks in a table format
 * Memoized for performance optimization
 */

import { memo } from "react";
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import {
  Table,
  TableBody,
  TableCell,
  TableHead,
  TableHeader,
  TableRow,
} from "@/components/ui/table";
import {
  DropdownMenu,
  DropdownMenuContent,
  DropdownMenuItem,
  DropdownMenuTrigger,
} from "@/components/ui/dropdown-menu";
import { MoreVertical, Edit, Trash2, Calendar } from "lucide-react";
import { type Task, TaskStatus, TaskPriority } from "@/types/task";
import { formatRelativeTime, getDueDateStatus, truncateText } from "@/utils/formatters";
import { cn } from "@/lib/utils";

interface TaskTableProps {
  tasks: Task[];
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

const TaskTableComponent = ({ tasks, onEdit, onDelete }: TaskTableProps) => {
  return (
    <div className="rounded-md border overflow-hidden">
      <div className="overflow-x-auto">
        <Table>
        <TableHeader>
          <TableRow>
            <TableHead className="w-[250px]">Title</TableHead>
            <TableHead className="min-w-[200px]">Description</TableHead>
            <TableHead className="w-[120px]">Status</TableHead>
            <TableHead className="w-[100px]">Priority</TableHead>
            <TableHead className="hidden lg:table-cell w-[150px]">Due Date</TableHead>
            <TableHead className="hidden xl:table-cell w-[150px]">Updated</TableHead>
            <TableHead className="w-[70px] text-right">Actions</TableHead>
          </TableRow>
        </TableHeader>
        <TableBody>
          {tasks.length === 0 ? (
            <TableRow>
              <TableCell colSpan={7} className="h-24 text-center">
                No tasks found.
              </TableCell>
            </TableRow>
          ) : (
            tasks.map((task) => {
              const dueDateStatus = getDueDateStatus(task.due_date);

              return (
                <TableRow key={task.id} className="hover:bg-muted/50">
                  <TableCell className="font-medium">
                    <div className="line-clamp-2">{task.title}</div>
                  </TableCell>
                  <TableCell>
                    <div className="line-clamp-2 text-sm text-muted-foreground min-w-[200px]">
                      {truncateText(task.description, 100)}
                    </div>
                  </TableCell>
                  <TableCell>
                    <Badge className={cn("capitalize", getStatusColor(task.status))}>
                      {task.status.replace("-", " ")}
                    </Badge>
                  </TableCell>
                  <TableCell>
                    <Badge className={cn("capitalize", getPriorityColor(task.priority))}>
                      {task.priority}
                    </Badge>
                  </TableCell>
                  <TableCell className="hidden lg:table-cell">
                    {task.due_date ? (
                      <div className="flex items-center gap-2">
                        <Calendar className="h-4 w-4 text-muted-foreground" />
                        <Badge
                          variant={dueDateStatus.variant}
                          className={cn(
                            "text-xs",
                            dueDateStatus.variant === "destructive" && "bg-red-500/10 text-red-700 dark:text-red-400",
                            dueDateStatus.isWarning && "bg-orange-500/10 text-orange-700 dark:text-orange-400"
                          )}
                        >
                          {dueDateStatus.label}
                        </Badge>
                      </div>
                    ) : (
                      <span className="text-sm text-muted-foreground">No due date</span>
                    )}
                  </TableCell>
                  <TableCell className="hidden xl:table-cell text-sm text-muted-foreground">
                    {formatRelativeTime(task.updated_at)}
                  </TableCell>
                  <TableCell className="text-right">
                    <DropdownMenu>
                      <DropdownMenuTrigger asChild>
                        <Button
                          variant="ghost"
                          size="icon"
                          className="h-8 w-8"
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
                  </TableCell>
                </TableRow>
              );
            })
          )}
        </TableBody>
      </Table>
      </div>
    </div>
  );
};

/**
 * Memoized TaskTable component to prevent unnecessary re-renders
 * Only re-renders when tasks, onEdit, or onDelete change
 */
export const TaskTable = memo(TaskTableComponent);
