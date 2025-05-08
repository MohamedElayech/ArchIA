from flask import Flask, request, jsonify
from elfinale import gbt
app = Flask(__name__)


# API endpoint to call the function
@app.route('/run_gbt', methods=['POST'])
def run_gbt():
    data = request.json.get('input')  # get the 'input' field from the JSON request
    layers = request.json.get('layers', [])
    display = request.json.get('layout')
    result = gbt(data,layers,display)
    print(result)  # This will show in your terminal where Flask is running
    return jsonify({"result": result})

if __name__ == '__main__':
    app.run(debug=True)
