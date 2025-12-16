#Simuler un capteur HTTP

from flask import Flask, jsonify
import random
import time
from threading import Thread

app = Flask(__name__)

sensor_data = {
    "sensor_id": "http_sensor_1",
    "pressure": 1013.25,
    "timestamp": time.time()
}

def update_data():
    while True:
        sensor_data["pressure"] = random.uniform(1000.0, 1020.0)
        sensor_data["timestamp"] = time.time()
        time.sleep(7)

@app.route('/data', methods=['GET'])
def get_data():
    return jsonify(sensor_data)

if __name__ == '__main__':
    # Démarrer la mise à jour des données en arrière-plan
    updater = Thread(target=update_data)
    updater.daemon = True
    updater.start()
    
    print("Capteur HTTP démarré sur http://localhost:5001/data")
    app.run(host='0.0.0.0', port=5001)