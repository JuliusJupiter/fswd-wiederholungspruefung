from flask import Flask, render_template, redirect, url_for, request, abort, flash
from flask_bootstrap import Bootstrap5
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from werkzeug.security import check_password_hash, generate_password_hash
from flask_restful import Api
from api import TodoListResource, TodoResource
import forms

app = Flask(__name__)

app.config.from_mapping(
    SECRET_KEY = 'secret_key_just_for_dev_environment',
    BOOTSTRAP_BOOTSWATCH_THEME = 'pulse'
)

api = Api(app)
api.add_resource(TodoListResource, '/api/todos/')
api.add_resource(TodoResource, '/api/todos/<int:todo_id>')

from db import db, Todo, List, User, insert_sample  


login_manager = LoginManager()
bootstrap = Bootstrap5(app)
login_manager.init_app(app)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

@app.route('/delete_user', methods=['GET', 'POST'])
@login_required
def delete_user():
    form = forms.DeleteAccountForm()
      
    if request.method == 'POST':
        if form.validate_on_submit():    
            db.session.delete(current_user)
            db.session.commit()
            logout_user()
            #flash('Account deleted.', 'success')
            return redirect(url_for('register')) 

    return render_template('delete_user.html', form=form)

@app.route('/index')
@app.route('/')
def index():
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = forms.LoginForm()
    if request.method == 'POST':
        if form.validate():
            user = User.query.filter_by(username=form.username.data).first()
            if user and check_password_hash(user.password, form.password.data):    
                login_user(user)
                return redirect(url_for('todos'))
            flash('wrong password', 'warnung')
            return redirect(url_for('login'))
    else:
        return render_template('login.html', form = form)
    
@app.route('/register', methods=['GET','POST'])
def register():
    form = forms.RegisterForm()
    if request.method == 'POST':
        if form.validate():
            name = form.username.data
            if User.query.filter_by(username=name).first():
                flash('Username already exists. Please choose another.', 'danger')
                return redirect(url_for('register'))
            hashed_password = generate_password_hash(form.password.data)
            user = User(username= name, password=hashed_password)    
            db.session.add(user)
            db.session.commit()
            login_user(user)
            return redirect(url_for('todos'))
    else:
        return render_template('register.html', form = form)    


@app.route('/todos/', methods=['GET', 'POST'])
@login_required
def todos():
    form = forms.CreateTodoForm()
    if request.method == 'GET':
        user_id = current_user.id
        todos = Todo.query.filter_by(user_id=user_id)
        return render_template('todos.html', todos=todos, form=form)
    else:  # request.method == 'POST'
        if form.validate():
            todo = Todo(description=form.description.data, user_id=current_user.id)  # !!
            db.session.add(todo)  # !!
            db.session.commit()  # !!
            flash('Todo has been created.', 'success')
        else:
            flash('No todo creation: validation error.', 'warning')
        return redirect(url_for('todos'))


@app.route('/todos/<int:id>', methods=['GET', 'POST'])
@login_required
def todo(id):
    todo = db.session.get(Todo, id)  # !!
    form = forms.TodoForm(obj=todo)  # (2.)  # !!
    if request.method == 'GET':
        if todo:
            if todo.lists: form.list_id.data = todo.lists[0].id  # (3.)  # !!
            choices = db.session.execute(db.select(List).order_by(List.name)).scalars()  # !!
            form.list_id.choices = [(0, 'List?')] + [(c.id, c.name) for c in choices]  # !!
            return render_template('todo.html', form=form)
        else:
            abort(404)
    else:  # request.method == 'POST'
        if form.method.data == 'PATCH':
            if form.validate():
                form.populate_obj(todo)  # (4.)
                todo.populate_lists([form.list_id.data])  # (5.)  # !!
                db.session.add(todo)  # !!
                db.session.commit()  # !!
                flash('Todo has been updated.', 'success')
            else:
                flash('No todo update: validation error.', 'warning')
            return redirect(url_for('todo', id=id))
        elif form.method.data == 'DELETE':
            db.session.delete(todo)  # !!
            db.session.commit()  # !!
            flash('Todo has been deleted.', 'success')
            return redirect(url_for('todos'), 303)
        else:
            flash('Nothing happened.', 'info')
            return redirect(url_for('todo', id=id))


@app.route('/lists/')
@login_required
def lists():
    lists = db.session.execute(db.select(List).order_by(List.name)).scalars()  # (6.)  # !!
    return render_template('lists.html', lists=lists)


@app.route('/lists/<int:id>')
@login_required
def list(id):
    list = db.session.get(List, id)  # !!
    if list is not None:
        return render_template('list.html', list=list)
    else:
        return redirect(url_for('lists'))

@app.route('/insert/sample')
def run_insert_sample():
    insert_sample()
    return 'Database flushed and populated with some sample data.'

@app.errorhandler(404)
def http_not_found(e):
    return render_template('404.html'), 404

@app.errorhandler(500)
def http_internal_server_error(e):
    return render_template('500.html'), 500

@app.get('/faq/<css>')
@app.get('/faq/', defaults={'css': 'default'})
def faq(css):
    return render_template('faq.html', css=css)

@app.get('/ex/<int:id>')
@app.get('/ex/', defaults={'id':1})
def ex(id):
    if id == 1:
        return render_template('ex1.html')
    elif id == 2:
        return render_template('ex2.html')
    else:
        abort(404)