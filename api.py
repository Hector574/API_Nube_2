from flask import Flask, jsonify
import random

app = Flask(__name__)

# Definición de la ruta: Acepta GET y POST (CRÍTICO para AppSheet)
@app.route('/generate_number', methods=['GET', 'POST'])
def generate_number():
    """Genera un número aleatorio entre 1 y 100 y lo devuelve en JSON."""
    random_number = random.randint(1, 100)
    # Formato de respuesta esperado por AppSheet (clave 'number')
    return jsonify({"number": random_number})

if __name__ == '__main__':
    # CORRECCIÓN CLAVE: El hosting en la nube requiere '0.0.0.0'
    app.run(host='0.0.0.0', port=5000, debug=True)