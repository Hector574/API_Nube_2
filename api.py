from flask import Flask, jsonify, request
import random
import json

app = Flask(__name__)

# La ruta de la API que AppSheet debe llamar
@app.route('/generate_number', methods=['POST'])
def generate_number():
    
    if request.method != 'POST':
        return jsonify({"error": "Método no permitido. Use POST."}), 405

    data = {}
    
    # 1. Lectura Robusta del Body: Intenta leer como JSON o como texto sin formato (Content-Type: Text)
    try:
        if request.is_json:
            data = request.get_json()
        elif request.data:
            # Si AppSheet envía Content-Type: Text o Plain, cargamos el JSON manualmente del body crudo
            data = json.loads(request.data)
    except Exception:
        # Si el body está vacío o mal formado, data es {}
        pass

    # 2. Definición de Límites (CRÍTICO: Valores por defecto ajustados)
    # Si AppSheet falla en enviar el límite inferior, se usará 1.
    # Si AppSheet falla en enviar el límite superior, se usará 10000.
    lower_limit_str = data.get('lower', 1) 
    upper_limit_str = data.get('upper', 10000) 

    try:
        # 3. Conversión a entero: Maneja "1200" (string) o 1200 (number)
        lower_limit = int(lower_limit_str)
        upper_limit = int(upper_limit_str)
        
        # 4. Validación y Generación
        if lower_limit > upper_limit:
            # Si AppSheet envía los límites al revés, usamos los valores por defecto para evitar el error 400
            lower_limit = 1
            upper_limit = 10000
        
        random_number = random.randint(lower_limit, upper_limit)
        
        # 5. Devolvemos el resultado
        return jsonify({"number": random_number})

    except ValueError:
        # Si AppSheet envía un valor no numérico (ej: "texto"), usamos los valores por defecto
        random_number = random.randint(1, 10000)
        return jsonify({"number": random_number})
        
    except Exception as e:
        return jsonify({"error": f"Error interno del servidor: {str(e)}"}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
