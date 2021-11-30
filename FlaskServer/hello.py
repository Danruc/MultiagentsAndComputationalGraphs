from flask import Flask, render_template, request, jsonify
import json, logging, os, atexit
import nodos


app = Flask(__name__, static_url_path='')
port = int(os.getenv('PORT', 8000))

@app.route('/board/<int:size>/<int:percent>/<int:N>', methods=['GET', 'POST'])
def make_board(size,percent, N):
    global city 
    city = nodos.City(size, percent, N)
    graph = city.getCity()
    return jsonify(graph)

@app.route('/position', methods=['GET', 'POST'])
def initialPos():
    result = city.getPositions()
    return jsonify(result)

@app.route('/step', methods=['GET', 'POST'])
def movement():
    result = city.step()
    return jsonify(result)


@app.route('/tl', methods=['GET', 'POST'])
def traffic():
    result = city.getTrafficLight()
    return jsonify(result)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=port, debug=True)

