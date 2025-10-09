import json
import random
from datetime import datetime
from flask import Flask, request, jsonify

app = Flask(__name__)

# Función para generar números aleatorios
def generar_numeros_aleatorios(inferior, superior, cantidad):
    if inferior >= superior or cantidad <= 0:
        # Devuelve None si los parámetros son inválidos
        return None 
    
    numeros = random.sample(range(inferior, superior + 1), min(cantidad, superior - inferior + 1))
    return ",".join(map(str, numeros))

@app.route('/generar_numeros', methods=['POST'])
def generar_numeros():
    try:
        data = request.get_json()
        
        # Validar y convertir datos (AppSheet envía los números como texto)
        try:
            limite_inferior = int(data.get('LimiteInferior'))
            limite_superior = int(data.get('LimiteSuperior'))
            cantidad = int(data.get('Cantidad'))
        except (ValueError, TypeError):
            # Error de datos inválidos
            response = {
                "resultado": "",
                "fechageneracion": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "codigo_status": "400",
                "mensaje_error": "Error: Los límites o la cantidad no son números válidos."
            }
            return jsonify(response), 400

        # Generar números
        resultado_str = generar_numeros_aleatorios(limite_inferior, limite_superior, cantidad)

        if resultado_str is None:
             response = {
                "resultado": "",
                "fechageneracion": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "codigo_status": "400",
                "mensaje_error": "Error: Rango inválido o cantidad excede el rango."
            }
             return jsonify(response), 400
        
        # Respuesta exitosa con claves en minúsculas
        response = {
            "resultado": resultado_str,
            "fechageneracion": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "codigo_status": "200",
            "mensaje_error": "transaccion completada exitosamente."
        }
        
        return jsonify(response), 200

    except Exception as e:
        # Error interno del servidor
        print(f"Error: {e}")
        response = {
            "resultado": "",
            "fechageneracion": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "codigo_status": "500",
            "mensaje_error": f"Error interno del servidor: {str(e)}"
        }
        return jsonify(response), 500
