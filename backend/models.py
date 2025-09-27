from typing import Optional, List, Dict, Any
from datetime import datetime, date
from bson import ObjectId
from enum import Enum

# Import enums directly since we can't import from schemas
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

# Database models using Motor/PyMongo
class BaseModel:
    """Base model with common fields and methods"""
    
    def __init__(self, **data):
        for key, value in data.items():
            setattr(self, key, value)
        
        if not hasattr(self, 'created_at'):
            self.created_at = datetime.utcnow()
        if not hasattr(self, 'updated_at'):
            self.updated_at = datetime.utcnow()
    
    def to_dict(self):
        """Convert model to dictionary"""
        result = {}
        for key, value in self.__dict__.items():
            if isinstance(value, ObjectId):
                result[key] = str(value)
            elif isinstance(value, datetime):
                result[key] = value.isoformat()
            elif isinstance(value, date):
                result[key] = value.isoformat()
            else:
                result[key] = value
        return result

class UserModel(BaseModel):
    """User model for authentication and authorization"""
    collection_name = "users"
    
    def __init__(self, **data):
        super().__init__(**data)
        self._id = data.get('_id')
        self.id = data.get('id', str(ObjectId()))
        self.email: str = data.get('email')
        self.full_name: str = data.get('full_name')
        self.hashed_password: str = data.get('hashed_password')
        self.role: UserRole = data.get('role', UserRole.EMPLOYEE)
        self.is_active: bool = data.get('is_active', True)
        self.last_login: Optional[datetime] = data.get('last_login')

class ContactModel(BaseModel):
    """Contact model for CRM"""
    collection_name = "contacts"
    
    def __init__(self, **data):
        super().__init__(**data)
        self._id = data.get('_id')
        self.id = data.get('id', str(ObjectId()))
        self.name: str = data.get('name')
        self.email: Optional[str] = data.get('email')
        self.phone: Optional[str] = data.get('phone')
        self.company: Optional[str] = data.get('company')
        self.position: Optional[str] = data.get('position')
        self.notes: Optional[str] = data.get('notes')

class LeadModel(BaseModel):
    """Lead model for CRM"""
    collection_name = "leads"
    
    def __init__(self, **data):
        super().__init__(**data)
        self._id = data.get('_id')
        self.id = data.get('id', str(ObjectId()))
        self.title: str = data.get('title')
        self.description: Optional[str] = data.get('description')
        self.status: LeadStatus = data.get('status', LeadStatus.NEW)
        self.source: Optional[str] = data.get('source')
        self.estimated_value: Optional[float] = data.get('estimated_value')
        self.expected_close_date: Optional[date] = data.get('expected_close_date')
        self.contact_id: Optional[str] = data.get('contact_id')
        self.assigned_to: Optional[str] = data.get('assigned_to')

class CustomerModel(BaseModel):
    """Customer model for CRM"""
    collection_name = "customers"
    
    def __init__(self, **data):
        super().__init__(**data)
        self._id = data.get('_id')
        self.id = data.get('id', str(ObjectId()))
        self.name: str = data.get('name')
        self.email: Optional[str] = data.get('email')
        self.phone: Optional[str] = data.get('phone')
        self.company: str = data.get('company')
        self.industry: Optional[str] = data.get('industry')
        self.status: CustomerStatus = data.get('status', CustomerStatus.PROSPECT)
        self.billing_address: Optional[str] = data.get('billing_address')
        self.notes: Optional[str] = data.get('notes')

class DepartmentModel(BaseModel):
    """Department model for HRMS"""
    collection_name = "departments"
    
    def __init__(self, **data):
        super().__init__(**data)
        self._id = data.get('_id')
        self.id = data.get('id', str(ObjectId()))
        self.name: str = data.get('name')
        self.description: Optional[str] = data.get('description')
        self.manager_id: Optional[str] = data.get('manager_id')

class EmployeeModel(BaseModel):
    """Employee model for HRMS"""
    collection_name = "employees"
    
    def __init__(self, **data):
        super().__init__(**data)
        self._id = data.get('_id')
        self.id = data.get('id', str(ObjectId()))
        self.employee_id: str = data.get('employee_id')  # Company employee ID
        self.user_id: Optional[str] = data.get('user_id')  # Link to User account
        self.first_name: str = data.get('first_name')
        self.last_name: str = data.get('last_name')
        self.email: str = data.get('email')
        self.phone: Optional[str] = data.get('phone')
        self.date_of_birth: Optional[date] = data.get('date_of_birth')
        self.hire_date: date = data.get('hire_date')
        self.department_id: Optional[str] = data.get('department_id')
        self.position: str = data.get('position')
        self.salary: Optional[float] = data.get('salary')
        self.manager_id: Optional[str] = data.get('manager_id')
        self.status: EmployeeStatus = data.get('status', EmployeeStatus.ACTIVE)
        self.address: Optional[str] = data.get('address')
        self.emergency_contact: Optional[Dict[str, Any]] = data.get('emergency_contact')

class AttendanceModel(BaseModel):
    """Attendance model for HRMS"""
    collection_name = "attendance"
    
    def __init__(self, **data):
        super().__init__(**data)
        self._id = data.get('_id')
        self.id = data.get('id', str(ObjectId()))
        self.employee_id: str = data.get('employee_id')
        self.date: date = data.get('date')
        self.check_in: Optional[datetime] = data.get('check_in')
        self.check_out: Optional[datetime] = data.get('check_out')
        self.status: AttendanceStatus = data.get('status', AttendanceStatus.PRESENT)
        self.hours_worked: Optional[float] = data.get('hours_worked')
        self.notes: Optional[str] = data.get('notes')

class LeaveRequestModel(BaseModel):
    """Leave request model for HRMS"""
    collection_name = "leave_requests"
    
    def __init__(self, **data):
        super().__init__(**data)
        self._id = data.get('_id')
        self.id = data.get('id', str(ObjectId()))
        self.employee_id: str = data.get('employee_id')
        self.leave_type: str = data.get('leave_type')  # Annual, Sick, Personal, etc.
        self.start_date: date = data.get('start_date')
        self.end_date: date = data.get('end_date')
        self.days_requested: int = data.get('days_requested')
        self.reason: Optional[str] = data.get('reason')
        self.status: LeaveStatus = data.get('status', LeaveStatus.PENDING)
        self.approved_by: Optional[str] = data.get('approved_by')
        self.approved_at: Optional[datetime] = data.get('approved_at')

# Database indexes for better performance
DATABASE_INDEXES = {
    "users": [
        {"key": [("email", 1)], "unique": True},
        {"key": [("role", 1)]},
        {"key": [("is_active", 1)]},
    ],
    "contacts": [
        {"key": [("email", 1)]},
        {"key": [("company", 1)]},
        {"key": [("name", "text")]},
    ],
    "leads": [
        {"key": [("status", 1)]},
        {"key": [("assigned_to", 1)]},
        {"key": [("contact_id", 1)]},
        {"key": [("expected_close_date", 1)]},
        {"key": [("created_at", -1)]},
    ],
    "customers": [
        {"key": [("email", 1)]},
        {"key": [("company", 1)]},
        {"key": [("status", 1)]},
        {"key": [("name", "text")]},
    ],
    "departments": [
        {"key": [("name", 1)], "unique": True},
        {"key": [("manager_id", 1)]},
    ],
    "employees": [
        {"key": [("employee_id", 1)], "unique": True},
        {"key": [("email", 1)], "unique": True},
        {"key": [("user_id", 1)]},
        {"key": [("department_id", 1)]},
        {"key": [("manager_id", 1)]},
        {"key": [("status", 1)]},
        {"key": [("hire_date", 1)]},
    ],
    "attendance": [
        {"key": [("employee_id", 1), ("date", 1)], "unique": True},
        {"key": [("date", -1)]},
        {"key": [("status", 1)]},
    ],
    "leave_requests": [
        {"key": [("employee_id", 1)]},
        {"key": [("status", 1)]},
        {"key": [("start_date", 1)]},
        {"key": [("approved_by", 1)]},
        {"key": [("created_at", -1)]},
    ]
}