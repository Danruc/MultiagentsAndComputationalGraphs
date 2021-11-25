from flask import Flask
import json

app = Flask(__name__)

@app.route('/tablero')
def make_board():
    return "tablero"

@app.route('/movimiento/<int:id>')

def movement(id):
    message = "movimiento" + str(id)
    return message

if __name__ == '__main__':
    app.run(debug=True)

