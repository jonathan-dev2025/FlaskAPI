from typing import List
from flask import Flask, redirect, request, render_template, url_for
from flask_expects_json import expects_json
from json_saver import JsonSaver
from datetime import datetime
import uuid

app = Flask(__name__, static_folder='assets') 

data_helper=JsonSaver("data.json")

todos:List = []
todo_schema = {
    "type":"object",
    "properties":{
        "title": {"type":"string"},
        "description": {"type":"string"},
        "status":{"type":"integer"},
        "due":{"type":"string"}
    },
    "required": ["title", "description", "status", "due"]
}
@app.route("/")
def home():
    message = "todoapp"
    return render_template('home.html', message=message)

@app.route("/todos", methods=["POST"])
@expects_json(todo_schema)
def create_todos():
    datas = request.get_json()
    datas["id"] = str(uuid.uuid4())
    responses = data_helper.add(datas["id"], datas)
    print(responses)
    return redirect(url_for('get_todos'))



@app.route("/todos")
def get_todos():
    todos = data_helper.find_all()
    return render_template('todos.html', todos=todos, datetime=datetime)

if __name__ == "__main__":
    app.run(debug=True)
