# Task Management Frontend

A modern, production-ready task management application built with React, TypeScript, and Tailwind CSS. Features a clean, responsive UI with dark/light theme support, real-time task management, and seamless backend integration.

## Table of Contents

- [Overview](#overview)
- [Tech Stack](#tech-stack)
- [Prerequisites](#prerequisites)
- [Quick Start](#quick-start)
- [Project Structure](#project-structure)
- [Configuration](#configuration)
- [Development](#development)
- [Building for Production](#building-for-production)
- [Features](#features)
- [API Integration](#api-integration)
- [Architecture](#architecture)
- [Troubleshooting](#troubleshooting)
- [Best Practices](#best-practices)

---

## Overview

This frontend application provides a complete task management interface with:

- **User Authentication**: Secure login and registration with JWT tokens
- **Task Management**: Full CRUD operations with filtering, sorting, and pagination
- **Real-time Updates**: Optimistic UI updates for better user experience
- **Responsive Design**: Mobile-first design that works on all devices
- **Theme Support**: Dark/Light mode with persistent preferences
- **Form Validation**: Type-safe validation with React Hook Form + Zod
- **Error Handling**: Comprehensive error handling with user-friendly messages

---

## Tech Stack

### Core Framework
- **React**: 19.2.0 (Latest with concurrent features)
- **TypeScript**: 5.9.3 (Strict mode enabled)
- **Vite**: 7.2.2 (Fast build tool and dev server)

### UI & Styling
- **Tailwind CSS**: 4.1.17 (Utility-first CSS framework)
- **ShadCN UI**: Production-ready accessible components
- **Lucide React**: Modern icon library
- **date-fns**: Date formatting and manipulation

### State Management & Routing
- **Zustand**: 5.0.8 (Lightweight state management)
- **React Router**: 7.9.6 (Client-side routing)

### Forms & Validation
- **React Hook Form**: 7.66.1 (Performant form library)
- **Zod**: 4.1.12 (TypeScript-first schema validation)
- **@hookform/resolvers**: Zod integration for React Hook Form

### HTTP & Notifications
- **Axios**: 1.13.2 (HTTP client with interceptors)
- **React Hot Toast**: 2.6.0 (Toast notifications)

### Development Tools
- **ESLint**: Code linting
- **TypeScript ESLint**: TypeScript-specific linting rules

---

## Prerequisites

Before you begin, ensure you have the following installed:

- **Node.js**: 18.0.0 or higher (20+ recommended)
- **npm**: 9.0.0 or higher (comes with Node.js)
- **Git**: For version control

**Verify Installation:**
```bash
node --version  # Should be 18.0.0 or higher
npm --version   # Should be 9.0.0 or higher
```

**Optional but Recommended:**
- **VS Code**: With extensions:
  - ESLint
  - Prettier
  - Tailwind CSS IntelliSense
  - TypeScript and JavaScript Language Features

---

## Quick Start

### Step 1: Navigate to Frontend Directory

```bash
cd frontend
```

### Step 2: Install Dependencies

```bash
npm install
```

This will install all required dependencies listed in `package.json`.

### Step 3: Configure Environment Variables

Create a `.env` file in the `frontend` directory:

```bash
# Windows PowerShell
New-Item -ItemType File -Path .env

# Linux/Mac
touch .env
```

Add the following configuration:

```env
# Backend API URL
VITE_API_BASE_URL=http://localhost:8000
```

**Note**: The `VITE_` prefix is required for Vite to expose the variable to your application.

### Step 4: Start Development Server

```bash
npm run dev
```

The application will be available at:
- **Local**: http://localhost:5173
- **Network**: The terminal will show the network URL

### Step 5: Verify Backend is Running

Ensure the backend API is running on `http://localhost:8000` (or update `VITE_API_BASE_URL` accordingly).

---

## Project Structure

```
frontend/
├── public/                 # Static assets
│   └── vite.svg           # Vite logo
├── src/
│   ├── components/        # React components
│   │   ├── ui/            # ShadCN base components
│   │   │   ├── button.tsx
│   │   │   ├── card.tsx
│   │   │   ├── dialog.tsx
│   │   │   └── ...        # Other UI components
│   │   ├── forms/         # Form components
│   │   │   ├── LoginForm.tsx
│   │   │   ├── RegisterForm.tsx
│   │   │   └── TaskForm.tsx
│   │   ├── layout/        # Layout components
│   │   │   ├── Header.tsx
│   │   │   ├── Sidebar.tsx
│   │   │   └── Footer.tsx
│   │   ├── TaskCard.tsx    # Task display component
│   │   ├── TaskTable.tsx   # Task table view
│   │   ├── TaskFilters.tsx # Filter controls
│   │   ├── EmptyState.tsx  # Empty state component
│   │   ├── LoadingSkeleton.tsx # Loading states
│   │   └── ErrorBoundary.tsx   # Error boundary
│   ├── pages/             # Page components
│   │   ├── LoginPage.tsx
│   │   ├── RegisterPage.tsx
│   │   └── DashboardPage.tsx
│   ├── stores/            # Zustand state stores
│   │   ├── authStore.ts   # Authentication state
│   │   ├── taskStore.ts   # Task state management
│   │   └── themeStore.ts  # Theme state (dark/light)
│   ├── services/          # API service layer
│   │   ├── authService.ts # Authentication API calls
│   │   └── taskService.ts # Task API calls
│   ├── hooks/             # Custom React hooks
│   │   ├── useAuth.ts     # Authentication hook
│   │   ├── useTasks.ts    # Task management hook
│   │   ├── useProtectedRoute.ts # Route protection
│   │   └── useOnlineStatus.ts  # Online/offline detection
│   ├── types/             # TypeScript type definitions
│   │   ├── auth.ts        # Authentication types
│   │   ├── task.ts        # Task types
│   │   └── api.ts         # API response types
│   ├── utils/             # Utility functions
│   │   ├── api.ts         # Axios client configuration
│   │   ├── constants.ts   # Application constants
│   │   └── formatters.ts # Date/text formatting
│   ├── lib/               # Library configurations
│   │   └── utils.ts       # Utility functions (cn, etc.)
│   ├── App.tsx            # Main app component with routing
│   ├── main.tsx           # Application entry point
│   └── index.css          # Global styles + Tailwind imports
├── .env                   # Environment variables (create this)
├── .gitignore             # Git ignore rules
├── components.json        # ShadCN UI configuration
├── eslint.config.js       # ESLint configuration
├── index.html             # HTML entry point
├── package.json           # Dependencies and scripts
├── tsconfig.json          # TypeScript configuration
├── tsconfig.app.json      # App-specific TS config
├── tsconfig.node.json     # Node-specific TS config
├── vite.config.ts         # Vite configuration
└── README.md              # This file
```

---

## Configuration

### Environment Variables

Create a `.env` file in the `frontend` directory:

```env
# Backend API Base URL
VITE_API_BASE_URL=http://localhost:8000
```

**Important Notes:**
- All environment variables must be prefixed with `VITE_` to be accessible in the browser
- Restart the dev server after changing environment variables
- Never commit `.env` files with sensitive data (already in `.gitignore`)

### Vite Configuration

The `vite.config.ts` file includes:
- React plugin for JSX/TSX support
- Tailwind CSS plugin
- Path alias `@` pointing to `src/` directory

### TypeScript Configuration

- **Strict mode**: Enabled for type safety
- **Path aliases**: `@/*` maps to `src/*`
- **Module resolution**: Node16/NodeNext

---

## Development

### Available Scripts

```bash
# Start development server
npm run dev

# Build for production
npm run build

# Preview production build locally
npm run preview

# Lint code
npm run lint
```

### Development Server

The development server runs on `http://localhost:5173` by default with:
- **Hot Module Replacement (HMR)**: Instant updates without page reload
- **Fast Refresh**: Preserves component state during updates
- **Source Maps**: For debugging in browser DevTools

### Code Quality

#### Linting

```bash
npm run lint
```

ESLint is configured with:
- React Hooks rules
- TypeScript-specific rules
- Modern JavaScript best practices

#### Type Checking

TypeScript type checking happens automatically during:
- Development (via IDE)
- Build process (`npm run build`)

### Development Workflow

1. **Start Backend**: Ensure the backend API is running
2. **Start Frontend**: Run `npm run dev`
3. **Open Browser**: Navigate to `http://localhost:5173`
4. **Make Changes**: Edit files and see changes instantly
5. **Check Console**: Monitor for errors in browser DevTools

---

## Building for Production

### Build Command

```bash
npm run build
```

This will:
1. Run TypeScript type checking
2. Bundle and optimize all assets
3. Generate production-ready files in `dist/` directory

### Build Output

The `dist/` directory will contain:
- `index.html` - Entry HTML file
- `assets/` - Optimized JavaScript and CSS bundles
- Static assets from `public/` directory

### Preview Production Build

```bash
npm run preview
```

This serves the production build locally for testing before deployment.

### Deployment

#### Static Hosting (Recommended)

The build output is a static site that can be deployed to:
- **Vercel**: `vercel --prod`
- **Netlify**: Drag and drop `dist/` folder
- **GitHub Pages**: Configure to serve `dist/` directory
- **AWS S3 + CloudFront**: Upload `dist/` to S3 bucket
- **Any static hosting service**

#### Environment Variables for Production

Set environment variables in your hosting platform:
- `VITE_API_BASE_URL`: Your production API URL

**Example for Vercel:**
```bash
vercel env add VITE_API_BASE_URL
# Enter: https://api.yourdomain.com
```

---

## Features

### Core Functionality

- ✅ **User Authentication**
  - Login with email/username and password
  - Registration with email verification
  - JWT token management
  - Automatic token refresh
  - Protected routes

- ✅ **Task Management**
  - Create, read, update, and delete tasks
  - Filter by status (pending, in-progress, completed)
  - Filter by priority (low, medium, high)
  - Sort by multiple criteria (date, title, priority, status)
  - Search functionality
  - Due date management

### UI/UX Features

- 🎨 **Theme Support**
  - Dark and light themes
  - Persistent theme preference (localStorage)
  - Smooth theme transitions

- 📱 **Responsive Design**
  - Mobile-first approach
  - Optimized for all screen sizes
  - Touch-friendly interactions

- ⚡ **Performance**
  - Loading states and skeletons
  - Optimistic UI updates
  - Efficient re-renders
  - Code splitting ready

- 🔔 **User Feedback**
  - Toast notifications for actions
  - Form validation with inline errors
  - Empty states with helpful messages
  - Error boundaries for graceful error handling

### Developer Experience

- 📦 **Clean Architecture**
  - Separation of concerns
  - Modular component structure
  - Reusable hooks and utilities

- 🔒 **Type Safety**
  - TypeScript strict mode
  - Type-safe API calls
  - Validated form inputs

- 🎯 **Code Quality**
  - ESLint configuration
  - Consistent code style
  - Comprehensive documentation

---

## API Integration

### Authentication Flow

1. **Login/Register**: User credentials sent to `/api/v1/auth/login` or `/api/v1/auth/register`
2. **Token Storage**: JWT tokens stored in `localStorage`
3. **Automatic Injection**: Axios interceptors add token to all requests
4. **Token Refresh**: Automatic refresh token handling
5. **Logout**: Clear tokens and redirect to login

### API Client Configuration

Located in `src/utils/api.ts`:
- Base URL from environment variable
- Request interceptor: Adds JWT token to headers
- Response interceptor: Handles errors and token refresh
- Error handling: Converts API errors to user-friendly messages

### Service Layer

API calls are abstracted in service files:
- `src/services/authService.ts`: Authentication endpoints
- `src/services/taskService.ts`: Task CRUD operations

### Error Handling

- **Network Errors**: Displayed as toast notifications
- **Validation Errors**: Shown inline in forms
- **401 Unauthorized**: Automatic logout and redirect
- **500 Server Errors**: User-friendly error messages

---

## Architecture

### Design Patterns

#### Clean Architecture
- **Presentation Layer**: Components and pages
- **Business Logic Layer**: Stores and hooks
- **Data Layer**: Services and API client

#### State Management (Zustand)

**Auth Store** (`stores/authStore.ts`):
- User authentication state
- Login/logout actions
- Token management

**Task Store** (`stores/taskStore.ts`):
- Task list state
- Filter and sort state
- CRUD operations

**Theme Store** (`stores/themeStore.ts`):
- Current theme
- Theme toggle action
- Persistent storage

#### Custom Hooks

- `useAuth`: Authentication state and actions
- `useTasks`: Task management with filters
- `useProtectedRoute`: Route protection logic
- `useOnlineStatus`: Network status detection

### Form Handling

**React Hook Form + Zod**:
- Type-safe validation schemas
- Uncontrolled components for performance
- Easy integration with ShadCN UI components
- Real-time validation feedback

### Styling Approach

**Tailwind CSS 4**:
- Utility-first CSS framework
- Consistent design system
- Excellent performance (tree-shaking)
- Responsive breakpoints

**ShadCN UI**:
- Accessible component library
- Fully customizable
- Copy-paste workflow
- No runtime dependencies

---

## Troubleshooting

### Common Issues

#### "Cannot find module" or Import Errors

**Solution:**
1. Delete `node_modules` and `package-lock.json`
2. Run `npm install` again
3. Restart your IDE/editor
4. Check that you're using the correct import paths (use `@/` alias)

#### Port Already in Use

**Solution:**
```bash
# Find process using port 5173
# Windows
netstat -ano | findstr :5173

# Linux/Mac
lsof -i :5173

# Kill the process or use a different port
# In vite.config.ts, add:
export default defineConfig({
  server: {
    port: 5174
  }
})
```

#### API Connection Errors

**Solution:**
1. Verify backend is running: `http://localhost:8000`
2. Check `VITE_API_BASE_URL` in `.env` file
3. Check browser console for CORS errors
4. Verify backend CORS configuration allows your frontend URL

#### TypeScript Errors

**Solution:**
1. Run `npm run build` to see all type errors
2. Check `tsconfig.json` configuration
3. Ensure all dependencies are installed
4. Restart TypeScript server in your IDE

#### Build Failures

**Solution:**
1. Clear build cache: Delete `dist/` and `node_modules/.vite`
2. Update dependencies: `npm update`
3. Check for TypeScript errors: `npm run build`
4. Verify all environment variables are set

#### Styling Issues (Tailwind not working)

**Solution:**
1. Verify Tailwind is imported in `src/index.css`
2. Check `vite.config.ts` includes Tailwind plugin
3. Restart dev server
4. Check browser console for CSS errors

#### Authentication Issues

**Solution:**
1. Check browser localStorage for tokens
2. Verify token format in browser DevTools
3. Check network tab for API responses
4. Verify backend authentication endpoints are working

### Getting Help

1. **Check Browser Console**: Look for JavaScript errors
2. **Check Network Tab**: Verify API requests are being made
3. **Check Backend Logs**: Ensure backend is receiving requests
4. **Review Documentation**: Check backend README for API details

---

## Best Practices

### Code Quality

✅ **TypeScript Strict Mode**: Enabled for maximum type safety  
✅ **Consistent Naming**: camelCase for variables, PascalCase for components  
✅ **Component Documentation**: JSDoc comments for complex components  
✅ **Single Responsibility**: Each component/hook has one clear purpose  
✅ **DRY Principle**: Reusable utilities and hooks

### React Patterns

✅ **Functional Components**: Using hooks instead of classes  
✅ **Custom Hooks**: Reusable logic abstraction  
✅ **Proper Prop Typing**: TypeScript interfaces for all props  
✅ **Key Props**: Proper keys in list rendering  
✅ **Error Boundaries**: Ready for error boundary implementation

### Security

✅ **Input Validation**: Zod schemas for all form inputs  
✅ **XSS Protection**: React's built-in XSS protection  
✅ **Secure Token Storage**: localStorage (consider httpOnly cookies for production)  
✅ **HTTPS Ready**: Works with HTTPS in production  
✅ **Environment Variables**: Sensitive data in environment variables

### Accessibility

✅ **Semantic HTML**: Proper HTML elements  
✅ **ARIA Labels**: On interactive elements  
✅ **Keyboard Navigation**: Full keyboard support  
✅ **Focus Management**: Proper focus handling in modals  
✅ **Color Contrast**: WCAG compliant color schemes

### Performance

✅ **Code Splitting**: Ready for React.lazy implementation  
✅ **Memoization**: Where beneficial (useMemo, useCallback)  
✅ **Optimized Re-renders**: Zustand selectors prevent unnecessary renders  
✅ **Skeleton Loading**: Perceived performance improvements  
✅ **Image Optimization**: Ready for image optimization

---

## Responsive Design

### Breakpoints

- **Mobile**: < 640px (default, mobile-first)
- **Tablet**: 640px - 1024px (`sm:` and `md:` breakpoints)
- **Desktop**: > 1024px (`lg:` and `xl:` breakpoints)

### Mobile Behavior

- Single column task grid
- Collapsible sidebar
- Touch-friendly buttons (min 44x44px)
- Hamburger menu navigation
- Optimized spacing for small screens

### Tablet Behavior

- Two column task grid
- Visible sidebar
- Optimized spacing
- Touch and mouse support

### Desktop Behavior

- Three column task grid
- Persistent sidebar
- Enhanced hover states
- Spacious layout
- Full keyboard navigation

---

## Future Enhancements

Potential features for future development:

- [ ] Task categories/tags system
- [ ] Advanced search with full-text search
- [ ] Drag-and-drop task reordering
- [ ] Task comments and notes
- [ ] File attachments for tasks
- [ ] Email notifications integration
- [ ] Collaboration features (shared tasks)
- [ ] Analytics dashboard
- [ ] Export tasks (CSV, PDF, JSON)
- [ ] Keyboard shortcuts
- [ ] Offline support with service workers
- [ ] PWA capabilities
- [ ] Task templates
- [ ] Recurring tasks
- [ ] Task dependencies

---

## Additional Resources

### Documentation

- **Backend API**: See `../backend/README.md` for API documentation
- **API Docs**: http://localhost:8000/docs (when backend is running)
- **React Docs**: https://react.dev
- **TypeScript Docs**: https://www.typescriptlang.org/docs
- **Tailwind CSS**: https://tailwindcss.com/docs
- **Vite Docs**: https://vite.dev

### Useful Commands

```bash
# Install dependencies
npm install

# Start development server
npm run dev

# Build for production
npm run build

# Preview production build
npm run preview

# Lint code
npm run lint

# Check TypeScript types
npx tsc --noEmit
```

---

## License

This project is part of a technical assessment.

---

## Support

For issues or questions:
1. Check the [Troubleshooting](#troubleshooting) section
2. Review browser console for errors
3. Verify backend is running and accessible
4. Check network requests in browser DevTools

---

**Version**: 1.0.0  
**Last Updated**: November 19, 2025  
**Built with ❤️ using modern web technologies**
