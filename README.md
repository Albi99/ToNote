# **ToNote**

## **Descrizione del Progetto**
Questa applicazione è una semplice **web app** costruita con **Flask**, che implementa l'architettura **MVC (Model-View-Controller)**. L'app consente agli utenti di:
- Aggiungere, modificare ed eliminare **note**.
- Aggiungere, contrassegnare come "fatto" ed eliminare **task** nella **to-do list**.

### **Caratteristiche principali**
- Architettura MVC ben definita per separare la logica di business, la presentazione e il controllo.
- Integrazione con un database SQLite per memorizzare note e task.
- Utilizzo di **Bootstrap** per un design responsive e user-friendly.
- Protezione contro attacchi CSRF con **Flask-WTF**.
- Interfaccia dinamica per aggiornare lo stato dei task.

---

## **Struttura del Progetto**

```plaintext
ToNote/
│
├── app/
│   ├── __init__.py          # Configurazione iniziale dell'app Flask
│   ├── models.py            # Modello per Note e To-Do
│   ├── controllers.py       # Logica del controller
│   ├── templates/           # Template HTML
│   │   ├── base.html        # Layout generale
│   │   ├── index.html       # Pagina principale
│   │   └── edit_note.html   # Pagina per modificare le note
│   └── static/              # File statici (ad esempio: CSS, JS, immagini)
│       └── style.css        # Stile personalizzato
│
├── instance/
│   └── app.db               # Istanza del database SQLite
├── run.py                   # Punto di avvio dell'applicazione
└── requirements.txt         # Librerie richieste
```

---

## **Implementazione dell'Architettura MVC**

### **1. Modello (Model)**

Il file `models.py` definisce la struttura dei dati per **Note** e **Task**, utilizzando **SQLAlchemy**.

```python
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Note(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(512), nullable=False)

class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    task = db.Column(db.String(128), nullable=False)
    is_done = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=db.func.now())
```

### **2. Controller (Controller)**

Il file `controllers.py` contiene le rotte che gestiscono le interazioni con l'applicazione. Ad esempio:
- **Aggiungere una nota**:
    ```python
    @main_blueprint.route('/add_note', methods=['POST'])
    def add_note():
        content = request.form.get('content')
        if content:
            new_note = Note(content=content)
            db.session.add(new_note)
            db.session.commit()
        return redirect(url_for('main.index'))
    ```

- **Modificare una nota**:
    ```python
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
    ```

### **3. Vista (View)**

Le viste sono definite nei file HTML nella directory `templates/`. Utilizzano il motore di template **Jinja2** per collegare i dati alle interfacce.

- **Template Base (`base.html`)**:
    Fornisce un layout comune per tutte le pagine, con una navbar e un contenitore principale.

    ```html
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0-alpha3/dist/css/bootstrap.min.css" rel="stylesheet">
        <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap-icons/font/bootstrap-icons.css">
        <link rel="stylesheet" href="{{ url_for('static', filename='style.css') }}">
        <title>{% block title %}ToNote{% endblock %}</title>
    </head>
    <body>
       
        <div class="container">
            {% block content %}{% endblock %}
        </div>

        <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0-alpha3/dist/js/bootstrap.bundle.min.js"></script>
    </body>
    </html>
    ```

- **Template per l'homepage (`index.html`)**:
    Visualizza e gestisce le note.

    ```html
    {% extends 'base.html' %}

    {% block content %}
    <div class="text-center mb-4">
        <br>
        <h1 class="display-4">ToNote</h1>
    </div>

    <div class="row">
        <!-- Sezione Note -->
        <div class="col-md-6">
            <h2>Notes</h2>
            <form method="POST" action="{{ url_for('main.add_note') }}" class="input-group mb-3">
                <input type="hidden" name="csrf_token" value="{{ csrf_token() }}" />
                <input type="text" name="content" class="form-control" placeholder="Type a new note" required>
                <button type="submit" class="btn btn-primary">Add</button>
            </form>
            <ul class="list-group">
                {% for note in notes %}
                    <li class="list-group-item d-flex justify-content-between align-items-center">
                        {{ note.content }}
                        <div>
                            <a href="{{ url_for('main.edit_note', note_id=note.id) }}" class="btn btn-warning btn-sm me-2">
                                <i class="bi bi-pencil sf-2"></i>
                            </a>
                            <form method="POST" action="{{ url_for('main.delete_note', note_id=note.id) }}" style="display:inline;">
                                <input type="hidden" name="csrf_token" value="{{ csrf_token() }}" />
                                <button type="submit" class="btn btn-danger btn-sm"><i class="bi bi-trash sf-2"></i></button>
                            </form>
                        </div>
                    </li>
                {% endfor %}
            </ul>
        </div>

        <!-- Sezione To-Do List -->
        <div class="col-md-6">
            <h2>Tasks</h2>
            <form method="POST" action="{{ url_for('main.add_todo') }}" class="input-group mb-3">
                <input type="hidden" name="csrf_token" value="{{ csrf_token() }}" />
                <input type="text" name="task" class="form-control" placeholder="Type a new task" required>
                <button type="submit" class="btn btn-primary">Add</button>
            </form>
            <ul class="list-group">
                {% for todo in todos %}
                    <li class="list-group-item d-flex justify-content-between align-items-center">
                        <form method="POST" action="{{ url_for('main.toggle_todo', todo_id=todo.id) }}">
                            <input type="hidden" name="csrf_token" value="{{ csrf_token() }}" />
                            <input type="checkbox" name="is_done" onchange="this.form.submit()" {% if todo.is_done %}checked{% endif %} />
                            <span class="task-text">
                                {{ todo.task }}
                            </span>
                        </form>
                        <span class="badge {% if todo.is_done %}bg-success{% else %}bg-warning{% endif %}">
                            {% if todo.is_done %}Done{% else %}Pending{% endif %}
                        </span>
                        <div>
                            <form method="POST" action="{{ url_for('main.delete_todo', todo_id=todo.id) }}" style="display:inline;">
                                <input type="hidden" name="csrf_token" value="{{ csrf_token() }}" />
                                <button type="submit" class="btn btn-danger btn-sm"><i class="bi bi-trash sf-2"></i></button>
                            </form>
                        </div>
                    </li>
                {% endfor %}
            </ul>
        </div>
    </div>
    {% endblock %}
    ```

---

## **Installazione**

1. **Clona il repository**:
    ```bash
    git clone https://github.com/Albi99/ToNote.git
    cd ToNote
    ```

2. **Installa le dipendenze**:
    ```bash
    pip install -r requirements.txt
    ```

3. **Configura il database e avvia l'applicazione**:
    ```bash
    python run.py
    ```

---

## **Utilizzo**
**Collegati a `localhost:5000`**

---

---

## **Tecnologie Utilizzate**
- **Backend**: Flask, Flask-SQLAlchemy
- **Frontend**: Bootstrap, Jinja2
- **Database**: SQLite

---

## **Screenshot**

- **Homepage**:
    ![Homepage](https://via.placeholder.com/800x400?text=Screenshot+Homepage)

- **Edit Note**:
    ![Modifica nota](https://via.placeholder.com/800x400?text=Screenshot+Edit+Note)

---

## **Miglioramenti Futuri**
- Aggiunta di autenticazione utenti.
- Supporto per tagging delle note.
- Funzionalità di ricerca.
