# Task Management Application

A full-stack task management application with a modern React frontend and a robust FastAPI backend. Features user authentication, task CRUD operations, real-time updates, and a responsive design with dark/light theme support.

## 🏗️ Project Structure

This is a monorepo containing both frontend and backend applications:

```
task-management-assessment/
├── backend/          # FastAPI backend (Python)
│   ├── app/         # Application code
│   ├── migrations/  # Database migrations
│   ├── README.md    # Backend setup instructions
│   └── requirements.txt
├── frontend/        # React frontend (TypeScript)
│   ├── src/         # Application code
│   ├── public/      # Static assets
│   ├── README.md    # Frontend setup instructions
│   └── package.json
├── .gitignore       # Git ignore rules
└── README.md        # This file
```

## 🚀 Quick Start

### Prerequisites

- **Node.js**: 18+ (for frontend)
- **Python**: 3.8+ (for backend)
- **npm**: 9+ (comes with Node.js)
- **pip**: Python package manager

### Backend Setup

1. Navigate to backend directory:
   ```bash
   cd backend
   ```

2. Create virtual environment:
   ```bash
   # Windows
   python -m venv venv
   venv\Scripts\activate

   # Linux/Mac
   python3 -m venv venv
   source venv/bin/activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Create `.env` file:
   ```env
   DATABASE_URL=sqlite:///./backend.db
   AUTO_CREATE_TABLES=true
   ENVIRONMENT=development
   SECRET_KEY=secret-key-change-in-production-MUST-BE-64-CHARS-MINIMUM-PLEASE-CHANGE
   ```

5. Run the server:
   ```bash
   python -m uvicorn app.main:app --reload --host 127.0.0.1 --port 8000
   ```

For detailed backend setup, see [backend/README.md](./backend/README.md)

### Frontend Setup

1. Navigate to frontend directory:
   ```bash
   cd frontend
   ```

2. Install dependencies:
   ```bash
   npm install
   ```

3. Create `.env` file:
   ```env
   VITE_API_BASE_URL=http://localhost:8000
   ```

4. Start development server:
   ```bash
   npm run dev
   ```

For detailed frontend setup, see [frontend/README.md](./frontend/README.md)

## 📚 Documentation

- **Backend API Documentation**: http://localhost:8000/docs (when backend is running)
- **Backend README**: [backend/README.md](./backend/README.md)
- **Frontend README**: [frontend/README.md](./frontend/README.md)

## 🛠️ Tech Stack

### Backend
- **Framework**: FastAPI 0.121.2
- **Database**: SQLite (dev) / PostgreSQL (prod)
- **ORM**: SQLAlchemy 2.0.44
- **Authentication**: JWT with refresh tokens
- **Validation**: Pydantic 2.12.4

### Frontend
- **Framework**: React 19 + TypeScript
- **Build Tool**: Vite 7
- **Styling**: Tailwind CSS 4 + ShadCN UI
- **State Management**: Zustand
- **Routing**: React Router v7
- **Forms**: React Hook Form + Zod

## ✨ Features

- ✅ User authentication (login/register)
- ✅ JWT token management with refresh tokens
- ✅ Email verification (optional)
- ✅ Password reset functionality
- ✅ Task CRUD operations
- ✅ Task filtering and sorting
- ✅ Real-time updates
- ✅ Responsive design
- ✅ Dark/Light theme support
- ✅ Form validation
- ✅ Error handling
- ✅ Rate limiting
- ✅ Security best practices

## 🔧 Development

### Running Both Services

**Terminal 1 - Backend:**
```bash
cd backend
venv\Scripts\activate  # Windows
# source venv/bin/activate  # Linux/Mac
python -m uvicorn app.main:app --reload --host 127.0.0.1 --port 8000
```

**Terminal 2 - Frontend:**
```bash
cd frontend
npm run dev
```

- Backend API: http://localhost:8000
- Frontend App: http://localhost:5173
- API Docs: http://localhost:8000/docs

## 📦 Building for Production

### Backend

```bash
cd backend
# Set ENVIRONMENT=production in .env
# Configure PostgreSQL database
# Set strong SECRET_KEY
uvicorn app.main:app --host 0.0.0.0 --port 8000 --workers 4
```

### Frontend

```bash
cd frontend
npm run build
# Deploy the dist/ folder to your hosting service
```

## 🔒 Security

### Development
- Default SECRET_KEY is acceptable
- CORS defaults to localhost
- SQLite database for simplicity

### Production
- ⚠️ **CRITICAL**: Generate strong SECRET_KEY (64+ characters)
- ⚠️ **CRITICAL**: Set ENVIRONMENT=production
- ⚠️ **CRITICAL**: Configure CORS_ORIGINS
- Use PostgreSQL database
- Enable HTTPS/TLS
- Configure proper firewall rules

## 📝 Environment Variables

### Backend (.env in backend/)
```env
DATABASE_URL=sqlite:///./backend.db
AUTO_CREATE_TABLES=true
ENVIRONMENT=development
SECRET_KEY=your-secret-key-here
CORS_ORIGINS=http://localhost:5173
```

### Frontend (.env in frontend/)
```env
VITE_API_BASE_URL=http://localhost:8000
```

## 🧪 Testing

### Backend API Testing
Use the interactive API documentation at http://localhost:8000/docs or use curl/Postman.

### Frontend Testing
The frontend includes comprehensive form validation and error handling. Test the application through the UI.

## 🐛 Troubleshooting

### Backend Issues
See [backend/README.md](./backend/README.md#troubleshooting)

### Frontend Issues
See [frontend/README.md](./frontend/README.md#troubleshooting)

### Common Issues
- **Port conflicts**: Change ports in configuration files
- **CORS errors**: Ensure backend CORS_ORIGINS includes frontend URL
- **Database errors**: Run migrations or recreate database
- **Module not found**: Reinstall dependencies

## 📄 License

This project is part of a technical assessment.

## 👥 Contributing

This is a technical assessment project. For questions or issues, please refer to the documentation in the respective frontend/backend README files.

---

**Version**: 1.0.0  
**Last Updated**: November 19, 2025

