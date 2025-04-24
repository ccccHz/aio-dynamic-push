from flask import Flask, jsonify
from typing import List
from main import TaskStore
from query_task import QueryTask, get_query_task
import os

def create_app(task_store: TaskStore) -> Flask:
    app = Flask(__name__)

    @app.route('/')
    def index():
        tasks = task_store.all()
        result = []
        for task in tasks:
            task_info = {
                'name': task.name,
                'type': task.type,
                'enable_living_check': task.enable_living_check,
                'living_status_dict': task.living_status_dict
            }
            result.append(task_info)
        return jsonify(result)
    
    @app.route('/living_status')
    def living_status():
        tasks = task_store.all()
        living_status_dicts = [task.living_status_dict for task in tasks]
        return jsonify(living_status_dicts)
    
    @app.route('/task_info')
    def task_info():
        tasks = task_store.all()
        result = []
        for task in tasks:
            task_info = {
                'name': task.name,
                'type': task.type,
                'enable': task.enable,
                'enable_dynamic_check': task.enable_dynamic_check,
                'enable_living_check': task.enable_living_check,
                'intervals_second': task.intervals_second,
                'begin_time': task.begin_time,
                'end_time': task.end_time
            }
            result.append(task_info)
        return jsonify(result)

    return app

def start_web_ui(taskStore: TaskStore):
    app = create_app(taskStore)
    port = int(os.environ.get("PORT", 5001))  # 默认 5001，兼容本地开发
    app.run(debug=False,host='0.0.0.0',port=port)
