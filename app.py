from flask import Flask, request, jsonify
from flask_cors import CORS
import json
import random
import os

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
    state_normalized = state.strip().lower()
    matched_state = None
    for s in state_city_map.keys():
        if s.lower() == state_normalized:
            matched_state = s
            break
    if not matched_state:
        return jsonify({"error": f"State '{state}' not found"}), 404

    cities = list(state_city_map[matched_state].keys())
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

# Only used for local testing
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=True)






