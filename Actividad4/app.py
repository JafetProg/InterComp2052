from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def index():
    data = {
        "title": "Inicio",
        "message": "Bienvenidos a la aplicacion de Flask con Jinja2"
    }
    return render_template('index.html', data=data)

@app.route('/tareas')
def tareas():
    data = {
        "title": "Lista de Tareas",
        "description": "Estas son las tareas de hoy:",
        "items": ["Hacer Actividad 4", "Hacer actividad 5", "Hacer actividad 6"]
    }
    return render_template('tareas.html', **data)

@app.route('/usuarios')
def usuarios():
    data = {
        "title": "Usuarios Registrados",
        "description": "Lista de usuarios activos:",
        "items": ["Ana Maria Lopez III", "Pepito", "Fulano", "Jafet"]
    }
    return render_template('usuarios.html', **data)

if __name__ == '__main__':
    app.run(debug=True)
