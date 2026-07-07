from flask import Blueprint
from drivers.postgres import PostgresDBHandler, conn

tables = Blueprint("tables_api",__name__)

@tables.get("/api/table/<db>/<schema>/<table>")
def table(db, schema, table):
    pstq = PostgresDBHandler()
    
    custom_cursor = conn(db)
    
    return pstq.get_table_content(schema, table, custom_cursor)

