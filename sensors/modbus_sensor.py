import socket
import json
import time
import random
from threading import Thread

def handle_client(client_socket):
    """Simule un serveur Modbus simplifié"""
    try:
        # Simuler la lecture de registres Modbus
        data = {
            "sensor_id": "modbus_sensor_1",
            "voltage": random.uniform(220.0, 240.0),
            "current": random.uniform(1.0, 5.0),
            "timestamp": time.time(),
            "type": "normal"
        }
        
        # Envoyer les données comme réponse Modbus simplifiée
        response = json.dumps(data).encode()
        client_socket.send(response)
    finally:
        client_socket.close()

def start_modbus_server():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(('0.0.0.0', 5021))
    server.listen(5)
    
    print("Serveur Modbus simulé démarré sur port 5021...")
    
    while True:
        client, addr = server.accept()
        print(f"Connexion Modbus depuis {addr}")
        client_handler = Thread(target=handle_client, args=(client,))
        client_handler.start()

if __name__ == '__main__':
    start_modbus_server()