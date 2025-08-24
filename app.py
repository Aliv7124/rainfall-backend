from flask import Flask, request, jsonify
from flask_cors import CORS
import json
import random

app = Flask(__name__)
CORS(app)

# Load state-city mapping (state -> city -> lat/lng)
with open("state_city_map.json", "r", encoding="utf-8") as f:
    state_city_map = json.load(f)

@app.route("/states", methods=["GET"])
def get_states():
    """Return all states"""
    return jsonify({"states": list(state_city_map.keys())})

@app.route("/cities/<state>", methods=["GET"])
def get_cities(state):
    """Return city names for a given state"""
    state = state.strip()
    if state not in state_city_map:
        return jsonify({"error": f"State '{state}' not found"}), 404

    # Return list of city names
    cities = list(state_city_map[state].keys())
    return jsonify({"cities": cities})

@app.route("/predict", methods=["POST"])
def predict():
    """Return dummy rainfall prediction"""
    try:
        data = request.get_json()
        location = data.get("location", "").strip()
        date = data.get("date", "").strip()

        if not location or not date:
            return jsonify({"error": "Location and date required"}), 400

        prediction = round(random.uniform(0, 200), 2)
        return jsonify({"prediction": prediction})

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)




