from flask import Flask, jsonify, request
import random

app = Flask(__name__)

@app.route('/generate_number', methods=['GET'])
def generate_number():
    # Obtener los límites de la URL (query string). Se usa 1 y 100 como fallback.
    try:
        lower_limit = int(request.args.get('lower', 1))
        upper_limit = int(request.args.get('upper', 100))
    except ValueError:
        return jsonify({"error": "Los límites deben ser valores enteros."}), 400

    # Asegurar la coherencia de los límites
    if lower_limit > upper_limit:
        lower_limit, upper_limit = upper_limit, lower_limit

    # Generar el número aleatorio
    random_number = random.randint(lower_limit, upper_limit)

    return jsonify({"number": random_number})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)