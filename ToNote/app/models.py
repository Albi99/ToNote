from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()



# NOTE

class Note(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(512), nullable=False)

    @staticmethod
    def add(content):
        if content:
            new_note = Note(content=content)
            db.session.add(new_note)
            db.session.commit()

    @staticmethod
    def edit(note, new_content):
        note.content = new_content
        db.session.commit()

    @staticmethod
    def delete(id):
        note = Note.query.get_or_404(id)
        db.session.delete(note)
        db.session.commit()

    @staticmethod
    def get(id):
        return Note.query.get_or_404(id)

    @staticmethod
    def get_all():
        return Note.query.all()



# TODO

class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    task = db.Column(db.String(128), nullable=False)
    is_done = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=db.func.now())

    @staticmethod
    def add(task):
        if task:
            new_task = Todo(task=task)
            db.session.add(new_task)
            db.session.commit()

    @staticmethod
    def toggle(id):
        todo =  Todo.query.get_or_404(id)
        todo.is_done = not todo.is_done
        db.session.commit()
    
    @staticmethod
    def detete(id):
        todo = Todo.query.get_or_404(id)
        db.session.delete(todo)
        db.session.commit()

    @staticmethod
    def get_all():
        return Todo.query.all()
