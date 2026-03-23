async def get_reporting_schema() -> dict:
    """
    Returns Reporting tables schema
    """
    
    return {
        "tables": {
            "clients": {
                "columns": {
                    "id": "integer",
                    "name": "varchar",
                }
            },
            "projects" : {
                "columns": {
                    "id": "integer",
                    "name": "varchar",
                    "client_id": "integer", "foreign_key": "clients.id"
                }
            },
            "sources" : {
                "columns": {
                    "id": "integer",
                    "name": "varchar",
                }
            },
            "jobs" : {
                "columns": {
                    "id": "integer",
                    "project_id": "integer", "foreign_key": "projects.id",
                    "source_id": "integer", "foreign_key": "sources.id",
                    "date": "date",
                    "status": "enum('IN_PROGRESS', 'COMPLETED', 'FAILED')",
                    "cost": "float"
                }
            }
        }
    }