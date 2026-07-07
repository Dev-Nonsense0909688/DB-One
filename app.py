from flask import Flask, render_template
from routes import query, tables, tree_api

app = Flask(__name__)
app.register_blueprint(query)
app.register_blueprint(tables)
app.register_blueprint(tree_api)


@app.route("/")
def index():

    return render_template("index.html")

if __name__ == "__main__": 
    app.run(host="0.0.0.0",port="5000",debug=False)
