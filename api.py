from flask import Flask, jsonify, request
import random

app = Flask(__name__)

# La API acepta GET y ahora lee los parámetros 'lower' y 'upper' de la URL.
# Ejemplo de llamada: /generate_number?lower=5&upper=50
@app.route('/generate_number', methods=['GET'])
def generate_number():
    # Obtener los parámetros 'lower' y 'upper' de la URL (query string)
    # Se usan valores por defecto de 1 y 100 si no se proporcionan, aunque AppSheet siempre los enviará.
    try:
        # request.args.get() recupera los parámetros de la parte ?clave=valor de la URL
        lower_limit = int(request.args.get('lower', 1))
        upper_limit = int(request.args.get('upper', 100))
    except ValueError:
        # Manejo de error si AppSheet envía texto en lugar de números
        return jsonify({"error": "Los límites deben ser valores enteros."}), 400

    # Asegurar la coherencia de los límites
    if lower_limit > upper_limit:
        lower_limit, upper_limit = upper_limit, lower_limit # Intercambiar

    # Generar el número aleatorio dentro del rango proporcionado
    random_number = random.randint(lower_limit, upper_limit)

    # Devolver la respuesta JSON
    return jsonify({"number": random_number})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)