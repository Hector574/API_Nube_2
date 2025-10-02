from flask import Flask, jsonify, request
import random

app = Flask(__name__)

# La ruta acepta ambos métodos: GET (URL) y POST (Body JSON)
@app.route('/generate_number', methods=['GET', 'POST']) 
def generate_number():
    # Límites por defecto para la prueba (10 y 15)
    lower_limit = 10
    upper_limit = 15
    
    # 1. Lógica para leer límites según el método de solicitud
    if request.method == 'POST':
        # Si es POST (viene de AppSheet), leemos el Body JSON
        data = request.get_json()
        if data:
            # Extraemos los límites. Si no existen, usamos 10 y 15 como fallback
            lower_limit = data.get('lower', 10) 
            upper_limit = data.get('upper', 15)
    
    elif request.method == 'GET':
        # Si es GET (para pruebas de navegador), leemos la URL
        lower_limit = request.args.get('lower', 10)
        upper_limit = request.args.get('upper', 15)

    # 2. Conversión y validación
    try:
        lower_limit = int(lower_limit)
        upper_limit = int(upper_limit)
    except (ValueError, TypeError):
        return jsonify({"error": "Los límites deben ser valores enteros."}), 400

    # Aseguramos que el límite inferior sea menor o igual al superior
    if lower_limit > upper_limit:
        lower_limit, upper_limit = upper_limit, lower_limit

    # 3. Generar y devolver el resultado
    random_number = random.randint(lower_limit, upper_limit)
    
    # Devolvemos la clave 'number' (en inglés)
    return jsonify({"number": random_number})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)