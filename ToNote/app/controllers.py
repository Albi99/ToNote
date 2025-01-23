from flask import Blueprint, render_template, request, redirect, url_for
from app import models

main_blueprint = Blueprint('main', __name__)

@main_blueprint.route('/')
def index():
    notes = models.Note.get_all()
    todos = models.Todo.get_all()
    return render_template('index.html', notes=notes, todos=todos)



# NOTE

@main_blueprint.route('/add_note', methods=['POST'])
def add_note():
    content = request.form.get('content')
    models.Note.add(content)
    return redirect(url_for('main.index'))

@main_blueprint.route('/edit_note/<int:note_id>', methods=['GET', 'POST'])
def edit_note(note_id):
    note = models.Note.get(note_id)
    if request.method == 'POST':
        print('Inside POST')
        new_content = request.form.get('content')
        if new_content:
            models.Note.edit(note, new_content)
            return redirect(url_for('main.index'))
    return render_template('edit_note.html', note=note)

@main_blueprint.route('/delete_note/<int:note_id>', methods=['POST'])
def delete_note(note_id):
    models.Note.delete(note_id)
    return redirect(url_for('main.index'))




# TODO

@main_blueprint.route('/add_todo', methods=['POST'])
def add_todo():
    task = request.form.get('task')
    models.Todo.add(task)
    return redirect(url_for('main.index'))

@main_blueprint.route('/toggle_todo/<int:todo_id>', methods=['POST'])
def toggle_todo(todo_id):
    models.Todo.toggle(todo_id)
    return redirect(url_for('main.index'))

@main_blueprint.route('/delete_todo/<int:todo_id>', methods=['POST'])
def delete_todo(todo_id):
    models.Todo.detete(todo_id)
    return redirect(url_for('main.index'))
