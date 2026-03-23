from flask import Flask, jsonify
from utils import load_data, analyze_data, generate_heatmap, generate_summary

app = Flask(__name__)

# Endpoint: /analyze
@app.route('/analyze', methods=['GET'])
def analyze():
    data = load_data()
    result = analyze_data(data)
    return jsonify(result)

# Endpoint: /heatmap
@app.route('/heatmap', methods=['GET'])
def heatmap():
    data = load_data()
    result = generate_heatmap(data)
    return jsonify(result)

# Endpoint: /summary
@app.route('/summary', methods=['GET'])
def summary():
    data = load_data()
    result = generate_summary(data)
    return jsonify({"summary": result})

if __name__ == '__main__':
    app.run(debug=True)