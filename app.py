from flask import Flask, jsonify, request
from database import obtener_conexion
from database import create_app
from flask_cors import CORS
import hashlib

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
    
def hash_password(password):
    sha256_hash = hashlib.sha256()
    sha256_hash.update(password.encode('utf-8'))
    hashed_password = sha256_hash.hexdigest()
    return hashed_password


#----------------------------------------------------------------------------------------------------------- AUTH
@app.route('/auth/', methods=['POST'])
def auth_route():
    user_data = request.json
    correo = user_data.get('correo')
    contrasena = user_data.get('contrasena')
    try:
        # Obtener una conexión
        connection = obtener_conexion()

         # Hashear la contraseña
        hashed_password = hash_password(contrasena)

        with connection.cursor() as cursor:
                cursor.execute("SELECT * FROM usuarios WHERE correo = %s AND contrasena = %s", (correo,hashed_password ))
                data = cursor.fetchall()
        result = jsonify(data)
        return result

    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        connection.close()


#----------------------------------------------------------------------------------------------------------- RUTA AGENDA USUARIOS
@app.route('/agendaUsuario/<id>', methods=['GET'])
def agendaUsuarios_route(id):

    try:
        # Obtener una conexión
        connection = obtener_conexion()

        with connection.cursor() as cursor:
                cursor.execute("SELECT * FROM agendaEmpleados, agendaEspecialista WHERE idUsuario = %s ", (id))
                data = cursor.fetchall()
        result = jsonify(data)
        return result

    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        connection.close()


#----------------------------------------------------------------------------------------------------------- RUTA USUARIOS
@app.route('/users', methods=['GET', 'POST', 'PUT', 'DELETE'])
def users_route():
    try:
        connection = obtener_conexion()

        if request.method == 'GET':
            with connection.cursor() as cursor:
                cursor.execute("SELECT * FROM usuarios")
                data = cursor.fetchall()
            result = jsonify(data)
            return result
        elif request.method == 'POST':
            # Obtener los datos del usuario desde el cuerpo de la solicitud
            user_data = request.json
            nombre = user_data.get('nombre')
            apellido = user_data.get('apellido')
            cedula = user_data.get('cedula')
            correo = user_data.get('correo')
            contrasena = user_data.get('contrasena')

            # Hashear la contraseña
            hashed_password = hash_password(contrasena)
            
            # Agregar lógica para otros campos del usuario según tu esquema de base de datos

            with connection.cursor() as cursor:
                # Ejecutar la consulta para insertar un nuevo usuario
                cursor.execute("INSERT INTO usuarios (nombre, apellido, cedula, correo, contrasena, rol) VALUES (%s, %s, %s, %s, %s, %s)", (nombre, apellido, cedula, correo, hashed_password, 'usuario'))
                connection.commit()

            return jsonify({"message": "Usuario creado exitosamente"}), 201
        elif request.method == 'PUT':
            # Obtener los datos del usuario desde el cuerpo de la solicitud
            user_data = request.json
            id_usuario = user_data.get('id')  # Suponiendo que el ID del usuario está presente en los datos
            nombre = user_data.get('nombre')
            apellido = user_data.get('apellido')
            cedula = user_data.get('cedula')
            correo = user_data.get('correo')
            contrasena = user_data.get('contrasena')

            # Hashear la contraseña
            hashed_password = hash_password(contrasena)
            
            with connection.cursor() as cursor:
                # Ejecutar la consulta para actualizar los datos del usuario
                cursor.execute("UPDATE usuarios SET nombre = %s, apellido = %s, cedula = %s, correo = %s, contrasena = %s WHERE id = %s", (nombre, apellido, cedula, correo, hashed_password, id_usuario))
                connection.commit()

            return jsonify({"message": "Usuario actualizado exitosamente"}), 200
        elif request.method == 'DELETE':
            # Obtener el ID del usuario a borrar desde el cuerpo de la solicitud
            user_data = request.json
            id_usuario = user_data.get('id')  # Suponiendo que el ID del usuario está presente en los datos
            
            with connection.cursor() as cursor:
                # Ejecutar la consulta para borrar un usuario
                cursor.execute("DELETE FROM usuarios WHERE id = %s", (id_usuario,))
                connection.commit()

            return jsonify({"message": "Usuario eliminado exitosamente"}), 200
        else:
            return jsonify({"error": "Método no permitido"}), 405
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        connection.close()


#----------------------------------------------------------------------------------------------------------- RUTA EMPLEADOS
@app.route('/empleados/<id>', methods=['GET', 'POST', 'PUT', 'DELETE'])
def empleados_route(id):
    try:
        # Obtener una conexión
        connection = obtener_conexion()

        if request.method == 'GET':
            with connection.cursor() as cursor:
                cursor.execute("SELECT * FROM empleados WHERE idEstablecimiento = %s", (id))
                data = cursor.fetchall()
            result = jsonify(data)
            return result
        elif request.method == 'POST':
            # Obtener los datos del empleado desde el cuerpo de la solicitud
            empleados_data = request.json
            nombre = empleados_data.get('nombre')
            apellido = empleados_data.get('apellido')
            imagen = empleados_data.get('imagen')
            horario = empleados_data.get('horario')
            
            # Agregar lógica para otros campos del empleado según tu esquema de base de datos

            with connection.cursor() as cursor:
                # Ejecutar la consulta para insertar un nuevo empleado
                cursor.execute("INSERT INTO empleados (idEstablecimiento, nombre, apellido, imagen, horario) VALUES (%s, %s, %s, %s, %s)", (2, nombre, apellido, imagen, horario))
                connection.commit()

            return jsonify({"message": "Empleado creado exitosamente"}), 201
        elif request.method == 'PUT':
            # Obtener los datos del empleado desde el cuerpo de la solicitud
            empleados_data = request.json
            id_empleado = empleados_data.get('id')  # Suponiendo que el ID del empleado está presente en los datos
            nombre = empleados_data.get('nombre')
            apellido = empleados_data.get('apellido')
            imagen = empleados_data.get('imagen')
            horario = empleados_data.get('horario')
            
            with connection.cursor() as cursor:
                # Ejecutar la consulta para actualizar los datos del empleado
                cursor.execute("UPDATE empleados SET nombre = %s, apellido = %s, imagen = %s, horario = %s WHERE id = %s", (nombre, apellido, imagen, horario, id_empleado))
                connection.commit()

            return jsonify({"message": "Empleado actualizado exitosamente"}), 200
        elif request.method == 'DELETE':
            # Obtener el ID del empleado a borrar desde el cuerpo de la solicitud
            empleados_data = request.json
            id_empleado = empleados_data.get('id')  # Suponiendo que el ID del empleado está presente en los datos
            
            with connection.cursor() as cursor:
                # Ejecutar la consulta para borrar un empleado
                cursor.execute("DELETE FROM empleados WHERE id = %s", (id_empleado,))
                connection.commit()

            return jsonify({"message": "Empleado eliminado exitosamente"}), 200
        else:
            return jsonify({"error": "Método no permitido"}), 405
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        connection.close()


#----------------------------------------------------------------------------------------------------------- RUTA ESPECIALISTA
@app.route('/especialistas', methods=['GET', 'POST', 'PUT', 'DELETE'])
def especialistas_route():
    try:
        connection = obtener_conexion()

        if request.method == 'GET':
            with connection.cursor() as cursor:
                cursor.execute("SELECT * FROM especialistas")
                data = cursor.fetchall()
            result = jsonify(data)
            return result
        elif request.method == 'POST':
            # Obtener los datos del usuario desde el cuerpo de la solicitud
            especialista_data = request.json
            nombre = especialista_data.get('nombre')
            apellido = especialista_data.get('apellido')
            telefono = especialista_data.get('telefono')
            imagen = especialista_data.get('imagen')
            horario = especialista_data.get('horario')
            
            # Agregar lógica para otros campos del usuario según tu esquema de base de datos

            with connection.cursor() as cursor:
                # Ejecutar la consulta para insertar un nuevo usuario
                cursor.execute("INSERT INTO especialistas (nombre, apellido, telefono, imagen, horario) VALUES (%s, %s, %s, %s, %s)", (nombre, apellido, telefono, imagen, horario))
                connection.commit()

            return jsonify({"message": "Especialista creado exitosamente"}), 201
        elif request.method == 'PUT':
            # Obtener los datos del usuario desde el cuerpo de la solicitud
            especialista_data = request.json
            id_especialista = especialista_data.get('id')  # Suponiendo que el ID del especialista está presente en los datos
            nombre = especialista_data.get('nombre')
            apellido = especialista_data.get('apellido')
            telefono = especialista_data.get('telefono')
            imagen = especialista_data.get('imagen')
            horario = especialista_data.get('horario')
            
            with connection.cursor() as cursor:
                # Ejecutar la consulta para actualizar los datos del usuario
                cursor.execute("UPDATE especialistas SET nombre = %s, apellido = %s, telefono = %s, imagen = %s, horario = %s WHERE id = %s", (nombre, apellido, telefono, imagen, horario, id_especialista))
                connection.commit()

            return jsonify({"message": "Especialista actualizado exitosamente"}), 200
        elif request.method == 'DELETE':
            # Obtener el ID del usuario a borrar desde el cuerpo de la solicitud
            especialista_data = request.json
            id_especialista = especialista_data.get('id')  # Suponiendo que el ID del especialista está presente en los datos
            
            with connection.cursor() as cursor:
                # Ejecutar la consulta para borrar un usuario
                cursor.execute("DELETE FROM especialistas WHERE id = %s", (id_especialista,))
                connection.commit()

            return jsonify({"message": "Especialista eliminado exitosamente"}), 200
        else:
            return jsonify({"error": "Método no permitido"}), 405
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        connection.close()


#----------------------------------------------------------------------------------------------------------- RUTA ESTABLECIMIENTOS
@app.route('/establecimientos', methods=['GET', 'POST', 'PUT', 'DELETE'])
def establecimientos_route():
    try:
        # Obtener una conexión
        connection = obtener_conexion()

        if request.method == 'GET':
            with connection.cursor() as cursor:
                cursor.execute("SELECT * FROM establecimientos")
                data = cursor.fetchall()
            result = jsonify(data)
            return result
        elif request.method == 'POST':
            # Obtener los datos del establecimiento desde el cuerpo de la solicitud
            establecimientos_data = request.json
            nombre = establecimientos_data.get('nombre')
            direccion = establecimientos_data.get('direccion')
            ciudad = establecimientos_data.get('ciudad')
            imagen = establecimientos_data.get('imagen')
            horario = establecimientos_data.get('horario')
            
            # Agregar lógica para otros campos del establecimiento según tu esquema de base de datos

            with connection.cursor() as cursor:
                # Ejecutar la consulta para insertar un nuevo establecimiento
                cursor.execute("INSERT INTO establecimientos (nombre, direccion, ciudad, imagen, horario) VALUES (%s, %s, %s, %s, %s)", (nombre, direccion, ciudad, imagen, horario))
                connection.commit()

            return jsonify({"message": "Establecimiento creado exitosamente"}), 201
        elif request.method == 'PUT':
            # Obtener los datos del establecimiento desde el cuerpo de la solicitud
            establecimientos_data = request.json
            id_establecimiento = establecimientos_data.get('id')  # Suponiendo que el ID del establecimiento está presente en los datos
            nombre = establecimientos_data.get('nombre')
            direccion = establecimientos_data.get('direccion')
            ciudad = establecimientos_data.get('ciudad')
            imagen = establecimientos_data.get('imagen')
            horario = establecimientos_data.get('horario')
            
            with connection.cursor() as cursor:
                # Ejecutar la consulta para actualizar los datos del establecimiento
                cursor.execute("UPDATE establecimientos SET nombre = %s, direccion = %s, ciudad = %s, imagen = %s, horario = %s WHERE id = %s", (nombre, direccion, ciudad, imagen, horario, id_establecimiento))
                connection.commit()

            return jsonify({"message": "Establecimiento actualizado exitosamente"}), 200
        elif request.method == 'DELETE':
            # Obtener el ID del establecimiento a borrar desde el cuerpo de la solicitud
            establecimientos_data = request.json
            id_establecimiento = establecimientos_data.get('id')  # Suponiendo que el ID del establecimiento está presente en los datos
            
            with connection.cursor() as cursor:
                # Ejecutar la consulta para borrar un establecimiento
                cursor.execute("DELETE FROM establecimientos WHERE id = %s", (id_establecimiento,))
                connection.commit()

            return jsonify({"message": "Establecimiento eliminado exitosamente"}), 200
        else:
            return jsonify({"error": "Método no permitido"}), 405
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        connection.close()


#----------------------------------------------------------------------------------------------------------- RUTA AGENDA EMPLEADOS
@app.route('/agendaEmpleados/<idempleado>/<idUsuario>', methods=['GET', 'POST', 'PUT', 'DELETE'])
def agendaEmpleados_route(idempleado,idUsuario):
    try:
        connection = obtener_conexion()

        if request.method == 'GET':
            with connection.cursor() as cursor:
                cursor.execute("SELECT * FROM agendaEmpleados WHERE idempleado = %s AND idUsuario = %s", (idempleado,idUsuario))
                data = cursor.fetchall()
            result = jsonify(data)
            return result
        elif request.method == 'POST':
            # Obtener los datos del usuario desde el cuerpo de la solicitud
            agendaEmpleados_data = request.json
            fecha = agendaEmpleados_data.get('fecha')
            hora = agendaEmpleados_data.get('hora')
                     
            # Agregar lógica para otros campos del usuario según tu esquema de base de datos

            with connection.cursor() as cursor:
                # Ejecutar la consulta para insertar un nuevo usuario
                cursor.execute("INSERT INTO agendaEmpleados (idempleado, idUsuario, fecha, hora) VALUES (%s, %s, %s, %s)", (2, 2, fecha, hora))
                connection.commit()

            return jsonify({"message": "La agenda de empleados creada exitosamente"}), 201
        elif request.method == 'PUT':
            # Obtener los datos del usuario desde el cuerpo de la solicitud
            agendaEmpleados_data= request.json
            id_agendaEmpleados = agendaEmpleados_data.get('id')  # Suponiendo que el ID del usuario está presente en los datos
            fecha = agendaEmpleados_data.get('fecha')
            hora = agendaEmpleados_data.get('hora')
            
            with connection.cursor() as cursor:
                # Ejecutar la consulta para actualizar los datos del usuario
                cursor.execute("UPDATE agendaEmpleados SET fecha = %s, hora = %s WHERE id = %s", (fecha, hora, id_agendaEmpleados))
                connection.commit()

            return jsonify({"message": "La agenda de empleados actualizada exitosamente"}), 200
        elif request.method == 'DELETE':
            # Obtener el ID del usuario a borrar desde el cuerpo de la solicitud
            agendaEmpleados_data = request.json
            id_agendaEmpleados = agendaEmpleados_data.get('id')  # Suponiendo que el ID del usuario está presente en los datos
            
            with connection.cursor() as cursor:
                # Ejecutar la consulta para borrar un usuario
                cursor.execute("DELETE FROM agendaEmpleados WHERE id = %s", (id_agendaEmpleados,))
                connection.commit()

            return jsonify({"message": "La agenda de empleados eliminada exitosamente"}), 200
        else:
            return jsonify({"error": "Método no permitido"}), 405
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        connection.close()

#----------------------------------------------------------------------------------------------------------- RUTA AGENDA ESPECIALISTA
@app.route('/agendaEspecialista/<idEspecialista>/<idUsuario>', methods=['GET', 'POST', 'PUT', 'DELETE'])
def agendaEspecialista_route(idEspecialista,idUsuario):
    try:
        connection = obtener_conexion()

        if request.method == 'GET':
            with connection.cursor() as cursor:
                cursor.execute("SELECT * FROM agendaEspecialista WHERE idEspecialista = %s AND idUsuario = %s", (idEspecialista,idUsuario))
                data = cursor.fetchall()
            result = jsonify(data)
            return result
        elif request.method == 'POST':
            # Obtener los datos del usuario desde el cuerpo de la solicitud
            agendaEspecialista_data = request.json
            fecha = agendaEspecialista_data.get('fecha')
            hora = agendaEspecialista_data.get('hora')
            lugar = agendaEspecialista_data.get('lugar')
            
            # Agregar lógica para otros campos del usuario según tu esquema de base de datos

            with connection.cursor() as cursor:
                # Ejecutar la consulta para insertar un nuevo usuario
                cursor.execute("INSERT INTO agendaEspecialista (idEspecialista, idUsuario, fecha, hora, lugar) VALUES (%s, %s, %s, %s, %s)", (2, 2, fecha, hora, lugar))
                connection.commit()

            return jsonify({"message": "La agenda del especialista creada exitosamente"}), 201
        elif request.method == 'PUT':
            # Obtener los datos del usuario desde el cuerpo de la solicitud
            agendaEspecialista_data = request.json
            id_agendaEspecialista = agendaEspecialista_data.get('id')  # Suponiendo que el ID del usuario está presente en los datos
            fecha = agendaEspecialista_data.get('fecha')
            hora = agendaEspecialista_data.get('hora')
            lugar = agendaEspecialista_data.get('lugar')
            
            with connection.cursor() as cursor:
                # Ejecutar la consulta para actualizar los datos del usuario
                cursor.execute("UPDATE agendaEspecialista SET fecha = %s, hora = %s, lugar = %s WHERE id = %s", (fecha, hora, lugar, id_agendaEspecialista))
                connection.commit()

            return jsonify({"message": "La agenda del especialista actualizada exitosamente"}), 200
        elif request.method == 'DELETE':
            # Obtener el ID del usuario a borrar desde el cuerpo de la solicitud
            agendaEspecialista_data = request.json
            id_agendaEspecialista = agendaEspecialista_data.get('id')  # Suponiendo que el ID del usuario está presente en los datos
            
            with connection.cursor() as cursor:
                # Ejecutar la consulta para borrar un usuario
                cursor.execute("DELETE FROM agendaEspecialista WHERE id = %s", (id_agendaEspecialista,))
                connection.commit()

            return jsonify({"message": "La agenda del especialista eliminada exitosamente"}), 200
        else:
            return jsonify({"error": "Método no permitido"}), 405
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        connection.close()

@app.route('/empleados/<id>')
def empleados(id):
    try:
        # Obtener una conexión
        connection = obtener_conexion()

        with connection.cursor() as cursor:
            # Ejecutar una consulta para obtener datos de la base de datos
            cursor.execute("SELECT * FROM empleados  WHERE idEstablecimiento = %s", (id,))
            data = cursor.fetchall()

        # Convertir los resultados a un formato JSON y retornarlos
        result = jsonify(data)
        return result
    except Exception as e:
        return str(e)
    finally:
        # Cerrar la conexión después de usarla
        connection.close()


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
    app.run(debug=True)
   
    