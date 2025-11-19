/**
 * Registration page component
 */

import { useEffect } from "react";
import { Link, useNavigate } from "react-router-dom";
import { Card, CardContent, CardDescription, CardFooter, CardHeader, CardTitle } from "@/components/ui/card";
import { RegisterForm } from "@/components/forms/RegisterForm";
import { useAuth } from "@/hooks/useAuth";
import toast from "react-hot-toast";
import type { UserCreate } from "@/types/auth";

export const RegisterPage = () => {
  const { register, loading, isAuthenticated, error, clearError } = useAuth();
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

  const handleSubmit = async (data: UserCreate) => {
    try {
      await register(data);
      toast.success("Account created successfully!");
      navigate("/dashboard", { replace: true });
    } catch {
      // Error is handled by the store and shown via toast
    }
  };

  return (
    <div className="flex min-h-screen items-center justify-center bg-muted/40 p-4">
      <Card className="w-full max-w-md">
        <CardHeader className="space-y-1">
          <CardTitle className="text-2xl font-bold">Create account</CardTitle>
          <CardDescription>
            Enter your information to create a new account
          </CardDescription>
        </CardHeader>
        <CardContent>
          <RegisterForm onSubmit={handleSubmit} loading={loading} />
        </CardContent>
        <CardFooter className="flex flex-col space-y-4">
          <div className="text-sm text-muted-foreground">
            Already have an account?{" "}
            <Link to="/login" className="font-medium text-primary hover:underline">
              Sign in
            </Link>
          </div>
        </CardFooter>
      </Card>
    </div>
  );
};
