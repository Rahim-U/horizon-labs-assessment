/**
 * Sidebar component with filters
 */

import { useState, useEffect, useRef } from "react";
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
import { Filter, X, Search } from "lucide-react";

interface SidebarProps {
  isOpen?: boolean;
  onClose?: () => void;
}

export const Sidebar = ({ isOpen = true, onClose }: SidebarProps) => {
  const { filters, setFilters, resetFilters, sorting, setSorting } = useTasks();
  const [searchQuery, setSearchQuery] = useState(filters.search || "");
  const filtersRef = useRef(filters);

  // Keep filters ref up to date
  useEffect(() => {
    filtersRef.current = filters;
  }, [filters]);

  // Debounce search input
  useEffect(() => {
    const timer = setTimeout(() => {
      setFilters({
        ...filtersRef.current,
        search: searchQuery || undefined,
      });
    }, 300);

    return () => clearTimeout(timer);
  }, [searchQuery, setFilters]);

  // Handle Enter key press for immediate search
  const handleSearchKeyDown = (e: React.KeyboardEvent<HTMLInputElement>) => {
    if (e.key === 'Enter') {
      e.preventDefault();
      setFilters({
        ...filtersRef.current,
        search: searchQuery || undefined,
      });
      // Close sidebar on mobile after search
      onClose?.();
    }
  };

  const handleStatusChange = (value: string) => {
    setFilters({
      ...filters,
      status: value === "all" ? undefined : (value as TaskStatus),
    });
    // Close sidebar on mobile after filter selection
    onClose?.();
  };

  const handlePriorityChange = (value: string) => {
    setFilters({
      ...filters,
      priority: value === "all" ? undefined : (value as TaskPriority),
    });
    // Close sidebar on mobile after filter selection
    onClose?.();
  };

  const handleSortByChange = (value: string) => {
    setSorting({
      sortBy: value as typeof sorting.sortBy,
    });
    // Close sidebar on mobile after sort selection
    onClose?.();
  };

  const handleSortOrderChange = (value: string) => {
    setSorting({
      sortOrder: value as "asc" | "desc",
    });
    // Close sidebar on mobile after sort selection
    onClose?.();
  };

  if (!isOpen) return null;

  return (
    <aside className="h-full w-full bg-card overflow-y-auto">
      <div className="p-4 sm:p-6 w-full max-w-2xl mx-auto">
        {/* Header */}
        <div className="mb-6 flex items-center justify-between">
          <div className="flex items-center gap-2">
            <Filter className="h-5 w-5 text-muted-foreground" />
            <h2 className="text-lg font-semibold">Filters</h2>
          </div>
          <Button variant="ghost" size="icon" onClick={onClose} aria-label="Close filters sidebar">
            <X className="h-5 w-5" />
          </Button>
        </div>

        <div className="space-y-4">
          {/* Search Input - Full Width */}
          <div className="space-y-2">
            <Label htmlFor="sidebar-search">Search</Label>
            <div className="relative">
              <Search className="absolute left-3 top-1/2 -translate-y-1/2 h-4 w-4 text-muted-foreground" />
              <Input
                id="sidebar-search"
                type="search"
                placeholder="Search tasks (press Enter)..."
                value={searchQuery}
                onChange={(e) => setSearchQuery(e.target.value)}
                onKeyDown={handleSearchKeyDown}
                className="pl-9 [&::-webkit-search-cancel-button]:hidden [&::-webkit-search-decoration]:hidden [&::-ms-clear]:hidden"
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
            <p className="text-xs text-muted-foreground">
              Press Enter to search immediately, or wait for auto-search
            </p>
          </div>

          {/* Filters Grid - 2 columns on tablet and up */}
          <div className="grid grid-cols-1 min-[480px]:grid-cols-2 gap-4">
            {/* Status Filter */}
            <div className="space-y-2">
              <Label htmlFor="status-filter">Status</Label>
              <Select
                value={filters.status || "all"}
                onValueChange={handleStatusChange}
              >
                <SelectTrigger id="status-filter">
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
            <div className="space-y-2">
              <Label htmlFor="priority-filter">Priority</Label>
              <Select
                value={filters.priority || "all"}
                onValueChange={handlePriorityChange}
              >
                <SelectTrigger id="priority-filter">
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
            <div className="space-y-2">
              <Label htmlFor="sort-by">Sort By</Label>
              <Select value={sorting.sortBy} onValueChange={handleSortByChange}>
                <SelectTrigger id="sort-by">
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
            <div className="space-y-2">
              <Label htmlFor="sort-order">Order</Label>
              <Select value={sorting.sortOrder} onValueChange={handleSortOrderChange}>
                <SelectTrigger id="sort-order">
                  <SelectValue />
                </SelectTrigger>
                <SelectContent>
                  <SelectItem value="asc">Ascending</SelectItem>
                  <SelectItem value="desc">Descending</SelectItem>
                </SelectContent>
              </Select>
            </div>
          </div>

          {/* Reset Filters */}
          {(filters.status || filters.priority || filters.search) && (
            <Button
              variant="outline"
              className="w-full"
              onClick={() => {
                resetFilters();
                setSearchQuery("");
                onClose?.();
              }}
            >
              Reset Filters
            </Button>
          )}
        </div>
      </div>
    </aside>
  );
};
