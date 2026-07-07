from flask import Blueprint
from drivers.postgres import PostgresDBHandler

tree_api = Blueprint("tree", __name__)


@tree_api.route("/api/tree")
def tree_table():
    return PostgresDBHandler().__tree__
