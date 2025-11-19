/**
 * Header component with navigation and theme toggle
 */

import { Link } from "react-router-dom";
import { Button } from "@/components/ui/button";
import {
  DropdownMenu,
  DropdownMenuContent,
  DropdownMenuItem,
  DropdownMenuLabel,
  DropdownMenuSeparator,
  DropdownMenuTrigger,
} from "@/components/ui/dropdown-menu";
import { Moon, Sun, User, LogOut, CheckSquare, Menu } from "lucide-react";
import { useAuth } from "@/hooks/useAuth";
import { useThemeStore } from "@/stores/themeStore";

interface HeaderProps {
  onMenuClick?: () => void;
}

export const Header = ({ onMenuClick }: HeaderProps) => {
  const { user, logout, isAuthenticated } = useAuth();
  const { theme, toggleTheme } = useThemeStore();

  const handleMenuClick = () => {
    if (onMenuClick) {
      onMenuClick();
    } else {
      // Dispatch custom event for mobile sidebar toggle
      window.dispatchEvent(new Event('toggle-mobile-sidebar'));
    }
  };

  return (
    <header className="sticky top-0 z-50 w-full border-b border-border/40 bg-background/95 backdrop-blur supports-backdrop-filter:bg-background/60">
      <div className="flex h-14 sm:h-16 items-center justify-between px-4 sm:px-4 md:px-6 container mx-auto">
        {/* Logo and Menu */}
        <div className="flex items-center gap-2 sm:gap-3 md:gap-4 min-w-0 flex-1">
          {isAuthenticated && (
            <Button
              variant="ghost"
              size="icon"
              className="md:hidden h-9 w-9 shrink-0"
              onClick={handleMenuClick}
              aria-label="Open filters"
            >
              <Menu className="h-5 w-5" />
            </Button>
          )}

          <Link to="/" className="flex items-center gap-1.5 sm:gap-2 font-semibold min-w-0">
            <CheckSquare className="h-5 w-5 sm:h-6 sm:w-6 text-primary shrink-0" />
            <span className="text-base sm:text-lg truncate">TaskManager</span>
          </Link>
        </div>

        {/* Right side - Theme toggle and User menu */}
        <div className="flex items-center gap-1 sm:gap-2 shrink-0">
          {/* Theme toggle */}
          <Button
            variant="ghost"
            size="icon"
            className="h-9 w-9"
            onClick={toggleTheme}
            aria-label="Toggle theme"
          >
            {theme === "light" ? (
              <Moon className="h-4 w-4 sm:h-5 sm:w-5" />
            ) : (
              <Sun className="h-4 w-4 sm:h-5 sm:w-5" />
            )}
          </Button>

          {/* User menu */}
          {isAuthenticated && user && (
            <DropdownMenu modal={false}>
              <DropdownMenuTrigger asChild>
                <Button
                  variant="ghost"
                  size="icon"
                  className="relative h-9 w-9 data-[state=open]:bg-transparent"
                  aria-label="User menu"
                >
                  <User className="h-4 w-4 sm:h-5 sm:w-5" />
                </Button>
              </DropdownMenuTrigger>
              <DropdownMenuContent
                align="end"
                sideOffset={8}
                alignOffset={0}
                collisionPadding={16}
                avoidCollisions={false}
                className="w-48 sm:w-56"
              >
                <DropdownMenuLabel>
                  <div className="flex flex-col space-y-1">
                    <p className="text-sm font-medium truncate">{user.username}</p>
                    <p className="text-xs text-muted-foreground truncate">{user.email}</p>
                  </div>
                </DropdownMenuLabel>
                <DropdownMenuSeparator />
                <DropdownMenuItem onClick={logout} className="text-destructive cursor-pointer">
                  <LogOut className="mr-2 h-4 w-4" />
                  <span>Log out</span>
                </DropdownMenuItem>
              </DropdownMenuContent>
            </DropdownMenu>
          )}
        </div>
      </div>
    </header>
  );
};
