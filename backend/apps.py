from flask import request

from dotenv import load_dotenv
load_dotenv()


from flask import Flask, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})   # allow all origins



from utils import load_data, analyze_data, generate_heatmap, generate_summary
import sys
import os

def get_filtered_data(data, ward):
    if ward:
        return [item for item in data if item.get('ward') == ward]
    return data

sys.path.append(os.path.abspath("../"))



# Endpoint: /analyze
@app.route('/analyze', methods=['GET'])
def analyze():
    ward = request.args.get('ward')

    data = load_data()

    if ward:
        data = [d for d in data if d.get("ward") == ward]

    result = analyze_data(data)

    return jsonify(result)


# Endpoint: /heatmap
@app.route('/heatmap', methods=['GET'])
def heatmap():
    data = load_data()

    heatmap_data = {}

    for item in data:
        ward = item.get("ward")

        if ward not in heatmap_data:
            heatmap_data[ward] = {"count": 0}

        heatmap_data[ward]["count"] += 1

    return jsonify(heatmap_data)


# Endpoint: /summary
@app.route('/summary', methods=['GET'])
def summary():
    ward = request.args.get('ward')

    data = load_data()

    if ward:
        data = [d for d in data if d.get("ward") == ward]

    result = generate_summary(data)

    return jsonify({"summary": result})



from groq import Groq

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

@app.route('/solutions', methods=['POST'])
def get_solutions():
    try:
        data = request.json
        topics = data.get("top_topics", [])

        prompt = f"""
You are a civic advisor for Delhi.

Ward: {data.get("ward")}

Top issues:
{topics}

Provide solutions in this format:

**Section Title**
* point 1
* point 2

Keep it practical, short, and specific to the ward.
Avoid generic global issues.
"""

        response = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[
                {"role": "user", "content": prompt}
            ]
        )

        output = response.choices[0].message.content

        return jsonify({"solutions": output})

    except Exception as e:
        print("ERROR:", e)
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)

