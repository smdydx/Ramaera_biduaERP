from sqlalchemy import Column, Integer, String, DateTime, Boolean, Text, ForeignKey, Date, Time, Enum, DECIMAL
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from datetime import datetime, date
import enum
from ..core.database import Base

# Enums for better data integrity
class UserRole(enum.Enum):
    ADMIN = "admin"
    HR_MANAGER = "hr_manager"
    SALES_MANAGER = "sales_manager"
    SALES_REP = "sales_rep"
    EMPLOYEE = "employee"
    MANAGER = "manager"

class LeadStatus(enum.Enum):
    NEW = "new"
    CONTACTED = "contacted"
    QUALIFIED = "qualified"
    PROPOSAL = "proposal"
    NEGOTIATION = "negotiation"
    CLOSED_WON = "closed_won"
    CLOSED_LOST = "closed_lost"

class CustomerStatus(enum.Enum):
    ACTIVE = "active"
    INACTIVE = "inactive"
    PROSPECT = "prospect"
    CHURNED = "churned"

class DealStage(enum.Enum):
    PROSPECTING = "prospecting"
    QUALIFICATION = "qualification"
    NEEDS_ANALYSIS = "needs_analysis"
    VALUE_PROPOSITION = "value_proposition"
    PROPOSAL = "proposal"
    NEGOTIATION = "negotiation"
    CLOSED_WON = "closed_won"
    CLOSED_LOST = "closed_lost"

class LeaveType(enum.Enum):
    ANNUAL = "annual"
    SICK = "sick"
    MATERNITY = "maternity"
    PATERNITY = "paternity"
    PERSONAL = "personal"
    EMERGENCY = "emergency"
    UNPAID = "unpaid"

class LeaveStatus(enum.Enum):
    PENDING = "pending"
    APPROVED = "approved"
    REJECTED = "rejected"
    CANCELLED = "cancelled"

class AttendanceStatus(enum.Enum):
    PRESENT = "present"
    ABSENT = "absent"
    LATE = "late"
    HALF_DAY = "half_day"
    WFH = "work_from_home"

class EmployeeStatus(enum.Enum):
    ACTIVE = "active"
    INACTIVE = "inactive"
    TERMINATED = "terminated"
    ON_LEAVE = "on_leave"

# Authentication Models
class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(255), unique=True, index=True, nullable=False)
    username = Column(String(100), unique=True, index=True, nullable=False)
    hashed_password = Column(String(255), nullable=False)
    full_name = Column(String(255), nullable=False)
    phone = Column(String(20))
    role = Column(Enum(UserRole), nullable=False, default=UserRole.EMPLOYEE)
    is_active = Column(Boolean, default=True)
    is_verified = Column(Boolean, default=False)
    last_login = Column(DateTime(timezone=True))
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationships
    employee_profile = relationship("Employee", back_populates="user", uselist=False)
    created_leads = relationship("Lead", back_populates="created_by")
    assigned_leads = relationship("Lead", foreign_keys="Lead.assigned_to_id", back_populates="assigned_to")
    created_customers = relationship("Customer", back_populates="created_by")
    created_deals = relationship("Deal", back_populates="created_by")
    assigned_deals = relationship("Deal", foreign_keys="Deal.assigned_to_id", back_populates="assigned_to")

# Company/Organization Models
class Company(Base):
    __tablename__ = "companies"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    domain = Column(String(100))
    industry = Column(String(100))
    size = Column(String(50))  # Small, Medium, Large, Enterprise
    website = Column(String(255))
    phone = Column(String(20))
    email = Column(String(255))
    address = Column(Text)
    city = Column(String(100))
    state = Column(String(100))
    country = Column(String(100))
    postal_code = Column(String(20))
    annual_revenue = Column(DECIMAL(15, 2))
    logo_url = Column(String(500))
    description = Column(Text)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationships
    customers = relationship("Customer", back_populates="company")
    leads = relationship("Lead", back_populates="company")
    contacts = relationship("Contact", back_populates="company")

# CRM Models
class Lead(Base):
    __tablename__ = "leads"
    
    id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String(100), nullable=False)
    last_name = Column(String(100), nullable=False)
    email = Column(String(255), nullable=False, index=True)
    phone = Column(String(20))
    job_title = Column(String(255))
    company_id = Column(Integer, ForeignKey("companies.id"))
    source = Column(String(100))  # Website, Referral, Cold Call, etc.
    status = Column(Enum(LeadStatus), default=LeadStatus.NEW)
    score = Column(Integer, default=0)  # Lead scoring 0-100
    estimated_value = Column(DECIMAL(12, 2))
    expected_close_date = Column(Date)
    notes = Column(Text)
    created_by_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    assigned_to_id = Column(Integer, ForeignKey("users.id"))
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationships
    company = relationship("Company", back_populates="leads")
    created_by = relationship("User", foreign_keys=[created_by_id], back_populates="created_leads")
    assigned_to = relationship("User", foreign_keys=[assigned_to_id], back_populates="assigned_leads")
    activities = relationship("Activity", back_populates="lead")

class Customer(Base):
    __tablename__ = "customers"
    
    id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String(100), nullable=False)
    last_name = Column(String(100), nullable=False)
    email = Column(String(255), nullable=False, unique=True, index=True)
    phone = Column(String(20))
    mobile = Column(String(20))
    job_title = Column(String(255))
    company_id = Column(Integer, ForeignKey("companies.id"))
    status = Column(Enum(CustomerStatus), default=CustomerStatus.PROSPECT)
    customer_type = Column(String(50))  # Individual, Business
    priority = Column(String(20), default="Medium")  # High, Medium, Low
    lifetime_value = Column(DECIMAL(15, 2), default=0)
    total_purchases = Column(DECIMAL(15, 2), default=0)
    last_contact_date = Column(DateTime(timezone=True))
    preferred_contact_method = Column(String(50))
    billing_address = Column(Text)
    shipping_address = Column(Text)
    notes = Column(Text)
    tags = Column(Text)  # JSON string for flexibility
    created_by_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationships
    company = relationship("Company", back_populates="customers")
    created_by = relationship("User", back_populates="created_customers")
    deals = relationship("Deal", back_populates="customer")
    activities = relationship("Activity", back_populates="customer")

class Deal(Base):
    __tablename__ = "deals"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    customer_id = Column(Integer, ForeignKey("customers.id"), nullable=False)
    stage = Column(Enum(DealStage), default=DealStage.PROSPECTING)
    value = Column(DECIMAL(12, 2), nullable=False)
    probability = Column(Integer, default=10)  # 0-100%
    expected_close_date = Column(Date)
    actual_close_date = Column(Date)
    description = Column(Text)
    next_step = Column(String(500))
    competition = Column(String(255))
    decision_maker = Column(String(255))
    budget_confirmed = Column(Boolean, default=False)
    authority_confirmed = Column(Boolean, default=False)
    need_confirmed = Column(Boolean, default=False)
    timeline_confirmed = Column(Boolean, default=False)
    created_by_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    assigned_to_id = Column(Integer, ForeignKey("users.id"))
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationships
    customer = relationship("Customer", back_populates="deals")
    created_by = relationship("User", foreign_keys=[created_by_id], back_populates="created_deals")
    assigned_to = relationship("User", foreign_keys=[assigned_to_id], back_populates="assigned_deals")
    activities = relationship("Activity", back_populates="deal")

class Contact(Base):
    __tablename__ = "contacts"
    
    id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String(100), nullable=False)
    last_name = Column(String(100), nullable=False)
    email = Column(String(255), nullable=False, index=True)
    phone = Column(String(20))
    mobile = Column(String(20))
    job_title = Column(String(255))
    department = Column(String(100))
    company_id = Column(Integer, ForeignKey("companies.id"))
    is_primary = Column(Boolean, default=False)
    is_decision_maker = Column(Boolean, default=False)
    linkedin_url = Column(String(500))
    twitter_handle = Column(String(100))
    birthday = Column(Date)
    notes = Column(Text)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationships
    company = relationship("Company", back_populates="contacts")
    activities = relationship("Activity", back_populates="contact")

# Activity/Communication Log
class Activity(Base):
    __tablename__ = "activities"
    
    id = Column(Integer, primary_key=True, index=True)
    type = Column(String(50), nullable=False)  # Call, Email, Meeting, Note, Task
    subject = Column(String(255), nullable=False)
    description = Column(Text)
    outcome = Column(String(100))
    duration_minutes = Column(Integer)
    scheduled_date = Column(DateTime(timezone=True))
    completed_date = Column(DateTime(timezone=True))
    is_completed = Column(Boolean, default=False)
    priority = Column(String(20), default="Medium")
    
    # Related entities
    lead_id = Column(Integer, ForeignKey("leads.id"))
    customer_id = Column(Integer, ForeignKey("customers.id"))
    deal_id = Column(Integer, ForeignKey("deals.id"))
    contact_id = Column(Integer, ForeignKey("contacts.id"))
    
    created_by_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationships
    lead = relationship("Lead", back_populates="activities")
    customer = relationship("Customer", back_populates="activities")
    deal = relationship("Deal", back_populates="activities")
    contact = relationship("Contact", back_populates="activities")
    created_by = relationship("User")

# HRMS Models
class Department(Base):
    __tablename__ = "departments"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False, unique=True)
    code = Column(String(20), unique=True)
    description = Column(Text)
    manager_id = Column(Integer, ForeignKey("employees.id"))
    budget = Column(DECIMAL(12, 2))
    location = Column(String(255))
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationships
    employees = relationship("Employee", back_populates="department")
    manager = relationship("Employee", foreign_keys=[manager_id])

class Employee(Base):
    __tablename__ = "employees"
    
    id = Column(Integer, primary_key=True, index=True)
    employee_id = Column(String(50), unique=True, nullable=False, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), unique=True)
    first_name = Column(String(100), nullable=False)
    last_name = Column(String(100), nullable=False)
    email = Column(String(255), nullable=False, unique=True)
    phone = Column(String(20))
    emergency_contact_name = Column(String(255))
    emergency_contact_phone = Column(String(20))
    
    # Job Information
    job_title = Column(String(255), nullable=False)
    department_id = Column(Integer, ForeignKey("departments.id"))
    manager_id = Column(Integer, ForeignKey("employees.id"))
    hire_date = Column(Date, nullable=False)
    termination_date = Column(Date)
    employment_type = Column(String(50))  # Full-time, Part-time, Contract, Intern
    status = Column(Enum(EmployeeStatus), default=EmployeeStatus.ACTIVE)
    
    # Personal Information
    date_of_birth = Column(Date)
    gender = Column(String(20))
    marital_status = Column(String(20))
    nationality = Column(String(50))
    address = Column(Text)
    city = Column(String(100))
    state = Column(String(100))
    country = Column(String(100))
    postal_code = Column(String(20))
    
    # Compensation
    salary = Column(DECIMAL(10, 2))
    hourly_rate = Column(DECIMAL(8, 2))
    currency = Column(String(10), default="USD")
    pay_frequency = Column(String(20))  # Weekly, Bi-weekly, Monthly
    
    # Additional Info
    skills = Column(Text)  # JSON string
    education = Column(Text)  # JSON string
    certifications = Column(Text)  # JSON string
    notes = Column(Text)
    profile_picture_url = Column(String(500))
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationships
    user = relationship("User", back_populates="employee_profile")
    department = relationship("Department", back_populates="employees")
    manager = relationship("Employee", remote_side=[id])
    direct_reports = relationship("Employee")
    attendance_records = relationship("Attendance", back_populates="employee")
    leave_requests = relationship("LeaveRequest", back_populates="employee")
    performance_reviews = relationship("PerformanceReview", back_populates="employee")
    payroll_records = relationship("PayrollRecord", back_populates="employee")

class Attendance(Base):
    __tablename__ = "attendance"
    
    id = Column(Integer, primary_key=True, index=True)
    employee_id = Column(Integer, ForeignKey("employees.id"), nullable=False)
    date = Column(Date, nullable=False)
    check_in_time = Column(Time)
    check_out_time = Column(Time)
    break_time_minutes = Column(Integer, default=0)
    total_hours = Column(DECIMAL(4, 2))
    overtime_hours = Column(DECIMAL(4, 2), default=0)
    status = Column(Enum(AttendanceStatus), default=AttendanceStatus.PRESENT)
    location = Column(String(255))  # Office, Home, Client Site
    ip_address = Column(String(45))
    notes = Column(Text)
    approved_by_id = Column(Integer, ForeignKey("employees.id"))
    approved_at = Column(DateTime(timezone=True))
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationships
    employee = relationship("Employee", back_populates="attendance_records")
    approved_by = relationship("Employee", foreign_keys=[approved_by_id])

class LeaveRequest(Base):
    __tablename__ = "leave_requests"
    
    id = Column(Integer, primary_key=True, index=True)
    employee_id = Column(Integer, ForeignKey("employees.id"), nullable=False)
    leave_type = Column(Enum(LeaveType), nullable=False)
    start_date = Column(Date, nullable=False)
    end_date = Column(Date, nullable=False)
    total_days = Column(Integer, nullable=False)
    reason = Column(Text, nullable=False)
    status = Column(Enum(LeaveStatus), default=LeaveStatus.PENDING)
    approved_by_id = Column(Integer, ForeignKey("employees.id"))
    approved_at = Column(DateTime(timezone=True))
    rejection_reason = Column(Text)
    emergency_contact = Column(String(255))
    substitute_employee_id = Column(Integer, ForeignKey("employees.id"))
    documents_url = Column(Text)  # JSON array of document URLs
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationships
    employee = relationship("Employee", back_populates="leave_requests")
    approved_by = relationship("Employee", foreign_keys=[approved_by_id])
    substitute = relationship("Employee", foreign_keys=[substitute_employee_id])

class PerformanceReview(Base):
    __tablename__ = "performance_reviews"
    
    id = Column(Integer, primary_key=True, index=True)
    employee_id = Column(Integer, ForeignKey("employees.id"), nullable=False)
    reviewer_id = Column(Integer, ForeignKey("employees.id"), nullable=False)
    review_period_start = Column(Date, nullable=False)
    review_period_end = Column(Date, nullable=False)
    overall_rating = Column(DECIMAL(3, 2))  # 0.00 - 5.00
    goals_achievement = Column(DECIMAL(3, 2))
    technical_skills = Column(DECIMAL(3, 2))
    communication_skills = Column(DECIMAL(3, 2))
    teamwork = Column(DECIMAL(3, 2))
    leadership = Column(DECIMAL(3, 2))
    initiative = Column(DECIMAL(3, 2))
    strengths = Column(Text)
    areas_for_improvement = Column(Text)
    goals_next_period = Column(Text)
    employee_comments = Column(Text)
    reviewer_comments = Column(Text)
    hr_comments = Column(Text)
    status = Column(String(20), default="Draft")  # Draft, In Progress, Completed
    submitted_at = Column(DateTime(timezone=True))
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationships
    employee = relationship("Employee", back_populates="performance_reviews")
    reviewer = relationship("Employee", foreign_keys=[reviewer_id])

class PayrollRecord(Base):
    __tablename__ = "payroll_records"
    
    id = Column(Integer, primary_key=True, index=True)
    employee_id = Column(Integer, ForeignKey("employees.id"), nullable=False)
    pay_period_start = Column(Date, nullable=False)
    pay_period_end = Column(Date, nullable=False)
    
    # Earnings
    base_salary = Column(DECIMAL(10, 2), nullable=False)
    overtime_pay = Column(DECIMAL(10, 2), default=0)
    bonus = Column(DECIMAL(10, 2), default=0)
    commission = Column(DECIMAL(10, 2), default=0)
    allowances = Column(DECIMAL(10, 2), default=0)
    gross_pay = Column(DECIMAL(10, 2), nullable=False)
    
    # Deductions
    tax_deduction = Column(DECIMAL(10, 2), default=0)
    social_security = Column(DECIMAL(10, 2), default=0)
    health_insurance = Column(DECIMAL(10, 2), default=0)
    retirement_contribution = Column(DECIMAL(10, 2), default=0)
    other_deductions = Column(DECIMAL(10, 2), default=0)
    total_deductions = Column(DECIMAL(10, 2), default=0)
    
    net_pay = Column(DECIMAL(10, 2), nullable=False)
    
    # Hours
    regular_hours = Column(DECIMAL(5, 2), default=0)
    overtime_hours = Column(DECIMAL(5, 2), default=0)
    
    payment_date = Column(Date)
    payment_method = Column(String(50))  # Bank Transfer, Check, Cash
    bank_account = Column(String(100))
    
    notes = Column(Text)
    processed_by_id = Column(Integer, ForeignKey("employees.id"))
    processed_at = Column(DateTime(timezone=True))
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationships
    employee = relationship("Employee", back_populates="payroll_records")
    processed_by = relationship("Employee", foreign_keys=[processed_by_id])

# Notification System
class Notification(Base):
    __tablename__ = "notifications"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    title = Column(String(255), nullable=False)
    message = Column(Text, nullable=False)
    type = Column(String(50), nullable=False)  # info, warning, error, success
    is_read = Column(Boolean, default=False)
    action_url = Column(String(500))
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    read_at = Column(DateTime(timezone=True))
    
    # Relationships
    user = relationship("User")

# Document Management
class Document(Base):
    __tablename__ = "documents"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    file_path = Column(String(500), nullable=False)
    file_size = Column(Integer)
    file_type = Column(String(50))
    description = Column(Text)
    category = Column(String(100))  # Contract, Invoice, HR Document, etc.
    
    # Related entities
    employee_id = Column(Integer, ForeignKey("employees.id"))
    customer_id = Column(Integer, ForeignKey("customers.id"))
    deal_id = Column(Integer, ForeignKey("deals.id"))
    
    uploaded_by_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    is_confidential = Column(Boolean, default=False)
    expires_at = Column(DateTime(timezone=True))
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationships
    employee = relationship("Employee")
    customer = relationship("Customer")
    deal = relationship("Deal")
    uploaded_by = relationship("User")

# System Settings
class SystemSetting(Base):
    __tablename__ = "system_settings"
    
    id = Column(Integer, primary_key=True, index=True)
    key = Column(String(100), unique=True, nullable=False)
    value = Column(Text)
    description = Column(Text)
    category = Column(String(50))  # General, Email, Security, etc.
    is_encrypted = Column(Boolean, default=False)
    updated_by_id = Column(Integer, ForeignKey("users.id"))
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationships
    updated_by = relationship("User")