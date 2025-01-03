from flask import Blueprint, render_template, request, redirect, url_for
from app.models import db, Note, Todo

main_blueprint = Blueprint('main', __name__)

@main_blueprint.route('/')
def index():
    notes = Note.query.all()
    todos = Todo.query.all()
    return render_template('index.html', notes=notes, todos=todos)



# NOTE

@main_blueprint.route('/add_note', methods=['POST'])
def add_note():
    content = request.form.get('content')
    if content:
        new_note = Note(content=content)
        db.session.add(new_note)
        db.session.commit()
    return redirect(url_for('main.index'))

@main_blueprint.route('/delete_note/<int:note_id>', methods=['POST'])
def delete_note(note_id):
    note = Note.query.get_or_404(note_id)
    db.session.delete(note)
    db.session.commit()
    return redirect(url_for('main.index'))

@main_blueprint.route('/edit_note/<int:note_id>', methods=['GET', 'POST'])
def edit_note(note_id):
    note = Note.query.get_or_404(note_id)
    if request.method == 'POST':
        new_content = request.form.get('content')
        if new_content:
            note.content = new_content
            db.session.commit()
            return redirect(url_for('main.index'))
    return render_template('edit_note.html', note=note)




# TODO

@main_blueprint.route('/add_todo', methods=['POST'])
def add_todo():
    task = request.form.get('task')
    if task:
        new_task = Todo(task=task)
        db.session.add(new_task)
        db.session.commit()
    return redirect(url_for('main.index'))

@main_blueprint.route('/toggle_todo/<int:todo_id>', methods=['POST'])
def toggle_todo(todo_id):
    todo =  Todo.query.get_or_404(todo_id)
    todo.is_done = not todo.is_done
    db.session.commit()
    return redirect(url_for('main.index'))

@main_blueprint.route('/delete_todo/<int:todo_id>', methods=['POST'])
def delete_todo(todo_id):
    todo = Todo.query.get_or_404(todo_id)
    db.session.delete(todo)
    db.session.commit()
    return redirect(url_for('main.index'))
