from app.core.database import run_query
import logging
import sys

# Configure logging to show INFO messages
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    stream=sys.stderr
)

logger = logging.getLogger(__name__)

async def execute_sql(sql: str) -> str:
    """
    Executes a read-only SQL query
    
    Args:
        sql: The SQL SELECT query string to execute
    """
    logger.info(f"Executing SQL: {sql}")
    result = run_query(sql)
    return str(result)