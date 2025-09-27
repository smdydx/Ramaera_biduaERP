
from fastapi import APIRouter, Depends, HTTPException, status, Query
from typing import List, Optional
from app.schemas.schemas import DepartmentCreate, DepartmentUpdate, DepartmentResponse
from app.models.models import DepartmentModel
from app.utils.database import DatabaseUtils
from app.middleware.auth import get_current_user

router = APIRouter()

@router.get("/", response_model=List[DepartmentResponse])
async def get_departments(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    current_user = Depends(get_current_user)
):
    """Get all departments with pagination"""
    departments = await DatabaseUtils.find_many(
        DepartmentModel.collection_name,
        {},
        skip=skip,
        limit=limit
    )
    
    return [DepartmentResponse(**dept) for dept in departments]

@router.get("/{department_id}", response_model=DepartmentResponse)
async def get_department(department_id: str, current_user = Depends(get_current_user)):
    """Get department by ID"""
    department = await DatabaseUtils.find_by_id(DepartmentModel.collection_name, department_id)
    if not department:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Department not found"
        )
    return DepartmentResponse(**department)

@router.post("/", response_model=DepartmentResponse)
async def create_department(
    department: DepartmentCreate,
    current_user = Depends(get_current_user)
):
    """Create a new department"""
    department_model = DepartmentModel(**department.dict())
    result = await DatabaseUtils.create(DepartmentModel.collection_name, department_model.to_dict())
    
    created_dept = await DatabaseUtils.find_by_id(
        DepartmentModel.collection_name,
        str(result.inserted_id)
    )
    return DepartmentResponse(**created_dept)
