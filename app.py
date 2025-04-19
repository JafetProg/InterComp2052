from flask import Flask, request, jsonify

app = Flask(__name__)


mensajes = []

@app.route("/", methods=["GET"])
def hello_world():
    return "<h1>Página principal !!</h1>"


@app.route("/info", methods=["GET"])
def info():
    return jsonify({
        "app": "Servidor Flask para proyecto Capstone",
        "version": "1.0",
        "autor": "Jafet R. Melendez Vidot"
    })

@app.route("/mensaje", methods=["GET", "POST"])
def mensaje():
    if request.method == "GET":
        return jsonify({"mensajes": mensajes})

    if request.method == "POST":
        data = request.json
        if not data or "mensaje" not in data:
            return jsonify({"error": "Mensaje no proporcionado"}), 400

        mensajes.append(data["mensaje"])
        return jsonify({"respuesta": f"Mensaje recibido: '{data['mensaje']}'"}), 201

if __name__ == "__main__":
    app.run(debug=True)
