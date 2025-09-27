
from fastapi import APIRouter, Depends, HTTPException, status, Query
from typing import List, Optional
from datetime import date
from ...schemas.schemas import EmployeeCreate, EmployeeUpdate, EmployeeResponse
from ...models.models import EmployeeModel
from ...utils.database import DatabaseUtils
from ...middleware.auth import get_current_user

router = APIRouter()

@router.get("/", response_model=List[EmployeeResponse])
async def get_employees(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    department_id: Optional[str] = None,
    status_filter: Optional[str] = None,
    current_user = Depends(get_current_user)
):
    """Get all employees with filtering and pagination"""
    filters = {}
    if department_id:
        filters["department_id"] = department_id
    if status_filter:
        filters["status"] = status_filter
    
    employees = await DatabaseUtils.find_many(
        EmployeeModel.collection_name,
        filters,
        skip=skip,
        limit=limit
    )
    
    return [EmployeeResponse(**employee) for employee in employees]

@router.get("/{employee_id}", response_model=EmployeeResponse)
async def get_employee(employee_id: str, current_user = Depends(get_current_user)):
    """Get employee by ID"""
    employee = await DatabaseUtils.find_by_id(EmployeeModel.collection_name, employee_id)
    if not employee:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Employee not found"
        )
    return EmployeeResponse(**employee)

@router.post("/", response_model=EmployeeResponse)
async def create_employee(
    employee: EmployeeCreate,
    current_user = Depends(get_current_user)
):
    """Create a new employee"""
    # Check if employee ID already exists
    existing_employee = await DatabaseUtils.find_one(
        EmployeeModel.collection_name,
        {"employee_id": employee.employee_id}
    )
    if existing_employee:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Employee ID already exists"
        )
    
    employee_model = EmployeeModel(**employee.dict())
    result = await DatabaseUtils.create(EmployeeModel.collection_name, employee_model.to_dict())
    
    created_employee = await DatabaseUtils.find_by_id(
        EmployeeModel.collection_name,
        str(result.inserted_id)
    )
    return EmployeeResponse(**created_employee)

@router.put("/{employee_id}", response_model=EmployeeResponse)
async def update_employee(
    employee_id: str,
    employee_update: EmployeeUpdate,
    current_user = Depends(get_current_user)
):
    """Update employee"""
    existing_employee = await DatabaseUtils.find_by_id(EmployeeModel.collection_name, employee_id)
    if not existing_employee:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Employee not found"
        )
    
    update_data = employee_update.dict(exclude_unset=True)
    if update_data:
        await DatabaseUtils.update_by_id(EmployeeModel.collection_name, employee_id, update_data)
    
    updated_employee = await DatabaseUtils.find_by_id(EmployeeModel.collection_name, employee_id)
    return EmployeeResponse(**updated_employee)

@router.get("/stats/overview")
async def get_employee_stats(current_user = Depends(get_current_user)):
    """Get employee statistics"""
    total_employees = await DatabaseUtils.count_documents(EmployeeModel.collection_name)
    active_employees = await DatabaseUtils.count_documents(
        EmployeeModel.collection_name,
        {"status": "active"}
    )
    
    return {
        "total_employees": total_employees,
        "active_employees": active_employees,
        "terminated_employees": await DatabaseUtils.count_documents(
            EmployeeModel.collection_name,
            {"status": "terminated"}
        )
    }

@router.get("/department/{department_id}", response_model=List[EmployeeResponse])
async def get_employees_by_department(
    department_id: str,
    current_user = Depends(get_current_user)
):
    """Get all employees in a specific department"""
    employees = await DatabaseUtils.find_many(
        EmployeeModel.collection_name,
        {"department_id": department_id}
    )
    return [EmployeeResponse(**employee) for employee in employees]
