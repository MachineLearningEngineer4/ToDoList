from flask import Flask, render_template, request, redirect, url_for
from datetime import datetime

app = Flask(__name__)

todos = []

@app.route('/todos/<int:todo_id>', methods=['GET'])
def get_todo(todo_id):
    todo = next((item for item in todos if item['id'] == todo_id), None)
    if todo is None:
        return {'error': 'Todo not found'}, 404
    return {'todo': todo}

@app.route('/todos/<int:todo_id>/update_form')
def update_form(todo_id):
    todo = next((item for item in todos if item['id'] == todo_id), None)
    if todo is None:
        return render_template('not_found.html'), 404
    return render_template('update_form.html', todo=todo)

@app.route('/todos/<int:todo_id>/update', methods=['POST'])
def update_todo(todo_id):
    global todos

    todo = next((item for item in todos if item['id'] == todo_id), None)
    if todo is None:
        return {'error': 'Todo not found'}, 404

    todo['name'] = request.json.get('name', todo['name'])
    todo['description'] = request.json.get('description', todo['description'])
    todo['deadline'] = request.json.get('deadline', todo['deadline'])
    todo['completed'] = request.json.get('completed', todo['completed'])

    return {'todo': todo}

@app.route('/todos/<int:todo_id>/delete', methods=['POST'])
def delete_todo(todo_id):
    global todos

    todos = [item for item in todos if item['id'] != todo_id]
    return {'message': 'Todo deleted successfully'}

@app.route('/todos', methods=['GET', 'POST'])
def todos_list():
    global todos

    if request.method == 'GET':
        sort_by = request.args.get('sort_by', 'id')
        filter_completed = request.args.get('filter_completed', None)

        # Sorting
        todos.sort(key=lambda x: x[sort_by])

        # Filtering
        if filter_completed is not None:
            filter_completed = filter_completed.lower() == 'true'
            todos = [todo for todo in todos if todo['completed'] == filter_completed]

        return {'todos': todos}

    elif request.method == 'POST':
        new_todo = {
            'id': todos[-1]['id'] + 1 if todos else 1,
            'name': request.json['name'],
            'description': request.json.get('description', ''),
            'deadline': request.json.get('deadline', ''),
            'completed': request.json.get('completed', False),
            'created_at': datetime.now().isoformat()
        }

        todos.append(new_todo)
        return {'todo': new_todo}


@app.route('/todos/<int:todo_id>/view', methods=['GET'])
def view_todo(todo_id):
    todo = next((item for item in todos if item['id'] == todo_id), None)
    if todo is None:
        return render_template('not_found.html'), 404
    return render_template('view_todo.html', todo=todo)

@app.route('/')
def index():
    return render_template('index.html', todos=todos)

if __name__ == '__main__':
    app.run(debug=True)