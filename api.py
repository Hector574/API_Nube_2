from flask import Flask, jsonify, request
import random

app = Flask(__name__)

# Función para generar un número aleatorio entre los límites proporcionados por AppSheet.
@app.route('/generate_number', methods=['POST'])
def generate_number():
    # Aseguramos que solo aceptamos peticiones POST
    if request.method != 'POST':
        return jsonify({"error": "Método no permitido. Use POST."}), 405

    # 1. Leemos el Body JSON enviado por AppSheet.
    # Ahora esperamos que 'lower' y 'upper' lleguen como strings (ej: "1050") 
    # debido al uso de TEXT() en el Webhook de AppSheet.
    data = request.get_json()

    # Usamos valores por defecto "1" y "1" como strings en caso de que AppSheet no envíe datos.
    lower_limit_str = data.get('lower', "1")
    upper_limit_str = data.get('upper', "1")

    # Si por alguna razón los valores llegan como None (nulos), los convertimos a "1" para evitar errores de tipo.
    if lower_limit_str is None:
        lower_limit_str = "1"
    if upper_limit_str is None:
        upper_limit_str = "1"
        
    try:
        # 2. CRÍTICO: Conversión explícita y segura de STRING a INTEGER.
        # Esto soluciona el fallo con números mayores a 999 que resultaba en '1'.
        lower_limit = int(lower_limit_str)
        upper_limit = int(upper_limit_str)
        
        # 3. Validación de límites
        if lower_limit > upper_limit:
            # Mensaje de error más útil en caso de que los límites estén invertidos
            return jsonify({"error": "El límite inferior (lower) no puede ser mayor que el superior (upper)."}), 400
        
        # 4. Generamos el número aleatorio (la lógica probada que funciona)
        random_number = random.randint(lower_limit, upper_limit)
        
        # 5. Devolvemos la respuesta JSON que AppSheet espera (clave 'number').
        return jsonify({"number": random_number})

    except ValueError:
        # Captura si el string enviado no puede convertirse a entero (ej: si envían "cien")
        return jsonify({"error": "Los límites enviados deben ser números enteros válidos."}), 400
        
    except Exception as e:
        # Captura cualquier otro error interno del servidor
        return jsonify({"error": f"Error interno del servidor: {str(e)}"}), 500

# Esta línea es necesaria para que Flask se ejecute en el entorno de Render o localmente.
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
