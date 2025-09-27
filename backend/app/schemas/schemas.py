from pydantic import BaseModel, EmailStr, Field
from typing import Optional, List
from datetime import datetime, date
from ..models.models import UserRole, LeadStatus, CustomerStatus, EmployeeStatus, LeaveStatus, AttendanceStatus

# Base schemas
class BaseSchema(BaseModel):
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

# User schemas
class UserCreate(BaseModel):
    email: EmailStr
    full_name: str
    password: str
    role: UserRole = UserRole.EMPLOYEE

class UserUpdate(BaseModel):
    email: Optional[EmailStr] = None
    full_name: Optional[str] = None
    role: Optional[UserRole] = None
    is_active: Optional[bool] = None

class UserResponse(BaseSchema):
    id: str
    email: str
    full_name: str
    role: UserRole
    is_active: bool
    last_login: Optional[datetime] = None

# Authentication schemas
class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    email: Optional[str] = None

class UserLogin(BaseModel):
    email: EmailStr
    password: str

# Customer schemas (CRM)
class CustomerCreate(BaseModel):
    name: str
    email: Optional[EmailStr] = None
    phone: Optional[str] = None
    company: str
    industry: Optional[str] = None
    billing_address: Optional[str] = None
    notes: Optional[str] = None

class CustomerUpdate(BaseModel):
    name: Optional[str] = None
    email: Optional[EmailStr] = None
    phone: Optional[str] = None
    company: Optional[str] = None
    industry: Optional[str] = None
    status: Optional[CustomerStatus] = None
    billing_address: Optional[str] = None
    notes: Optional[str] = None

class CustomerResponse(BaseSchema):
    id: str
    name: str
    email: Optional[str] = None
    phone: Optional[str] = None
    company: str
    industry: Optional[str] = None
    status: CustomerStatus
    billing_address: Optional[str] = None
    notes: Optional[str] = None

# Lead schemas (CRM)
class LeadCreate(BaseModel):
    name: str
    email: Optional[EmailStr] = None
    phone: Optional[str] = None
    company: Optional[str] = None
    source: Optional[str] = None
    notes: Optional[str] = None
    assigned_to: Optional[str] = None

class LeadUpdate(BaseModel):
    name: Optional[str] = None
    email: Optional[EmailStr] = None
    phone: Optional[str] = None
    company: Optional[str] = None
    source: Optional[str] = None
    status: Optional[LeadStatus] = None
    notes: Optional[str] = None
    assigned_to: Optional[str] = None

class LeadResponse(BaseSchema):
    id: str
    name: str
    email: Optional[str] = None
    phone: Optional[str] = None
    company: Optional[str] = None
    source: Optional[str] = None
    status: LeadStatus
    notes: Optional[str] = None
    assigned_to: Optional[str] = None

# Employee schemas (HRMS)
class EmployeeCreate(BaseModel):
    employee_id: str
    full_name: str
    email: EmailStr
    phone: Optional[str] = None
    department_id: Optional[str] = None
    position: str
    hire_date: date
    salary: Optional[float] = None
    manager_id: Optional[str] = None

class EmployeeUpdate(BaseModel):
    full_name: Optional[str] = None
    email: Optional[EmailStr] = None
    phone: Optional[str] = None
    department_id: Optional[str] = None
    position: Optional[str] = None
    salary: Optional[float] = None
    status: Optional[EmployeeStatus] = None
    manager_id: Optional[str] = None

class EmployeeResponse(BaseSchema):
    id: str
    employee_id: str
    full_name: str
    email: str
    phone: Optional[str] = None
    department_id: Optional[str] = None
    position: str
    hire_date: date
    salary: Optional[float] = None
    status: EmployeeStatus
    manager_id: Optional[str] = None

# Leave Request schemas (HRMS)
class LeaveRequestCreate(BaseModel):
    leave_type: str
    start_date: date
    end_date: date
    reason: Optional[str] = None

class LeaveRequestUpdate(BaseModel):
    status: LeaveStatus
    approved_by: Optional[str] = None

class LeaveRequestResponse(BaseSchema):
    id: str
    employee_id: str
    leave_type: str
    start_date: date
    end_date: date
    days_requested: int
    reason: Optional[str] = None
    status: LeaveStatus
    approved_by: Optional[str] = None
    approved_at: Optional[datetime] = None

# Department schemas (HRMS)
class DepartmentCreate(BaseModel):
    name: str
    description: Optional[str] = None
    manager_id: Optional[str] = None

class DepartmentUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    manager_id: Optional[str] = None

class DepartmentResponse(BaseSchema):
    id: str
    name: str
    description: Optional[str] = None
    manager_id: Optional[str] = None

# Attendance schemas (HRMS)
class AttendanceCreate(BaseModel):
    employee_id: str
    check_in: datetime
    check_out: Optional[datetime] = None
    status: AttendanceStatus = AttendanceStatus.PRESENT

class AttendanceUpdate(BaseModel):
    check_out: Optional[datetime] = None
    status: Optional[AttendanceStatus] = None
    notes: Optional[str] = None

class AttendanceResponse(BaseSchema):
    id: str
    employee_id: str
    date: date
    check_in: datetime
    check_out: Optional[datetime] = None
    hours_worked: Optional[float] = None
    status: AttendanceStatus
    notes: Optional[str] = None