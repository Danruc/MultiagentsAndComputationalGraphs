from flask import Flask, render_template, request, jsonify
import json, logging, os, atexit
import nodos


app = Flask(__name__, static_url_path='')
port = int(os.getenv('PORT', 8000))

@app.route('/tablero/<int:size>/<int:percent>', methods=['GET', 'POST'])
def make_board(size,percent):
    city = nodos.City(size, percent)
    graph = city.getCity()
    return jsonify(graph)


@app.route('/movimiento', methods=['GET', 'POST'])
def movement():
    dir = {1: {[1,2]:[1,0]}}
    return jsonify(dir)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=port, debug=True)

