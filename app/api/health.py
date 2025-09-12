from fastapi import APIRouter
from app.models import ChatResponse

router = APIRouter(prefix="/api/v1", tags=["Health"])

@router.get("/health")
async def health_check():
    """헬스 체크 엔드포인트"""
    return {"status": "healthy", "service": "hyperclova-chat-api"}

@router.get("/")
async def root():
    """루트 엔드포인트"""
    return {
        "message": "HyperCLOVA X Chat API",
        "version": "1.0.0",
        "docs": "/docs"
    }