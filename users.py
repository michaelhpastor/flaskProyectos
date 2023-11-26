from flask import Blueprint, jsonify, request
from database import obtener_conexion

users = Blueprint('users', __name__)

@users.route('/users', methods=['GET', 'POST', 'PUT', 'DELETE'])
def users_route():
    try:
        # Obtener una conexión
        connection = obtener_conexion()

        with connection.cursor() as cursor:
            # Ejecutar una consulta para obtener datos de la base de datos
            cursor.execute("SELECT * FROM usuarios")
            data = cursor.fetchall()

        # Convertir los resultados a un formato JSON y retornarlos
        result = jsonify(data)

        print(data[0]['nombre'])
        return result
    except Exception as e:
        return str(e)
    finally:
        # Cerrar la conexión después de usarla
        connection.close()