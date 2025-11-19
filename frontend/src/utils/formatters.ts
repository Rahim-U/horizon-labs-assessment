/**
 * Utility functions for formatting dates, times, and other display values
 */

import { format, formatDistance, isPast, isToday, isTomorrow, parseISO } from "date-fns";

/**
 * Format ISO date string to readable format
 */
export const formatDate = (dateString: string | null): string => {
  if (!dateString) return "No due date";

  try {
    const date = parseISO(dateString);
    return format(date, "MMM dd, yyyy");
  } catch {
    return "Invalid date";
  }
};

/**
 * Format ISO date string to relative time (e.g., "2 days ago")
 */
export const formatRelativeTime = (dateString: string): string => {
  try {
    const date = parseISO(dateString);
    return formatDistance(date, new Date(), { addSuffix: true });
  } catch {
    return "Unknown";
  }
};

/**
 * Format ISO datetime string to readable date and time
 */
export const formatDateTime = (dateString: string): string => {
  try {
    const date = parseISO(dateString);
    return format(date, "MMM dd, yyyy 'at' h:mm a");
  } catch {
    return "Invalid date";
  }
};

/**
 * Check if a due date is overdue
 */
export const isOverdue = (dueDateString: string | null): boolean => {
  if (!dueDateString) return false;

  try {
    const dueDate = parseISO(dueDateString);
    return isPast(dueDate) && !isToday(dueDate);
  } catch {
    return false;
  }
};

/**
 * Check if a due date is today
 */
export const isDueToday = (dueDateString: string | null): boolean => {
  if (!dueDateString) return false;

  try {
    const dueDate = parseISO(dueDateString);
    return isToday(dueDate);
  } catch {
    return false;
  }
};

/**
 * Check if a due date is tomorrow
 */
export const isDueTomorrow = (dueDateString: string | null): boolean => {
  if (!dueDateString) return false;

  try {
    const dueDate = parseISO(dueDateString);
    return isTomorrow(dueDate);
  } catch {
    return false;
  }
};

/**
 * Get due date status with color indicator
 */
export const getDueDateStatus = (dueDateString: string | null): {
  label: string;
  variant: "default" | "secondary" | "destructive";
  isWarning: boolean;
} => {
  if (!dueDateString) {
    return { label: "No due date", variant: "default", isWarning: false };
  }

  if (isOverdue(dueDateString)) {
    return { label: "Overdue", variant: "destructive", isWarning: false };
  }

  if (isDueToday(dueDateString)) {
    return { label: "Due today", variant: "secondary", isWarning: true };
  }

  if (isDueTomorrow(dueDateString)) {
    return { label: "Due tomorrow", variant: "secondary", isWarning: true };
  }

  return { label: formatDate(dueDateString), variant: "default", isWarning: false };
};

/**
 * Truncate text to specified length
 */
export const truncateText = (text: string, maxLength: number): string => {
  if (text.length <= maxLength) return text;
  return `${text.substring(0, maxLength)}...`;
};

/**
 * Capitalize first letter of string
 */
export const capitalize = (str: string): string => {
  return str.charAt(0).toUpperCase() + str.slice(1);
};
