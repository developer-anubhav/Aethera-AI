from fastapi import APIRouter, Depends
from fastapi.responses import StreamingResponse
from sqlalchemy.orm import Session
from pydantic import BaseModel, Field
from typing import List, Optional

from app.core.database import get_db
from app.services.aera_service import AeraService

router = APIRouter(prefix="/aera", tags=["aera"])

class ChatMessage(BaseModel):
    role: str = Field(..., description="Role of the sender: 'user' or 'assistant'")
    content: str = Field(..., description="Text content of the message")

class AeraChatRequest(BaseModel):
    compound_slug: str = Field(..., description="The main compound slug context")
    compare_with_slug: Optional[str] = Field(None, description="The optional slug of the compound to compare with")
    question: str = Field(..., description="The active user question query")
    messages: List[ChatMessage] = Field(default=[], description="The in-memory conversation log history")
    level: str = Field("university", description="Target explanation level: school, high_school, university, research, professional")
    mode: str = Field("explain", description="Generation mode: explain, compare, summarize, teach")

@router.post("/chat")
async def chat_stream(
    request: AeraChatRequest,
    db: Session = Depends(get_db)
):
    """
    Establish a Server-Sent Events (SSE) stream to pipe atomic property context-aware responses.
    """
    service = AeraService(db)
    
    # Format message history to simple dictionaries
    history_dicts = [msg.model_dump() for msg in request.messages]
    
    # Return streaming payload generator
    generator = service.chat_stream(
        compound_slug=request.compound_slug,
        question=request.question,
        history=history_dicts,
        level=request.level,
        mode=request.mode,
        compare_with_slug=request.compare_with_slug
    )
    
    return StreamingResponse(
        generator, 
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
            "Content-Encoding": "none"
        }
    )
