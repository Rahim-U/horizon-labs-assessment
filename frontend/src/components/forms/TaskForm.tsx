/**
 * Task form component with validation
 * Reusable for both create and edit modes
 */

import { useForm } from "react-hook-form";
import { zodResolver } from "@hookform/resolvers/zod";
import { z } from "zod";
import { format } from "date-fns";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { Textarea } from "@/components/ui/textarea";
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from "@/components/ui/select";
import { Loader2, Calendar as CalendarIcon } from "lucide-react";
import { TaskStatus, TaskPriority, type Task } from "@/types/task";
import { Popover, PopoverContent, PopoverTrigger } from "@/components/ui/popover";
import { Calendar } from "@/components/ui/calendar";
import { cn } from "@/lib/utils";

// Validation schema
const taskSchema = z.object({
  title: z
    .string()
    .min(1, "Title is required")
    .max(200, "Title must be less than 200 characters"),
  description: z.string().min(1, "Description is required"),
  status: z.enum([TaskStatus.PENDING, TaskStatus.IN_PROGRESS, TaskStatus.COMPLETED]),
  priority: z.enum([TaskPriority.LOW, TaskPriority.MEDIUM, TaskPriority.HIGH]),
  due_date: z.string().nullable().optional(),
});

type TaskFormValues = z.infer<typeof taskSchema>;

interface TaskFormProps {
  onSubmit: (data: TaskFormValues) => Promise<void>;
  loading?: boolean;
  initialData?: Task;
  mode?: "create" | "edit";
}

export const TaskForm = ({
  onSubmit,
  loading = false,
  initialData,
  mode = "create",
}: TaskFormProps) => {
  const {
    register,
    handleSubmit,
    formState: { errors },
    setValue,
    watch,
  } = useForm<TaskFormValues>({
    resolver: zodResolver(taskSchema),
    defaultValues: initialData
      ? {
          title: initialData.title,
          description: initialData.description,
          status: initialData.status,
          priority: initialData.priority,
          due_date: initialData.due_date,
        }
      : {
          title: "",
          description: "",
          status: TaskStatus.PENDING,
          priority: TaskPriority.MEDIUM,
          due_date: null,
        },
  });

  const selectedDate = watch("due_date");

  return (
    <form onSubmit={handleSubmit(onSubmit)} className="space-y-4">
      <div className="space-y-2">
        <Label htmlFor="title">Title</Label>
        <Input
          id="title"
          type="text"
          placeholder="Enter task title"
          disabled={loading}
          {...register("title")}
        />
        {errors.title && (
          <p className="text-sm text-destructive">{errors.title.message}</p>
        )}
      </div>

      <div className="space-y-2">
        <Label htmlFor="description">Description</Label>
        <Textarea
          id="description"
          placeholder="Enter task description"
          rows={4}
          disabled={loading}
          {...register("description")}
        />
        {errors.description && (
          <p className="text-sm text-destructive">{errors.description.message}</p>
        )}
      </div>

      <div className="grid grid-cols-1 gap-4 sm:grid-cols-2">
        <div className="space-y-2">
          <Label htmlFor="status">Status</Label>
          <Select
            value={watch("status")}
            onValueChange={(value) => setValue("status", value as TaskStatus)}
            disabled={loading}
          >
            <SelectTrigger id="status">
              <SelectValue placeholder="Select status" />
            </SelectTrigger>
            <SelectContent>
              <SelectItem value={TaskStatus.PENDING}>Pending</SelectItem>
              <SelectItem value={TaskStatus.IN_PROGRESS}>In Progress</SelectItem>
              <SelectItem value={TaskStatus.COMPLETED}>Completed</SelectItem>
            </SelectContent>
          </Select>
          {errors.status && (
            <p className="text-sm text-destructive">{errors.status.message}</p>
          )}
        </div>

        <div className="space-y-2">
          <Label htmlFor="priority">Priority</Label>
          <Select
            value={watch("priority")}
            onValueChange={(value) => setValue("priority", value as TaskPriority)}
            disabled={loading}
          >
            <SelectTrigger id="priority">
              <SelectValue placeholder="Select priority" />
            </SelectTrigger>
            <SelectContent>
              <SelectItem value={TaskPriority.LOW}>Low</SelectItem>
              <SelectItem value={TaskPriority.MEDIUM}>Medium</SelectItem>
              <SelectItem value={TaskPriority.HIGH}>High</SelectItem>
            </SelectContent>
          </Select>
          {errors.priority && (
            <p className="text-sm text-destructive">{errors.priority.message}</p>
          )}
        </div>
      </div>

      <div className="space-y-2">
        <Label>Due Date</Label>
        <Popover>
          <PopoverTrigger asChild>
            <Button
              variant="outline"
              className={cn(
                "w-full justify-start text-left font-normal",
                !selectedDate && "text-muted-foreground"
              )}
              disabled={loading}
            >
              <CalendarIcon className="mr-2 h-4 w-4" />
              {selectedDate ? format(new Date(selectedDate), "PPP") : "Pick a date"}
            </Button>
          </PopoverTrigger>
          <PopoverContent className="w-auto p-0" align="start">
            <Calendar
              mode="single"
              selected={selectedDate ? new Date(selectedDate) : undefined}
              onSelect={(date) => {
                setValue("due_date", date ? date.toISOString() : null);
              }}
              initialFocus
            />
          </PopoverContent>
        </Popover>
        {selectedDate && (
          <Button
            type="button"
            variant="ghost"
            size="sm"
            onClick={() => setValue("due_date", null)}
            disabled={loading}
          >
            Clear date
          </Button>
        )}
      </div>

      <Button type="submit" className="w-full" disabled={loading}>
        {loading ? (
          <>
            <Loader2 className="mr-2 h-4 w-4 animate-spin" />
            {mode === "create" ? "Creating..." : "Updating..."}
          </>
        ) : (
          <>{mode === "create" ? "Create Task" : "Update Task"}</>
        )}
      </Button>
    </form>
  );
};
