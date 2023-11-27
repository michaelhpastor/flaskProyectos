from flask import Blueprint, jsonify, request
from database import obtener_conexion

agendaEspecialista = Blueprint('agendaEspecialista', __name__)


@agendaEspecialista.route('/agendaEspecialista', methods=['GET', 'POST', 'PUT', 'DELETE'])
def agendaEmpleado_route():
    try:
        if request.method == 'GET':
            connection = obtener_conexion()

            with connection.cursor() as cursor:
            # Ejecutar una consulta para obtener datos de la base de datos
                cursor.execute("SELECT * FROM agendaEspecialistas")
                data = cursor.fetchall()

            # Convertir los resultados a un formato JSON y retornarlos
            result = jsonify(data)
            return result
        elif request.method == 'POST':
            pass

        elif request.method == 'PUT':
            pass
        elif request.method == 'DELETE':
            pass
    except Exception as e:
        return str(e)
    finally:
        # Cerrar la conexión después de usarla
        connection.close()
