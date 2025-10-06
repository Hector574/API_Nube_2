from flask import Flask, jsonify, request
import random
import json

app = Flask(__name__)

# --- CONFIGURACIÓN GLOBAL ---
# Rangos por defecto para asegurar robustez si AppSheet envía algo inválido.
DEFAULT_LOWER = 1
DEFAULT_UPPER = 10000 

# --- FUNCIÓN DE UTILIDAD: LECTURA ROBUSTA DE DATOS ---
def get_request_data():
    """
    Intenta leer los parámetros ('lower', 'upper') desde 
    la URL (Query Params) o desde el Cuerpo (Body) de la solicitud.
    """
    data = {}
    
    # 1. Leer desde Query Params (método AppSheet robusto: GET en URL)
    for key in ['lower', 'upper']:
        if key in request.args:
            data[key] = request.args.get(key)

    # 2. Leer desde Body (método POST: solo si no se encontraron params en la URL)
    if not data and request.method == 'POST':
        try:
            if request.is_json:
                data = request.get_json()
            elif request.data:
                data = json.loads(request.data)
        except Exception:
            pass
            
    return data

# --- ENDPOINT ÚNICO: GENERAR UN SOLO NÚMERO ---
# Usamos el endpoint correcto y aceptamos POST o GET.
@app.route('/generate_single_number', methods=['POST', 'GET'])
def generate_single_number():
    """
    Genera un solo número aleatorio entre los límites proporcionados.
    La respuesta es un objeto JSON simple: {"number": 1234}
    """
    data = get_request_data()
    
    # Extraer y asignar valores.
    # CRÍTICO: Python recibe los límites como cadenas de texto (str) desde AppSheet
    lower_limit_str = data.get('lower', DEFAULT_LOWER) 
    upper_limit_str = data.get('upper', DEFAULT_UPPER)

    try:
        # Conversión segura a entero
        lower_limit = int(lower_limit_str)
        upper_limit = int(upper_limit_str)
        
        # Validación y ajuste de límites
        if lower_limit > upper_limit:
            lower_limit, upper_limit = DEFAULT_LOWER, DEFAULT_UPPER
        
        # Generación del número
        random_number = random.randint(lower_limit, upper_limit)
        
        # Devolvemos el resultado en formato JSON
        return jsonify({"number": random_number})

    except ValueError:
        # Manejo de error si los límites no son numéricos
        random_number = random.randint(DEFAULT_LOWER, DEFAULT_UPPER)
        return jsonify({"number": random_number})
        
    except Exception as e:
        # Manejo de cualquier otro error inesperado
        return jsonify({"error": f"Internal server error: {str(e)}"}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
