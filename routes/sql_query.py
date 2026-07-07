from flask import Blueprint, request, jsonify
import psycopg

from config import HOST, PASSWORD

query = Blueprint("sql_query",__name__)


@query.post("/api/query")
def execute_query():
    data = request.get_json()

    db = data["database"]
    sql = data["query"]

    try:
        with psycopg.connect(
            host=HOST, dbname=db, user="postgres", password=PASSWORD
        ) as conn:

            conn.autocommit = True

            with conn.cursor() as cur:
                cur.execute(sql)

                # SELECT .
                if cur.description is not None:
                    columns = [d.name for d in cur.description]
                    rows = cur.fetchall()

                    return jsonify(
                        {
                            "success": True,
                            "type": "result",
                            "columns": columns,
                            "rows": rows,
                            "rowcount": len(rows),
                        }
                    )

                # INSERT, UPDATE, DELETE, CREATE, DROP etc.
                return jsonify(
                    {
                        "success": True,
                        "type": "command",
                        "message": "Query executed successfully.",
                        "affected_rows": cur.rowcount,
                    }
                )

    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 400
