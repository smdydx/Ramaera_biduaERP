from pydantic import BaseModel, Field, EmailStr
from typing import Optional, List, Dict, Any
from datetime import datetime, date
from enum import Enum
import uuid

# Enums for various status types
class UserRole(str, Enum):
    ADMIN = "admin"
    HR_MANAGER = "hr_manager" 
    SALES_TEAM = "sales_team"
    EMPLOYEE = "employee"

class LeadStatus(str, Enum):
    NEW = "new"
    CONTACTED = "contacted"
    QUALIFIED = "qualified"
    PROPOSAL = "proposal"
    NEGOTIATION = "negotiation"
    CLOSED_WON = "closed_won"
    CLOSED_LOST = "closed_lost"

class CustomerStatus(str, Enum):
    ACTIVE = "active"
    INACTIVE = "inactive"
    PROSPECT = "prospect"

class EmployeeStatus(str, Enum):
    ACTIVE = "active"
    INACTIVE = "inactive"
    TERMINATED = "terminated"

class LeaveStatus(str, Enum):
    PENDING = "pending"
    APPROVED = "approved"
    REJECTED = "rejected"
    CANCELLED = "cancelled"

class AttendanceStatus(str, Enum):
    PRESENT = "present"
    ABSENT = "absent"
    HALF_DAY = "half_day"
    LATE = "late"

# Base schemas
class TimestampMixin(BaseModel):
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

# User and Authentication Schemas
class UserBase(BaseModel):
    email: EmailStr
    full_name: str
    role: UserRole
    is_active: bool = True

class UserCreate(UserBase):
    password: str

class UserUpdate(BaseModel):
    email: Optional[EmailStr] = None
    full_name: Optional[str] = None
    role: Optional[UserRole] = None
    is_active: Optional[bool] = None

class User(UserBase, TimestampMixin):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    last_login: Optional[datetime] = None

class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"
    expires_in: int
    user: User

# CRM Schemas
class ContactBase(BaseModel):
    name: str
    email: Optional[EmailStr] = None
    phone: Optional[str] = None
    company: Optional[str] = None
    position: Optional[str] = None
    notes: Optional[str] = None

class ContactCreate(ContactBase):
    pass

class ContactUpdate(BaseModel):
    name: Optional[str] = None
    email: Optional[EmailStr] = None
    phone: Optional[str] = None
    company: Optional[str] = None
    position: Optional[str] = None
    notes: Optional[str] = None

class Contact(ContactBase, TimestampMixin):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))

class LeadBase(BaseModel):
    title: str
    description: Optional[str] = None
    status: LeadStatus = LeadStatus.NEW
    source: Optional[str] = None
    estimated_value: Optional[float] = None
    expected_close_date: Optional[date] = None
    contact_id: Optional[str] = None
    assigned_to: Optional[str] = None  # User ID

class LeadCreate(LeadBase):
    pass

class LeadUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    status: Optional[LeadStatus] = None
    source: Optional[str] = None
    estimated_value: Optional[float] = None
    expected_close_date: Optional[date] = None
    contact_id: Optional[str] = None
    assigned_to: Optional[str] = None

class Lead(LeadBase, TimestampMixin):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    contact: Optional[Contact] = None

class CustomerBase(BaseModel):
    name: str
    email: Optional[EmailStr] = None
    phone: Optional[str] = None
    company: str
    industry: Optional[str] = None
    status: CustomerStatus = CustomerStatus.PROSPECT
    billing_address: Optional[str] = None
    notes: Optional[str] = None

class CustomerCreate(CustomerBase):
    pass

class CustomerUpdate(BaseModel):
    name: Optional[str] = None
    email: Optional[EmailStr] = None
    phone: Optional[str] = None
    company: Optional[str] = None
    industry: Optional[str] = None
    status: Optional[CustomerStatus] = None
    billing_address: Optional[str] = None
    notes: Optional[str] = None

class Customer(CustomerBase, TimestampMixin):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))

# HRMS Schemas
class DepartmentBase(BaseModel):
    name: str
    description: Optional[str] = None
    manager_id: Optional[str] = None

class DepartmentCreate(DepartmentBase):
    pass

class DepartmentUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    manager_id: Optional[str] = None

class Department(DepartmentBase, TimestampMixin):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))

class EmployeeBase(BaseModel):
    employee_id: str  # Company employee ID
    first_name: str
    last_name: str
    email: EmailStr
    phone: Optional[str] = None
    date_of_birth: Optional[date] = None
    hire_date: date
    department_id: Optional[str] = None
    position: str
    salary: Optional[float] = None
    manager_id: Optional[str] = None
    status: EmployeeStatus = EmployeeStatus.ACTIVE
    address: Optional[str] = None
    emergency_contact: Optional[Dict[str, Any]] = None

class EmployeeCreate(EmployeeBase):
    user_id: Optional[str] = None  # Link to User account

class EmployeeUpdate(BaseModel):
    employee_id: Optional[str] = None
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    email: Optional[EmailStr] = None
    phone: Optional[str] = None
    date_of_birth: Optional[date] = None
    hire_date: Optional[date] = None
    department_id: Optional[str] = None
    position: Optional[str] = None
    salary: Optional[float] = None
    manager_id: Optional[str] = None
    status: Optional[EmployeeStatus] = None
    address: Optional[str] = None
    emergency_contact: Optional[Dict[str, Any]] = None

class Employee(EmployeeBase, TimestampMixin):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    user_id: Optional[str] = None
    department: Optional[Department] = None

class AttendanceBase(BaseModel):
    employee_id: str
    date: date
    check_in: Optional[datetime] = None
    check_out: Optional[datetime] = None
    status: AttendanceStatus = AttendanceStatus.PRESENT
    hours_worked: Optional[float] = None
    notes: Optional[str] = None

class AttendanceCreate(AttendanceBase):
    pass

class AttendanceUpdate(BaseModel):
    check_in: Optional[datetime] = None
    check_out: Optional[datetime] = None
    status: Optional[AttendanceStatus] = None
    hours_worked: Optional[float] = None
    notes: Optional[str] = None

class Attendance(AttendanceBase, TimestampMixin):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    employee: Optional[Employee] = None

class LeaveRequestBase(BaseModel):
    employee_id: str
    leave_type: str  # Annual, Sick, Personal, etc.
    start_date: date
    end_date: date
    days_requested: int
    reason: Optional[str] = None
    status: LeaveStatus = LeaveStatus.PENDING
    approved_by: Optional[str] = None  # User ID
    approved_at: Optional[datetime] = None

class LeaveRequestCreate(LeaveRequestBase):
    pass

class LeaveRequestUpdate(BaseModel):
    leave_type: Optional[str] = None
    start_date: Optional[date] = None
    end_date: Optional[date] = None
    days_requested: Optional[int] = None
    reason: Optional[str] = None
    status: Optional[LeaveStatus] = None
    approved_by: Optional[str] = None
    approved_at: Optional[datetime] = None

class LeaveRequest(LeaveRequestBase, TimestampMixin):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    employee: Optional[Employee] = None

# Dashboard and Analytics Schemas
class CRMDashboard(BaseModel):
    total_leads: int
    leads_by_status: Dict[str, int]
    total_customers: int
    customers_by_status: Dict[str, int]
    revenue_pipeline: float
    recent_activities: List[Dict[str, Any]]

class HRMSDashboard(BaseModel):
    total_employees: int
    employees_by_department: Dict[str, int]
    employees_by_status: Dict[str, int]
    pending_leave_requests: int
    attendance_summary: Dict[str, Any]
    recent_activities: List[Dict[str, Any]]

# Response schemas
class ResponseBase(BaseModel):
    success: bool
    message: str
    data: Optional[Any] = None

class PaginatedResponse(ResponseBase):
    total: int
    page: int
    per_page: int
    pages: int