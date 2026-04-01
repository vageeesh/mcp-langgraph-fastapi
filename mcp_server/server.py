import sys
from pathlib import Path

# Add workspace root to Python path
sys.path.insert(0, str(Path(__file__).parent.parent))

from fastmcp import FastMCP

# Import Tools
from app.core.tools.sql_tool import execute_sql
from app.modules.reporting.tools import get_reporting_schema

mcp = FastMCP(
    "query-agent-mcp",
    version="1.0"
)

# Register tools explicitly
mcp.tool()(execute_sql)
mcp.tool()(get_reporting_schema)


if __name__ == "__main__":
    mcp.run(transport="streamable-http", host="0.0.0.0", port=8001)
