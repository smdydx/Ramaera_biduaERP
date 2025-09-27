# CRM + HRMS System

## Overview
Professional MNC-style Customer Relationship Management (CRM) and Human Resource Management System (HRMS) built with modern technologies.

## Technology Stack
- **Backend**: FastAPI with Python 3.11
- **Frontend**: React 18 with TypeScript and Ant Design
- **Database**: MongoDB Atlas
- **Authentication**: JWT with role-based access control

## Project Structure
```
├── backend/          # FastAPI backend application
├── frontend/         # React frontend application  
├── docs/            # Project documentation
└── progress_log.md  # Development progress tracking
```

## Current Status
- **Phase**: Project Setup & Schema Design
- **Progress**: Initial project structure created
- **Database**: MongoDB Atlas connection configured
- **Next**: Database schema design and backend API development

## User Preferences
- Professional MNC-style interface design
- Fully responsive across all devices
- Enterprise-grade security and validation
- Comprehensive testing coverage
- Structured development approach: Schema → Backend → Testing → Frontend → Testing

## Key Features

### CRM Module
- Lead management and tracking
- Customer profiles and history
- Sales pipeline visualization
- Contact management system
- Sales analytics and reporting

### HRMS Module  
- Employee records management
- Attendance tracking system
- Leave management workflow
- Basic payroll information
- HR analytics dashboard

### User Roles
- **Admin**: Full system access and configuration
- **HR Manager**: Complete HRMS access + basic CRM view
- **Sales Team**: Full CRM access + limited employee info
- **Employee**: Personal profile + leave requests + attendance

## Architecture Decisions
- Microservices-ready FastAPI backend with proper separation of concerns
- React frontend with component-based architecture
- MongoDB for flexible document storage suitable for CRM/HRMS data
- JWT authentication for stateless, scalable security
- Ant Design for professional, enterprise-grade UI components