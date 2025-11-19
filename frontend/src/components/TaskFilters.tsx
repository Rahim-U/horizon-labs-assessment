/**
 * Inline task filters component for medium/large screens
 * Optimized with useCallback to prevent ESLint warnings and improve performance
 */

import { useState, useEffect, useCallback, useMemo } from "react";
import { Button } from "@/components/ui/button";
import { Label } from "@/components/ui/label";
import { Input } from "@/components/ui/input";
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from "@/components/ui/select";
import { TaskStatus, TaskPriority } from "@/types/task";
import { useTasks } from "@/hooks/useTasks";
import { X, Search } from "lucide-react";

export const TaskFilters = () => {
  const { filters, setFilters, resetFilters, sorting, setSorting } = useTasks();
  const [searchQuery, setSearchQuery] = useState(filters.search || "");

  // Debounce search input
  useEffect(() => {
    const timer = setTimeout(() => {
      setFilters((prevFilters) => ({
        ...prevFilters,
        search: searchQuery || undefined,
      }));
    }, 300);

    return () => clearTimeout(timer);
  }, [searchQuery, setFilters]);

  // Handle Enter key press for immediate search
  const handleSearchKeyDown = useCallback((e: React.KeyboardEvent<HTMLInputElement>) => {
    if (e.key === 'Enter') {
      e.preventDefault();
      setFilters((prevFilters) => ({
        ...prevFilters,
        search: searchQuery || undefined,
      }));
    }
  }, [searchQuery, setFilters]);

  const handleStatusChange = useCallback((value: string) => {
    setFilters((prevFilters) => ({
      ...prevFilters,
      status: value === "all" ? undefined : (value as TaskStatus),
    }));
  }, [setFilters]);

  const handlePriorityChange = useCallback((value: string) => {
    setFilters((prevFilters) => ({
      ...prevFilters,
      priority: value === "all" ? undefined : (value as TaskPriority),
    }));
  }, [setFilters]);

  const handleSortByChange = useCallback((value: string) => {
    setSorting({
      sortBy: value as typeof sorting.sortBy,
    });
  }, [setSorting, sorting.sortBy]);

  const handleSortOrderChange = useCallback((value: string) => {
    setSorting({
      sortOrder: value as "asc" | "desc",
    });
  }, [setSorting]);

  const hasActiveFilters = useMemo(
    () => !!(filters.status || filters.priority || filters.search),
    [filters.status, filters.priority, filters.search]
  );

  return (
    <div className="flex flex-wrap items-end gap-3">
      {/* Search Input */}
      <div className="flex flex-col gap-1.5 min-w-[200px] flex-1 max-w-[300px]">
        <Label htmlFor="search-input" className="text-xs">Search</Label>
        <div className="relative">
          <Search className="absolute left-3 top-1/2 -translate-y-1/2 h-4 w-4 text-muted-foreground" />
          <Input
            id="search-input"
            type="search"
            placeholder="Search tasks..."
            value={searchQuery}
            onChange={(e) => setSearchQuery(e.target.value)}
            onKeyDown={handleSearchKeyDown}
            className="h-9 pl-9"
            title="Press Enter to search immediately"
          />
          {searchQuery && (
            <button
              onClick={() => setSearchQuery("")}
              className="absolute right-2 top-1/2 -translate-y-1/2 p-1 hover:bg-muted rounded"
              aria-label="Clear search"
            >
              <X className="h-3 w-3" />
            </button>
          )}
        </div>
      </div>

      {/* Status Filter */}
      <div className="flex flex-col gap-1.5 min-w-[150px]">
        <Label htmlFor="status-filter" className="text-xs">Status</Label>
        <Select
          value={filters.status || "all"}
          onValueChange={handleStatusChange}
        >
          <SelectTrigger id="status-filter" className="h-9">
            <SelectValue placeholder="All statuses" />
          </SelectTrigger>
          <SelectContent>
            <SelectItem value="all">All Statuses</SelectItem>
            <SelectItem value={TaskStatus.PENDING}>Pending</SelectItem>
            <SelectItem value={TaskStatus.IN_PROGRESS}>In Progress</SelectItem>
            <SelectItem value={TaskStatus.COMPLETED}>Completed</SelectItem>
          </SelectContent>
        </Select>
      </div>

      {/* Priority Filter */}
      <div className="flex flex-col gap-1.5 min-w-[150px]">
        <Label htmlFor="priority-filter" className="text-xs">Priority</Label>
        <Select
          value={filters.priority || "all"}
          onValueChange={handlePriorityChange}
        >
          <SelectTrigger id="priority-filter" className="h-9">
            <SelectValue placeholder="All priorities" />
          </SelectTrigger>
          <SelectContent>
            <SelectItem value="all">All Priorities</SelectItem>
            <SelectItem value={TaskPriority.LOW}>Low</SelectItem>
            <SelectItem value={TaskPriority.MEDIUM}>Medium</SelectItem>
            <SelectItem value={TaskPriority.HIGH}>High</SelectItem>
          </SelectContent>
        </Select>
      </div>

      {/* Sort By */}
      <div className="flex flex-col gap-1.5 min-w-[150px]">
        <Label htmlFor="sort-by" className="text-xs">Sort By</Label>
        <Select value={sorting.sortBy} onValueChange={handleSortByChange}>
          <SelectTrigger id="sort-by" className="h-9">
            <SelectValue />
          </SelectTrigger>
          <SelectContent>
            <SelectItem value="created_at">Created Date</SelectItem>
            <SelectItem value="updated_at">Updated Date</SelectItem>
            <SelectItem value="due_date">Due Date</SelectItem>
            <SelectItem value="title">Title</SelectItem>
            <SelectItem value="status">Status</SelectItem>
            <SelectItem value="priority">Priority</SelectItem>
          </SelectContent>
        </Select>
      </div>

      {/* Sort Order */}
      <div className="flex flex-col gap-1.5 min-w-[120px]">
        <Label htmlFor="sort-order" className="text-xs">Order</Label>
        <Select value={sorting.sortOrder} onValueChange={handleSortOrderChange}>
          <SelectTrigger id="sort-order" className="h-9">
            <SelectValue />
          </SelectTrigger>
          <SelectContent>
            <SelectItem value="asc">Ascending</SelectItem>
            <SelectItem value="desc">Descending</SelectItem>
          </SelectContent>
        </Select>
      </div>

      {/* Reset Filters */}
      {hasActiveFilters && (
        <Button
          variant="outline"
          size="sm"
          onClick={() => {
            resetFilters();
            setSearchQuery("");
          }}
          className="h-9"
        >
          <X className="mr-2 h-4 w-4" />
          Reset
        </Button>
      )}
    </div>
  );
};
