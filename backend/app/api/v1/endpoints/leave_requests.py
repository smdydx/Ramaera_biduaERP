
from fastapi import APIRouter

router = APIRouter()

@router.get("/")
async def get_leave_requests():
    return {"message": "Leave requests endpoint - coming soon"}

@router.get("/{request_id}")
async def get_leave_request(request_id: str):
    return {"message": f"Leave request {request_id} details - coming soon"}
