from flask import Flask, render_template, request, jsonify
import json, logging, os, atexit
import nuevo


app = Flask(__name__, static_url_path='')
port = int(os.getenv('PORT', 8000))


@app.route('/main/<int:N>', methods=['GET', 'POST'])
def main(N):
    global city
    city = nuevo.City(N,10,10)
    city.showGraph()
    return "Ciudad creada"

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
    result = city.getTL()
    return result

@app.route('/getGoal', methods=['GET', 'POST'])
def getGoal():
    result = city.getGoal()
    return result



if __name__ == '__main__':
    app.run(host='0.0.0.0', port=port, debug=True)

