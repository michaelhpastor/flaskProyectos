from flask import Blueprint, jsonify
from database import obtener_conexion

establecimientos = Blueprint('establecimientos', __name__)

@establecimientos.route('/establecimientos', methods=['GET'])
def establecimientos_route():
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