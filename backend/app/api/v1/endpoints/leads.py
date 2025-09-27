
from fastapi import APIRouter

router = APIRouter()

@router.get("/")
async def get_leads():
    return {"message": "Leads endpoint - coming soon"}

@router.get("/{lead_id}")
async def get_lead(lead_id: str):
    return {"message": f"Lead {lead_id} details - coming soon"}
