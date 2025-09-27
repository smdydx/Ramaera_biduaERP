
from fastapi import APIRouter, Depends, HTTPException, status
from typing import List, Optional
from ....schemas.schemas import CustomerCreate, CustomerUpdate, CustomerResponse
from ....utils.database import DatabaseUtils
from ....models.models import CustomerModel
from ....core.database import get_database

router = APIRouter()

@router.post("/", response_model=CustomerResponse)
async def create_customer(customer_data: CustomerCreate, db = Depends(get_database)):
    """Create a new customer"""
    if not db:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Database not available"
        )
    
    customer_dict = customer_data.model_dump()
    customer_id = await DatabaseUtils.insert_one(CustomerModel.collection_name, customer_dict)
    
    if customer_id:
        created_customer = await DatabaseUtils.find_by_id(CustomerModel.collection_name, customer_id)
        return CustomerResponse(**created_customer)
    
    raise HTTPException(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        detail="Failed to create customer"
    )

@router.get("/", response_model=List[CustomerResponse])
async def get_customers(
    skip: int = 0, 
    limit: int = 100,
    status: Optional[str] = None,
    db = Depends(get_database)
):
    """Get all customers with optional filtering"""
    if not db:
        return []
    
    filter_dict = {}
    if status:
        filter_dict["status"] = status
    
    customers = await DatabaseUtils.find_many(
        CustomerModel.collection_name, 
        filter_dict, 
        limit
    )
    
    return [CustomerResponse(**customer) for customer in customers[skip:skip+limit]]

@router.get("/{customer_id}", response_model=CustomerResponse)
async def get_customer(customer_id: str, db = Depends(get_database)):
    """Get a specific customer by ID"""
    if not db:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Database not available"
        )
    
    customer = await DatabaseUtils.find_by_id(CustomerModel.collection_name, customer_id)
    
    if not customer:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Customer not found"
        )
    
    return CustomerResponse(**customer)

@router.put("/{customer_id}", response_model=CustomerResponse)
async def update_customer(
    customer_id: str, 
    customer_data: CustomerUpdate, 
    db = Depends(get_database)
):
    """Update a customer"""
    if not db:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Database not available"
        )
    
    update_dict = customer_data.model_dump(exclude_unset=True)
    if not update_dict:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="No data provided for update"
        )
    
    success = await DatabaseUtils.update_one(CustomerModel.collection_name, customer_id, update_dict)
    
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Customer not found or update failed"
        )
    
    updated_customer = await DatabaseUtils.find_by_id(CustomerModel.collection_name, customer_id)
    return CustomerResponse(**updated_customer)

@router.delete("/{customer_id}")
async def delete_customer(customer_id: str, db = Depends(get_database)):
    """Delete a customer"""
    if not db:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Database not available"
        )
    
    success = await DatabaseUtils.delete_one(CustomerModel.collection_name, customer_id)
    
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Customer not found"
        )
    
    return {"message": "Customer deleted successfully"}
