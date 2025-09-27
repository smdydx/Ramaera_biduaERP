
from fastapi import APIRouter, Depends, HTTPException, status, Query
from typing import List, Optional
from app.schemas.schemas import LeadCreate, LeadUpdate, LeadResponse
from app.models.models import LeadModel
from app.utils.database import DatabaseUtils
from app.middleware.auth import get_current_user

router = APIRouter()

@router.get("/", response_model=List[LeadResponse])
async def get_leads(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    status_filter: Optional[str] = None,
    current_user = Depends(get_current_user)
):
    """Get all leads with filtering and pagination"""
    filters = {}
    if status_filter:
        filters["status"] = status_filter
    
    leads = await DatabaseUtils.find_many(
        LeadModel.collection_name,
        filters,
        skip=skip,
        limit=limit
    )
    
    return [LeadResponse(**lead) for lead in leads]

@router.get("/{lead_id}", response_model=LeadResponse)
async def get_lead(lead_id: str, current_user = Depends(get_current_user)):
    """Get lead by ID"""
    lead = await DatabaseUtils.find_by_id(LeadModel.collection_name, lead_id)
    if not lead:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Lead not found"
        )
    return LeadResponse(**lead)

@router.post("/", response_model=LeadResponse)
async def create_lead(
    lead: LeadCreate,
    current_user = Depends(get_current_user)
):
    """Create a new lead"""
    lead_model = LeadModel(**lead.dict())
    result = await DatabaseUtils.create(LeadModel.collection_name, lead_model.to_dict())
    
    created_lead = await DatabaseUtils.find_by_id(
        LeadModel.collection_name,
        str(result.inserted_id)
    )
    return LeadResponse(**created_lead)
