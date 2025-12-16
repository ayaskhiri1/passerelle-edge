from flask import Flask, jsonify
import random
import time

app = Flask(__name__)

@app.route('/data', methods=['GET'])
def get_data():
    data = {
        "sensor_id": "http_sensor_1",
        "pressure": random.uniform(1000.0, 1020.0),
        "timestamp": time.time()
    }
    print(f"HTTP envoyé: {data}")
    return jsonify(data)

if __name__ == '__main__':
    print("HTTP Sensor démarré sur http://localhost:5001/data")
    # Utiliser threaded=False pour éviter problèmes
    app.run(host='0.0.0.0', port=5001, debug=False, threaded=False)