# driver for postgres DBs
import psycopg

from config import HOST, PASSWORD


def conn(db: str = "postgres") -> psycopg.Cursor:
    return psycopg.connect(
        host=HOST, dbname=db, user="postgres", password=PASSWORD
    ).cursor()


class PostgresDBHandler:
    def __init__(self):
        pass

    def get_databases(self, cursor: psycopg.Cursor = conn()):

        cursor.execute("""
            SELECT datname
            FROM pg_database
            WHERE NOT datistemplate
            AND datname <> 'postgres'  
            ORDER BY datname;
        """)  # executing with `AND datname <> 'postgres'` to exclude inbuilt databases.
        return [r[0] for r in cursor.fetchall()]

    def get_schemas(self, cursor: psycopg.Cursor = conn()):
        cursor.execute("""
            SELECT schema_name
            FROM information_schema.schemata
            WHERE schema_name NOT IN (
                'information_schema',
                'pg_catalog',
                'pg_toast'
            )
            ORDER BY schema_name;
        """) # executeing with WHERE schem_name NOT IN ( ... .... .... ) to exclude those inbuilt schemas
        return [r[0] for r in cursor.fetchall()]

    def get_tables(self, schema: str, cursor: psycopg.Cursor = conn() ):

        cursor.execute(
            """
            SELECT table_name
            FROM information_schema.tables
            WHERE table_schema = %s
            ORDER BY table_name;
        """,
            (schema,),
        ) # getting tables from a specific schemas.
        return [r[0] for r in cursor.fetchall()]

    def get_columns(self, schema: str, table: str, cursor: psycopg.Cursor = conn()):

        cursor.execute(
            """
            SELECT
                column_name,
                data_type
            FROM information_schema.columns
            WHERE table_schema = %s
            AND table_name = %s
            ORDER BY ordinal_position;
        """,
            (schema, table),
        ) # getting columns of a specific table from a specific table.
        return [(r[0], r[1].upper()) for r in cursor.fetchall()]

    def get_table_content(self, schema: str, table: str, cursor: psycopg.Cursor = conn()):

        cursor.execute(f"SELECT * FROM \"{schema}\".\"{table}\";") # Getting all rows and columns from the specifc table.

        rows = cursor.fetchall()
        columns = [(d.name, d.type_code) for d in cursor.description]

        return {"columns": self.get_columns(schema,  table, cursor), "rows": None if rows == [] else rows}

    @property
    def __tree__(self):
        tree = {}

        dbs = self.get_databases()

        for db in dbs:
            tree[db] = {}

            with conn(db) as cursor:
                schemas = self.get_schemas(cursor)
                for schema in schemas:
                    tree[db][schema] = self.get_tables(schema, cursor)

                    
        return tree
     
