from flask import request, Blueprint,jsonify, request

from .extension import db
from .models import Task

main = Blueprint("main", __name__)

@main.route("/v1/tasks", methods=["POST"])
def createTask():
    data = request.get_json()

    if not data:
        return jsonify({"error": "Request body is required"}), 400

    if "tasks" in data:  # Bulk addition
        tasks = []
        for item in data["tasks"]:
            if "title" not in item:
                return jsonify({"error": "Title is required for each task"}), 400
            task = Task(title=item["title"], is_completed=item.get("is_completed", False))
            tasks.append(task)
        db.session.add_all(tasks)
    else:  # Single addition
        if "title" not in data:
            return jsonify({"error": "Title is required in the request body"}), 400
        task = Task(title=data["title"], is_completed=data.get("is_completed", False))
        db.session.add(task)

    db.session.commit()

    if "tasks" in data:
        return jsonify({"ids": [task.id for task in tasks]}), 201
    else:
        return jsonify({"id": task.id}), 201
    

@main.route("/v1/tasks", methods=["GET"])
def getTasks():
    tasks = Task.query.all()

    task_list = []
    for task in tasks:
        task_list.append(task.to_dict())

    return jsonify({"tasks": task_list}), 200


@main.route("/v1/tasks/<int:task_id>", methods=["GET"])
def getTaskById(task_id):
    task = Task.query.get(task_id)

    if task:
        return jsonify(task.to_dict()), 200
    else:
        return jsonify({"error": "There is no task at that id"}), 404


@main.route("/v1/tasks/<int:task_id>", methods=["DELETE"])
def deleteTaskById(task_id):
    task = Task.query.get(task_id)
    if task:
        db.session.delete(task)
        db.session.commit()
    return '', 204


@main.route("/v1/tasks/<int:task_id>", methods=["PUT"])
def editTaskById(task_id):
    task = Task.query.get(task_id)

    if not task:
        return jsonify({"error": f"There is no task at that id"}), 404

    data = request.get_json()

    if not data:
        return jsonify({"error": "Invalid JSON data in request body"}), 400

    task.title = data.get("title", task.title)
    task.is_completed = data.get("is_completed", task.is_completed)
    db.session.commit()

    return '', 204

@main.route("/v1/tasks", methods=["DELETE"])
def deleteTasks():
    data = request.get_json()

    if not data or "tasks" not in data or not isinstance(data["tasks"], list):
        return '', 400

    task_ids = [task_data.get("id") for task_data in data["tasks"]]

    if None in task_ids:
        return '', 400

    tasks_to_delete = Task.query.filter(Task.id.in_(task_ids)).all()

    for task in tasks_to_delete:
        db.session.delete(task)

    db.session.commit()

    return '', 204