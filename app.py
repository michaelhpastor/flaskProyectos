from flask import Flask, jsonify, request

app = Flask(__name__)

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
    app.run(debug=True)