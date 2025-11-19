/**
 * Footer component
 */

export const Footer = () => {
  const currentYear = new Date().getFullYear();

  return (
    <footer className="mt-auto border-t border-border bg-card">
      <div className="container flex h-14 items-center justify-center px-4">
        <p className="text-sm text-muted-foreground">
          © {currentYear} TaskManager. All rights reserved.
        </p>
      </div>
    </footer>
  );
};
