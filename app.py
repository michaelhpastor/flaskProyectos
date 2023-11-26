from flask import Flask, jsonify, request
from users import users
from establecimientos import establecimientos
from empleados import empleados
from database import create_app

app = Flask(__name__)
create_app(app)

@app.route('/', methods=['GET', 'POST', 'PUT', 'DELETE'])
def index():
    if request.method == 'GET':
        return jsonify({'metodo': 'GET vista index'})
    elif request.method == 'POST':
        return jsonify({'metodo': 'POST'})
    else:
        return jsonify({'metodo': request.method})


@app.route('/hello')
def hello():
    return jsonify({'mensaje': 'vista Hello'})

@app.route('/user/<nombre>')
def user(nombre):
    return jsonify({'nombre': 'el usuario se llama {nombre}'})

if __name__ == '__main__':
    app.register_blueprint(users)
    app.register_blueprint(establecimientos)
    app.register_blueprint(empleados)
    app.run(debug=True)