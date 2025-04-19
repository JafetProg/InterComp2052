from flask import Flask, request, jsonify

app = Flask(__name__)

# Lista en memoria para almacenar usuarios
usuarios = []

# Ruta GET /info
@app.route('/info', methods=['GET'])
def info():
    return jsonify({
        'informacion': 'Usuarios',
        'version': 'Reciente',
        'estado': 'Disponible'
    })

# Ruta POST /crear_usuario
@app.route('/crear_usuario', methods=['POST'])
def crear_usuario():
    data = request.json

    nombre = data.get('nombre')
    correo = data.get('correo')

    if not nombre or not correo:
        return jsonify({
            'ERROR': 'Es debido tener ambos datos: nombre y correo'
        }), 400

    nuevo_usuario = {
        'id': len(usuarios) + 1,
        'nombre': nombre,
        'correo': correo
    }

    usuarios.append(nuevo_usuario)

    return jsonify({
        "mensaje": "Usuario creado exitosamente!",
        "usuario": nuevo_usuario
    }), 201

# Ruta GET /usuarios
@app.route('/usuarios', methods=['GET'])
def listar_usuarios():
    return jsonify(usuarios)

# Correccion final para ejecutar Flask
if __name__ == '__main__':
    app.run(debug=True)
