from flask_restful import Resource, Api, reqparse
from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_login import login_required, current_user


app = Flask(__name__)
api = Api(app)

parser = reqparse.RequestParser()
parser.add_argument('description', type=str, help='Description of the todo')

class TodoResource(Resource):
    @login_required
    def get(self, todo_id):
        from db import Todo, db
        todo = Todo.query.filter_by(id=todo_id, user_id=current_user.id).first()
        if todo:
            return jsonify({'id': todo.id, 'description': todo.description, 'complete': todo.complete})
        return {'message': 'Todo not found'}, 404

    @login_required
    def patch(self, todo_id):
        from db import Todo, db
        args = parser.parse_args()
        todo = Todo.query.filter_by(id=todo_id, user_id=current_user.id).first()
        if todo:
            todo.description = args['description']
            db.session.commit()
            return {'message': 'Todo updated successfully'}
        return {'message': 'Todo not found'}, 404

    @login_required
    def delete(self, todo_id):
        from db import Todo, db
        todo = Todo.query.filter_by(id=todo_id, user_id=current_user.id).first()
        if todo:
            db.session.delete(todo)
            db.session.commit()
            return {'message': 'Todo deleted successfully'}
        return {'message': 'Todo not found'}, 404

class TodoListResource(Resource):
    @login_required
    def get(self):
        from db import Todo, db
        todos = Todo.query.filter_by(user_id=current_user.id).all()
        todo_list = [{'id': todo.id, 'description': todo.description, 'complete': todo.complete} for todo in todos]
        return jsonify(todo_list)

    @login_required
    def post(self):
        args = parser.parse_args()
        from db import Todo, db
        new_todo = Todo(description=args['description'], user_id=current_user.id)
        db.session.add(new_todo)
        db.session.commit()
        return {'message': 'Todo created successfully'}, 201

api.add_resource(TodoListResource, '/api/todos/')
api.add_resource(TodoResource, '/api/todos/<int:todo_id>')

if __name__ == '__main__':
    app.run(debug=True)
