import logging
from flask import Flask, jsonify, request

app = Flask(__name__)
logging.basicConfig(level=logging.INFO)

# In-memory list of tasks
todos = []

@app.route('/')
def hello_world():
    app.logger.info("Handling request to home route")
    return 'Hello, World!'

# Get all tasks (READ)
@app.route('/todos', methods=['GET'])
def get_todos():
    return jsonify(todos), 200

# Get a specific task by ID (READ)
@app.route('/todos/<int:todo_id>', methods=['GET'])
def get_todo(todo_id):
    if todo_id < len(todos):
        return jsonify(todos[todo_id]), 200
    else:
        return jsonify({'error': 'Task not found'}), 404

# Create a new task (CREATE)
@app.route('/todos', methods=['POST'])
def create_todo():
    if not request.json or not isinstance(request.json, list):
        return jsonify({'error': 'Invalid input, expected a list of tasks'}), 400

    new_todos = request.json
    for task in new_todos:
        if 'task' not in task:
            return jsonify({'error': 'Missing "task" key in one or more items'}), 400
        todos.append(task)
    
    return jsonify(new_todos), 201

# Update an existing task (UPDATE)
@app.route('/todos/<int:todo_id>', methods=['PUT'])
def update_todo(todo_id):
    if todo_id < len(todos):
        todos[todo_id] = request.json
        return jsonify(todos[todo_id]), 200
    else:
        return jsonify({'error': 'Task not found'}), 404

# Delete a task (DELETE)
@app.route('/todos/<int:todo_id>', methods=['DELETE'])
def delete_todo(todo_id):
    if todo_id < len(todos):
        deleted_todo = todos.pop(todo_id)
        return jsonify(deleted_todo), 200
    else:
        return jsonify({'error': 'Task not found'}), 404

if __name__ == '__main__':
    app.run(debug=True)
