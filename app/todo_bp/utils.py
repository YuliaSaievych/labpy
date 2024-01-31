

def to_json(todo):
    return {
        'id': todo.id,
        'title': todo.title,
        'description': todo.description,
        'done': todo.done,
        'status': todo.status
    }
