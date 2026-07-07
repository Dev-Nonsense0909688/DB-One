from flask import Blueprint, request, jsonify
import psycopg

query = Blueprint("sql_query",__name__)


@query.post("/api/query")
def execute_query():

    data = request.get_json()

    db = data["database"]
    query = data["query"]

    try:
        with psycopg.connect(host="localhost", dbname=db, user="postgres", password="anish") as conn:
            conn.autocommit = True
            
            with conn.cursor() as cur:

                cur.execute(query)
                
                if cur.description:
                    columns = [d.name for d in cur.description]
                    rows = cur.fetchall()
                    return jsonify({"success": True, "columns": columns, "rows": rows})

                conn.commit()

                return jsonify(
                    {"success": True, "message": "Query executed successfully."}
                )

    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 400
