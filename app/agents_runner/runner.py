import os
from agents import Runner
from agents.mcp import MCPServerStreamableHttp

from agents.stream_events import (
    RawResponsesStreamEvent, 
    RunItemStreamEvent, 
    AgentUpdatedStreamEvent
)
from app.agents.sql_agent import create_sql_agent
from app.core.redis import RedisClient

MCP_URL = os.getenv("MCP_SERVER_URL", "http://mcp-server:8001/mcp")

# Initialize once, reuse across requests
mcp_server = MCPServerStreamableHttp(params={"url": MCP_URL})


async def stream_sql_agent(query: str, session_id: str = "default"):
    """Stream SQL agent responses with MCP capabilities using run_streamed"""
    print(f"Streaming query from user: {query}")
    
    redis_client = RedisClient()

    async with mcp_server as server:
        sql_agent = create_sql_agent(mcp_servers=[server])

        history = redis_client.load_memory(session_id)
        input_messages = history + [
            {"role": "user", "content": query}
        ]

        print("Complete input messages for agent:", input_messages)

        full_response = ""

        # run_streamed returns a RunResultStreaming object
        result = Runner.run_streamed(sql_agent, input_messages)

        # stream_events() returns an async iterator of events
        async for event in result.stream_events():
            # Check for text delta events by type attribute
            if hasattr(event, 'type') and event.type == 'response.output_text.delta':
                # This is the actual text chunk from the model
                if hasattr(event, 'delta') and event.delta:
                    full_response += event.delta
                    yield event.delta
            elif isinstance(event, RawResponsesStreamEvent):
                # Handle wrapped delta events
                if hasattr(event.data, 'type') and event.data.type == 'response.output_text.delta':
                    if hasattr(event.data, 'delta') and event.data.delta:
                        full_response += event.data.delta
                        yield event.data.delta
                # Only handle string data, skip other event objects
                elif isinstance(event.data, str) and event.data:
                    full_response += event.data
                    yield event.data
            elif isinstance(event, RunItemStreamEvent):
                # Handle tool calls, tool results, messages if needed
                pass
            elif isinstance(event, AgentUpdatedStreamEvent):
                # Handle agent updates (state changes, tool calls, etc.)
                pass
            else:
                # Silently ignore other event types (ResponseCreatedEvent, ResponseInProgressEvent, etc.)
                pass

        print("Final streamed output:", full_response)
        redis_client.save_turn(session_id, query, full_response)
