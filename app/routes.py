from flask import Blueprint, request, jsonify, current_app, render_template
from bson.objectid import ObjectId

routes = Blueprint('routes', __name__)

def register_routes(app):
    app.register_blueprint(routes)

@routes.route('/add', methods=['POST'])
def add_todo():
    db = current_app.db  # Use current_app to access db
    data = request.json
    if not data or 'title' not in data:
        return jsonify({'error': 'Title is required'}), 400
    todo = {'title': data['title'], 'description': data.get('description', ''), 'completed': False}
    result = db.todos.insert_one(todo)
    todo['_id'] = str(result.inserted_id)
    return jsonify(todo), 201


@routes.route('/display', methods=['GET'])
def get_all_todos():
    db = current_app.db  # Use current_app to access db
    todos = list(db.todos.find())
    if not todos:
        return jsonify({'message': 'All tasks are completed'}), 200
    return jsonify([
        {'id': str(todo['_id']), 'title': todo['title'], 'description': todo.get('description', ''), 'completed': todo.get('completed', False)}
        for todo in todos
    ]), 200

@routes.route('/edit/<todo_id>', methods=['PUT'])
def update_todo(todo_id):
    db = current_app.db  # Use current_app to access db
    data = request.json
    if not data:
        return jsonify({'error': 'No data provided'}), 400

    update_data = {}
    if 'title' in data:
        update_data['title'] = data['title']
    if 'description' in data:
        update_data['description'] = data['description']
    if 'completed' in data:
        update_data['completed'] = data['completed']

    if not update_data:
        return jsonify({'error': 'No valid fields to update'}), 400

    result = db.todos.update_one({'_id': ObjectId(todo_id)}, {'$set': update_data})
    if result.matched_count == 0:
        return jsonify({'error': 'Todo not found'}), 404

    return jsonify({'message': 'Todo updated successfully'}), 200

@routes.route('/delete/<todo_id>', methods=['DELETE'])
def delete_todo(todo_id):
    db = current_app.db  # Use current_app to access db
    result = db.todos.delete_one({'_id': ObjectId(todo_id)})
    if result.deleted_count == 0:
        return jsonify({'error': 'Todo not found'}), 404
    return jsonify({'message': 'Todo deleted successfully'}), 200

@routes.route("/")
def home():
    return render_template('index.html', template_folder='templates')
