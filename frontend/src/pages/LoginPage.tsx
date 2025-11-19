/**
 * Login page component
 */

import { useEffect } from "react";
import { Link, useNavigate } from "react-router-dom";
import { Card, CardContent, CardDescription, CardFooter, CardHeader, CardTitle } from "@/components/ui/card";
import { LoginForm } from "@/components/forms/LoginForm";
import { useAuth } from "@/hooks/useAuth";
import toast from "react-hot-toast";
import type { LoginCredentials } from "@/types/auth";

export const LoginPage = () => {
  const { login, loading, isAuthenticated, error, clearError } = useAuth();
  const navigate = useNavigate();

  // Redirect if already authenticated
  useEffect(() => {
    if (isAuthenticated) {
      navigate("/dashboard", { replace: true });
    }
  }, [isAuthenticated, navigate]);

  // Show error toast
  useEffect(() => {
    if (error) {
      toast.error(error);
      clearError();
    }
  }, [error, clearError]);

  const handleSubmit = async (data: LoginCredentials) => {
    try {
      await login(data);
      toast.success("Welcome back!");
      navigate("/dashboard", { replace: true });
    } catch {
      // Error is handled by the store and shown via toast
    }
  };

  return (
    <div className="flex min-h-screen items-center justify-center bg-muted/40 p-4">
      <Card className="w-full max-w-md">
        <CardHeader className="space-y-1">
          <CardTitle className="text-2xl font-bold">Sign in</CardTitle>
          <CardDescription>
            Enter your email and password to access your account
          </CardDescription>
        </CardHeader>
        <CardContent>
          <LoginForm onSubmit={handleSubmit} loading={loading} />
        </CardContent>
        <CardFooter className="flex flex-col space-y-4">
          <div className="text-sm text-muted-foreground">
            Don't have an account?{" "}
            <Link to="/register" className="font-medium text-primary hover:underline">
              Create account
            </Link>
          </div>
        </CardFooter>
      </Card>
    </div>
  );
};
