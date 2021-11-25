from flask import Flask, render_template, request, jsonify
import json, logging, os, atexit

app = Flask(__name__, static_url_path='')
port = int(os.getenv('PORT', 8000))

@app.route('/tablero')
def make_board():
    return "tablero"

@app.route('/movimiento/<int:id>')

def movement(id):
    message = "movimiento" + str(id)
    return message

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=port, debug=True)

