from flask import Flask, jsonify
from typing import List
from query_task import QueryTask, get_query_task

app = Flask(__name__)
Tasks=[]

# accept list of QueryTask objects
# and start a flask server to display the results
@app.route('/')
def index():
    living_status_dicts = [
        task.living_status_dict for task in Tasks]
    return jsonify(living_status_dicts)

    # Assuming there's a template named 'index.html' that expects 'tasks' variable
       # return render_template('index.html', tasks=query_task_list)

def start_web_ui(tasks: List[QueryTask]):
    global Tasks
    Tasks=tasks
    app.run(debug=False,port=5001)
