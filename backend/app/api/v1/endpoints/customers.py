
from fastapi import APIRouter, Depends, HTTPException, status, Query
from typing import List, Optional
from ...schemas.schemas import CustomerCreate, CustomerUpdate, CustomerResponse
from ...models.models import CustomerModel
from ...utils.database import DatabaseUtils
from ...middleware.auth import get_current_user

router = APIRouter()

@router.get("/", response_model=List[CustomerResponse])
async def get_customers(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    status_filter: Optional[str] = None,
    industry_filter: Optional[str] = None,
    current_user = Depends(get_current_user)
):
    """Get all customers with filtering and pagination"""
    filters = {}
    if status_filter:
        filters["status"] = status_filter
    if industry_filter:
        filters["industry"] = industry_filter
    
    customers = await DatabaseUtils.find_many(
        CustomerModel.collection_name,
        filters,
        skip=skip,
        limit=limit
    )
    
    return [CustomerResponse(**customer) for customer in customers]

@router.get("/{customer_id}", response_model=CustomerResponse)
async def get_customer(customer_id: str, current_user = Depends(get_current_user)):
    """Get customer by ID"""
    customer = await DatabaseUtils.find_by_id(CustomerModel.collection_name, customer_id)
    if not customer:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Customer not found"
        )
    return CustomerResponse(**customer)

@router.post("/", response_model=CustomerResponse)
async def create_customer(
    customer: CustomerCreate,
    current_user = Depends(get_current_user)
):
    """Create a new customer"""
    customer_model = CustomerModel(**customer.dict())
    result = await DatabaseUtils.create(CustomerModel.collection_name, customer_model.to_dict())
    
    created_customer = await DatabaseUtils.find_by_id(
        CustomerModel.collection_name, 
        str(result.inserted_id)
    )
    return CustomerResponse(**created_customer)

@router.put("/{customer_id}", response_model=CustomerResponse)
async def update_customer(
    customer_id: str,
    customer_update: CustomerUpdate,
    current_user = Depends(get_current_user)
):
    """Update customer"""
    existing_customer = await DatabaseUtils.find_by_id(CustomerModel.collection_name, customer_id)
    if not existing_customer:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Customer not found"
        )
    
    update_data = customer_update.dict(exclude_unset=True)
    if update_data:
        await DatabaseUtils.update_by_id(CustomerModel.collection_name, customer_id, update_data)
    
    updated_customer = await DatabaseUtils.find_by_id(CustomerModel.collection_name, customer_id)
    return CustomerResponse(**updated_customer)

@router.delete("/{customer_id}")
async def delete_customer(customer_id: str, current_user = Depends(get_current_user)):
    """Delete customer"""
    customer = await DatabaseUtils.find_by_id(CustomerModel.collection_name, customer_id)
    if not customer:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Customer not found"
        )
    
    await DatabaseUtils.delete_by_id(CustomerModel.collection_name, customer_id)
    return {"message": "Customer deleted successfully"}

@router.get("/stats/overview")
async def get_customer_stats(current_user = Depends(get_current_user)):
    """Get customer statistics"""
    total_customers = await DatabaseUtils.count_documents(CustomerModel.collection_name)
    active_customers = await DatabaseUtils.count_documents(
        CustomerModel.collection_name, 
        {"status": "active"}
    )
    
    return {
        "total_customers": total_customers,
        "active_customers": active_customers,
        "prospect_customers": await DatabaseUtils.count_documents(
            CustomerModel.collection_name, 
            {"status": "prospect"}
        )
    }
