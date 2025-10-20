from fastapi import APIRouter
from .schemas import Blog

router = APIRouter()




@router.post("/")
async def create_blog(request: Blog):
    return request
