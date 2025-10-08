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
        # Se asume que AppSheet envia los valores como strings (Tipo TEXTO)
        limite_inf_str = data.get('LimiteInferior')
        limite_sup_str = data.get('LimiteSuperior')
        cantidad_str = data.get('Cantidad')

        # Si falta algún dato, devuelve un error 400
        if not limite_inf_str or not limite_sup_str or not cantidad_str:
            return jsonify({
                "NúmerosGenerados": "",
                "FechaGeneracion": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "CODIGO_STATUS": "400",
                "MENSAJE_ERROR": "Error: Faltan uno o más parámetros de entrada (LimiteInferior, LimiteSuperior o Cantidad)."
            }), 400

        try:
            limite_inf = int(limite_inf_str)
            limite_sup = int(limite_sup_str)
            cantidad = int(cantidad_str)
        except ValueError:
             return jsonify({
                "NúmerosGenerados": "",
                "FechaGeneracion": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "CODIGO_STATUS": "400",
                "MENSAJE_ERROR": "Error: Los parámetros de entrada deben ser números enteros."
            }), 400

        # 3. Lógica de negocio: Generar N números aleatorios
        numeros = [str(random.randint(limite_inf, limite_sup)) for _ in range(cantidad)]
        resultado_str = ",".join(numeros)

        # 4. Preparar la respuesta de éxito
        response = {
            "NúmerosGenerados": resultado_str,  # ¡Clave cambiada a NúmerosGenerados!
            "FechaGeneracion": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "CODIGO_STATUS": "200",
            "MENSAJE_ERROR": "Transacción completada exitosamente."
        }
        
        return jsonify(response), 200

    except Exception as e:
        # Manejo de cualquier otro error del servidor
        return jsonify({
            "NúmerosGenerados": "",
            "FechaGeneracion": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "CODIGO_STATUS": "500",
            "MENSAJE_ERROR": f"Error interno del servidor: {str(e)}"
        }), 500

if __name__ == '__main__':
    app.run(debug=True)