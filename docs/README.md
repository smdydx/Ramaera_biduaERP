
# CRM + HRMS System

A comprehensive Customer Relationship Management (CRM) and Human Resource Management System (HRMS) built with FastAPI and React.

## Architecture

### Backend (FastAPI)
- **API Framework**: FastAPI with async/await support
- **Database**: MongoDB with Motor (async driver)
- **Authentication**: JWT tokens with bcrypt password hashing
- **Validation**: Pydantic models for request/response validation
- **CORS**: Configured for cross-origin requests

### Frontend (React + TypeScript)
- **Framework**: React 18 with TypeScript
- **Styling**: CSS modules with responsive design
- **State Management**: React hooks and context
- **API Communication**: Fetch API with service layer

## Project Structure

```
├── backend/
│   ├── app/
│   │   ├── api/v1/endpoints/     # API route handlers
│   │   ├── core/                 # Core configurations
│   │   ├── models/               # Database models
│   │   ├── schemas/              # Pydantic schemas
│   │   ├── services/             # Business logic
│   │   ├── utils/                # Utility functions
│   │   └── middleware/           # Custom middleware
│   ├── tests/                    # Test files
│   └── main.py                   # Application entry point
├── frontend/
│   ├── src/
│   │   ├── components/           # React components
│   │   ├── services/             # API service layer
│   │   └── App.tsx               # Main application
│   └── public/                   # Static assets
└── docs/                         # Documentation
```

## Features

### CRM Module
- Customer management (CRUD operations)
- Lead tracking and conversion
- Sales pipeline management
- Customer communication history

### HRMS Module
- Employee management
- Department organization
- Attendance tracking
- Leave request management
- Payroll processing

## API Endpoints

### Authentication
- `POST /api/v1/auth/login` - User login
- `POST /api/v1/auth/register` - User registration

### CRM
- `GET /api/v1/customers` - List customers
- `POST /api/v1/customers` - Create customer
- `GET /api/v1/leads` - List leads
- `POST /api/v1/leads` - Create lead

### HRMS
- `GET /api/v1/employees` - List employees
- `POST /api/v1/employees` - Create employee
- `GET /api/v1/attendance` - Get attendance records
- `GET /api/v1/leave-requests` - List leave requests

## Development

### Prerequisites
- Python 3.8+
- Node.js 16+
- MongoDB

### Setup
1. Install backend dependencies: `cd backend && pip install -r requirements.txt`
2. Install frontend dependencies: `cd frontend && npm install`
3. Configure environment variables
4. Start MongoDB service
5. Run backend: `python backend/main.py`
6. Run frontend: `npm start` (in frontend directory)

### Environment Variables
Create a `.env` file in the root directory:
```
MONGODB_URI=mongodb://localhost:27017
DATABASE_NAME=crm_hrms_db
SECRET_KEY=your-secret-key
ACCESS_TOKEN_EXPIRE_MINUTES=60
```

## Testing
Run tests with: `pytest backend/tests/`

## Deployment
This application is designed to be deployed on Replit with automatic dependency installation and port configuration.
