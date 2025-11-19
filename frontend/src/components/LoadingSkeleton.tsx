/**
 * Loading skeleton components for tasks
 */

import {
  Table,
  TableBody,
  TableCell,
  TableHead,
  TableHeader,
  TableRow,
} from "@/components/ui/table";
import { Skeleton } from "@/components/ui/skeleton";

export const TaskTableSkeleton = () => {
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
            {Array.from({ length: 5 }).map((_, i) => (
              <TableRow key={i}>
                <TableCell>
                  <Skeleton className="h-5 w-full" />
                </TableCell>
                <TableCell>
                  <div className="space-y-2">
                    <Skeleton className="h-4 w-full" />
                    <Skeleton className="h-4 w-3/4" />
                  </div>
                </TableCell>
                <TableCell>
                  <Skeleton className="h-6 w-20" />
                </TableCell>
                <TableCell>
                  <Skeleton className="h-6 w-16" />
                </TableCell>
                <TableCell className="hidden lg:table-cell">
                  <Skeleton className="h-6 w-24" />
                </TableCell>
                <TableCell className="hidden xl:table-cell">
                  <Skeleton className="h-4 w-28" />
                </TableCell>
                <TableCell className="text-right">
                  <Skeleton className="h-8 w-8 ml-auto" />
                </TableCell>
              </TableRow>
            ))}
          </TableBody>
        </Table>
      </div>
    </div>
  );
};
