from fastapi import APIRouter
from fastapi.responses import StreamingResponse
from app.api.v1.router import router as v1_router
from app.agents_runner.runner import run_sql_agent, stream_sql_agent
import json

api_router = APIRouter()

api_router.include_router(
    v1_router,
    prefix="/api/v1"
)


@api_router.post("/query")
async def ask(query: dict):
    result = await run_sql_agent(query["query"])
    return {"output": result}


@api_router.post("/query/stream")
async def ask_stream(query: dict):
    async def event_generator():
        async for chunk in stream_sql_agent(query["query"], query.get("session_id", "default")):
            #  We need this if the client is expecting Server-Sent Events (SSE) format, but since we're just sending plain text chunks, we can yield the chunk directly
            # Standard SSE protocol expects data to be prefixed with "data: " and followed by two newlines, but if the client can handle plain text, we can simplify it
            # yield f"data: {chunk}\n\n"  # Uncomment this if using SSE format and the client expects it
            yield chunk  # Send chunk directly
    
    return StreamingResponse(event_generator(), media_type="text/event-stream")
