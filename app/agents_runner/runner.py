from agents import Runner
from agents.mcp import MCPServerStdio
from agents.stream_events import (
    RawResponsesStreamEvent, 
    RunItemStreamEvent, 
    AgentUpdatedStreamEvent
)
from app.agents.sql_agent import create_sql_agent
from app.core.redis import RedisClient


async def run_sql_agent(query: str, session_id: str = "default"):
    """Run SQL agent with given query and session ID for conversation history"""
    # later change the sesion_id to be dynamic based on user or conversation context for better memory management
    # In production, use MCPServerHTTP or a persistent connection to avoid startup overhead
    # Always ensure the MCP server is running before executing this function in production
    # example: mcp_server = MCPServerHTTP("http://localhost:8000/mcp")
    # run like python mcp_server/server.py in a separate terminal
    print(f"Query got from user is {query}")
    
    # Initialize Redis client
    redis_client = RedisClient()
    
    mcp_server = MCPServerStdio(
        params={
            "command": "python",
            "args": ["mcp_server/server.py"]
        }
    )

    async with mcp_server as server:
        # Create agent with MCP server
        sql_agent = create_sql_agent(mcp_servers=[server])
        
        # Load conversation history from Redis (if needed)
        history = redis_client.load_memory(session_id)
        # Attach history to the input messages for the agent
        input_messages = history + [
            {"role": "user", "content": query}
        ]
        
        result = await Runner.run(
            sql_agent,
            input_messages
        )

        print("Final output from agent:", result.final_output)
        
        # Save conversation turn to Redis
        # To DO: later store metadata, like Query instead of current complete message and that can be used to improve accurecy and performence of agent in future interactions
        redis_client.save_turn(session_id, query, result.final_output)

        return result.final_output


async def stream_sql_agent(query: str, session_id: str = "default"):
    """Stream SQL agent responses with MCP capabilities using run_streamed"""
    print(f"Streaming query from user: {query}")
    
    redis_client = RedisClient()
    
    mcp_server = MCPServerStdio(
        params={
            "command": "python",
            "args": ["mcp_server/server.py"]
        }
    )

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
