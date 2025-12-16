import time
import json
import random
import threading
import socket

def simulate_mqtt_without_broker():
    """Simule l'envoi MQTT via un socket TCP simple"""
    while True:
        try:
            # Crée une connexion TCP comme le ferait MQTT
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.connect(('localhost', 1883))
            
            temperature = random.uniform(20.0, 30.0)
            humidity = random.uniform(40.0, 60.0)
            
            data = {
                "sensor_id": "mqtt_sensor_1",
                "temperature": round(temperature, 2),
                "humidity": round(humidity, 2),
                "timestamp": time.time(),
                "type": "critical" if temperature > 28 else "normal"
            }
            
            # Envoie les données
            sock.send(json.dumps(data).encode())
            sock.close()
            
            print(f"MQTT Simulé envoyé: {data}")
            
        except ConnectionRefusedError:
            print("⚠️  Broker MQTT non disponible - simulation en cours...")
            # Simule quand même la génération de données
            temperature = random.uniform(20.0, 30.0)
            humidity = random.uniform(40.0, 60.0)
            
            data = {
                "sensor_id": "mqtt_sensor_1",
                "temperature": round(temperature, 2),
                "humidity": round(humidity, 2),
                "timestamp": time.time(),
                "type": "critical" if temperature > 28 else "normal"
            }
            
            print(f"📤 Données générées (mode simulation): {data}")
            
        time.sleep(5)

if __name__ == "__main__":
    print("Capteur MQTT démarré (mode simulation)...")
    simulate_mqtt_without_broker()