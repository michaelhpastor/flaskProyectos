from flask import Flask, jsonify, request
from empleados import empleados
from database import obtener_conexion
from database import create_app
from flask_cors import CORS

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})
create_app(app)

@app.route('/', methods=['GET', 'POST', 'PUT', 'DELETE'])
def index():
    if request.method == 'GET':
        return jsonify({'metodo': 'GET vista index'})
    elif request.method == 'POST':
        return jsonify({'metodo': 'POST'})
    else:
        return jsonify({'metodo': request.method})
    

@app.route('/establecimientos')
def establecimientos():
    try:
        # Obtener una conexión
        connection = obtener_conexion()

        with connection.cursor() as cursor:
            # Ejecutar una consulta para obtener datos de la base de datos
            cursor.execute("SELECT * FROM establecimientos")
            data = cursor.fetchall()

        # Convertir los resultados a un formato JSON y retornarlos
        result = jsonify(data)
        return result
    except Exception as e:
        return str(e)
    finally:
        # Cerrar la conexión después de usarla
        connection.close()

if __name__ == '__main__':
    #app.register_blueprint(establecimientos)
    #app.register_blueprint(users)
    app.register_blueprint(empleados)
    app.run(debug=True)
   
    