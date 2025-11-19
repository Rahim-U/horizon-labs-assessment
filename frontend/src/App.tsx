/**
 * Main App component with routing
 */

import { BrowserRouter as Router, Routes, Route, Navigate } from "react-router-dom";
import { Toaster } from "react-hot-toast";
import { useEffect, lazy, Suspense } from "react";
import { Header } from "@/components/layout/Header";
import { Footer } from "@/components/layout/Footer";
import { ErrorBoundary } from "@/components/ErrorBoundary";
import { useAuth } from "@/hooks/useAuth";
import { useOnlineStatus } from "@/hooks/useOnlineStatus";
import { useThemeStore } from "@/stores/themeStore";
import "./index.css";

// Lazy load page components for code splitting
const LoginPage = lazy(() => import("@/pages/LoginPage").then(module => ({ default: module.LoginPage })));
const RegisterPage = lazy(() => import("@/pages/RegisterPage").then(module => ({ default: module.RegisterPage })));
const DashboardPage = lazy(() => import("@/pages/DashboardPage").then(module => ({ default: module.DashboardPage })));

/**
 * Protected route wrapper
 */
const ProtectedRoute = ({ children }: { children: React.ReactNode }) => {
  const { isAuthenticated, loading, initializeAuth } = useAuth();

  useEffect(() => {
    initializeAuth();
  }, [initializeAuth]);

  if (loading) {
    return (
      <div className="flex min-h-screen items-center justify-center">
        <div className="h-8 w-8 animate-spin rounded-full border-4 border-primary border-t-transparent" />
      </div>
    );
  }

  if (!isAuthenticated) {
    return <Navigate to="/login" replace />;
  }

  return <>{children}</>;
};

/**
 * Public route wrapper (redirects to dashboard if authenticated)
 */
const PublicRoute = ({ children }: { children: React.ReactNode }) => {
  const { isAuthenticated, loading } = useAuth();

  if (loading) {
    return (
      <div className="flex min-h-screen items-center justify-center">
        <div className="h-8 w-8 animate-spin rounded-full border-4 border-primary border-t-transparent" />
      </div>
    );
  }

  if (isAuthenticated) {
    return <Navigate to="/dashboard" replace />;
  }

  return <>{children}</>;
};

/**
 * Loading fallback component
 */
const LoadingFallback = () => (
  <div className="flex min-h-screen items-center justify-center">
    <div className="text-center">
      <div className="h-12 w-12 animate-spin rounded-full border-4 border-primary border-t-transparent mx-auto" />
      <p className="mt-4 text-sm text-muted-foreground">Loading...</p>
    </div>
  </div>
);

function App() {
  const { theme } = useThemeStore();

  // Monitor online/offline status
  useOnlineStatus();

  // Apply theme on mount
  useEffect(() => {
    if (theme === "dark") {
      document.documentElement.classList.add("dark");
    } else {
      document.documentElement.classList.remove("dark");
    }
  }, [theme]);

  // Listen for auth:logout events from API interceptor
  // This replaces hard page redirects with React Router navigation
  useEffect(() => {
    const handleLogout = () => {
      // Check if already on login page to avoid unnecessary navigation
      if (!window.location.pathname.includes("/login")) {
        window.location.href = "/login";
      }
    };

    window.addEventListener('auth:logout', handleLogout);
    return () => window.removeEventListener('auth:logout', handleLogout);
  }, []);

  return (
    <ErrorBoundary>
      <Router>
        <div className="flex min-h-screen flex-col w-full overflow-x-hidden">
          <Header />
          <main className="flex-1 w-full min-w-0">
            <Suspense fallback={<LoadingFallback />}>
              <Routes>
                {/* Public routes */}
                <Route
                  path="/login"
                  element={
                    <PublicRoute>
                      <LoginPage />
                    </PublicRoute>
                  }
                />
                <Route
                  path="/register"
                  element={
                    <PublicRoute>
                      <RegisterPage />
                    </PublicRoute>
                  }
                />

                {/* Protected routes */}
                <Route
                  path="/dashboard"
                  element={
                    <ProtectedRoute>
                      <DashboardPage />
                    </ProtectedRoute>
                  }
                />

                {/* Default redirect */}
                <Route path="/" element={<Navigate to="/dashboard" replace />} />

                {/* 404 - Redirect to dashboard */}
                <Route path="*" element={<Navigate to="/dashboard" replace />} />
              </Routes>
            </Suspense>
          </main>
          <Footer />

          {/* Toast notifications */}
          <Toaster
            position="top-right"
            toastOptions={{
              duration: 3000,
              style: {
                background: "var(--background)",
                color: "var(--foreground)",
                border: "1px solid var(--border)",
              },
              success: {
                iconTheme: {
                  primary: "var(--primary)",
                  secondary: "var(--primary-foreground)",
                },
              },
              error: {
                iconTheme: {
                  primary: "var(--destructive)",
                  secondary: "var(--destructive-foreground)",
                },
              },
            }}
          />
        </div>
      </Router>
    </ErrorBoundary>
  );
}

export default App;
