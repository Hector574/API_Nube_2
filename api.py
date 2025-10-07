from flask import Flask, request, jsonify
from flask_cors import CORS
import random
from datetime import datetime

# Inicialización de la aplicación Flask
app = Flask(__name__)
# Habilitar CORS para permitir solicitudes desde AppSheet o cualquier otro origen
CORS(app) 

@app.route('/process', methods=['POST'])
def process_data():
    """
    Recibe los límites y la cantidad, genera N números aleatorios y
    devuelve el resultado, la fecha de generación y el código de estado.
    """
    try:
        # 1. Obtener los datos JSON de la solicitud POST
        data = request.get_json(force=True)
        
        # 2. Extraer y convertir los datos de entrada
        # Se asume que AppSheet envía los valores como strings (Tipo TEXTO)
        limite_inf_str = data.get('LimiteInferior')
        limite_sup_str = data.get('LimiteSuperior')
        cantidad_str = data.get('Cantidad')

        # Si falta algún dato, devuelve un error 400
        if not limite_inf_str or not limite_sup_str or not cantidad_str:
            return jsonify({
                "Resultado": "ERROR: Faltan datos de entrada (Limite, Cantidad)",
                "FechaGeneracion": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "CODIGO_STATUS": 400
            }), 400 # Error del cliente (Bad Request)

        # 3. Conversión de Tipos (Intentar convertir a entero)
        limite_inf = int(limite_inf_str)
        limite_sup = int(limite_sup_str)
        cantidad = int(cantidad_str)

        # 4. Validación de Límites
        if limite_inf >= limite_sup:
            return jsonify({
                "Resultado": "ERROR: El Límite Inferior debe ser menor que el Límite Superior.",
                "FechaGeneracion": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "CODIGO_STATUS": 400
            }), 400
        
        if cantidad <= 0:
            return jsonify({
                "Resultado": "ERROR: La Cantidad debe ser mayor que cero.",
                "FechaGeneracion": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "CODIGO_STATUS": 400
            }), 400

        # 5. Generación de números aleatorios
        numeros_aleatorios = [
            str(random.randint(limite_inf, limite_sup)) 
            for _ in range(cantidad)
        ]
        
        # Unir la lista en una sola cadena separada por comas
        resultado_final = ", ".join(numeros_aleatorios)

        # 6. Devolver la respuesta JSON de éxito (CODIGO_STATUS 200)
        return jsonify({
            "Resultado": resultado_final, # Clave que coincide con la columna de AppSheet
            "FechaGeneracion": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "CODIGO_STATUS": 200 
        }), 200

    except ValueError:
        # Captura el error si la conversión a int falla (si AppSheet no envía strings)
        return jsonify({
            "Resultado": "ERROR: Los límites o cantidad no son números válidos. Revise el tipo de dato en AppSheet.",
            "FechaGeneracion": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "CODIGO_STATUS": 400
        }), 400
    except Exception as e:
        # Captura cualquier otro error del servidor
        return jsonify({
            "Resultado": f"ERROR INTERNO: {str(e)}",
            "FechaGeneracion": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "CODIGO_STATUS": 500
        }), 500

if __name__ == '__main__':
    # Usar puerto para despliegue local o para Render (aunque Render usa Gunicorn)
    app.run(host='0.0.0.0', port=5000)
