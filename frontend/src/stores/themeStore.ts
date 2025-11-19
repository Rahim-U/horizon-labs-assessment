/**
 * Theme store using Zustand
 * Manages dark/light theme with localStorage persistence
 */

import { create } from "zustand";
import { persist } from "zustand/middleware";
import { STORAGE_KEYS } from "@/utils/constants";

type Theme = "light" | "dark";

interface ThemeState {
  // State
  theme: Theme;

  // Actions
  setTheme: (theme: Theme) => void;
  toggleTheme: () => void;
}

/**
 * Theme store
 */
export const useThemeStore = create<ThemeState>()(
  persist(
    (set) => ({
      // Initial state - check system preference
      theme: "light",

      /**
       * Set theme
       */
      setTheme: (theme: Theme) => {
        // Update document class for Tailwind dark mode
        if (theme === "dark") {
          document.documentElement.classList.add("dark");
        } else {
          document.documentElement.classList.remove("dark");
        }

        set({ theme });
      },

      /**
       * Toggle between light and dark theme
       */
      toggleTheme: () => {
        set((state) => {
          const newTheme = state.theme === "light" ? "dark" : "light";

          // Update document class
          if (newTheme === "dark") {
            document.documentElement.classList.add("dark");
          } else {
            document.documentElement.classList.remove("dark");
          }

          return { theme: newTheme };
        });
      },
    }),
    {
      name: STORAGE_KEYS.THEME,
      onRehydrateStorage: () => (state) => {
        // Apply theme on hydration
        if (state?.theme === "dark") {
          document.documentElement.classList.add("dark");
        } else {
          document.documentElement.classList.remove("dark");
        }
      },
    }
  )
);
