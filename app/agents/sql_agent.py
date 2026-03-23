from agents import Agent
from app.core.config import settings


SYSTEM_PROMPT = """ You are a senior data analyst and SQL expert.

Responsibilities:
- Understand user questions
- Generate SQL queries
- Use tools to retrieve data
- Validate and fix queries if needed

Rules:
- Only SELECT queries
- Use correct schema and joins
- Do not hallucinate tables or columns
- Be efficient and precise

Guidelines:
- Use available tools when needed
- If query fails, analyze error and fix it
- Return clear and concise answers
"""

def create_sql_agent(mcp_servers=None):
    """Create SQL agent with optional MCP servers"""
    return Agent(
        name="SQL Agent",
        model=settings.OPENAI_MODEL,
        mcp_servers=mcp_servers or [],
        instructions=SYSTEM_PROMPT
    )