from fastapi import FastAPI
from app.routers import api_router

app = FastAPI(
    title="Agent Reporting API"
)

app.include_router(api_router)

# Register tools here
# mcp.tool()(execute_sql)
# mcp.tool()(get_reporting_schema)
