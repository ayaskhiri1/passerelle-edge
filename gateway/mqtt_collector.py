import json
import threading
import socket
import time

class MQTTCollector:
    def __init__(self, callback):
        self.callback = callback
        self.running = False
        
    def start_server(self):
        """Démarre un serveur TCP simple qui simule un broker MQTT"""
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server.bind(('0.0.0.0', 1883))
        server.listen(5)
        server.settimeout(1.0)
        
        print("Serveur MQTT simulé démarré sur port 1883...")
        
        while self.running:
            try:
                client, addr = server.accept()
                data = client.recv(1024)
                if data:
                    try:
                        parsed_data = json.loads(data.decode())
                        self.callback("mqtt_sensor", parsed_data)
                        print(f"MQTT reçu de {addr}: {parsed_data}")
                    except json.JSONDecodeError:
                        print(f"Données non JSON: {data}")
                client.close()
            except socket.timeout:
                continue
            except Exception as e:
                print(f"Erreur serveur MQTT: {e}")
        
        server.close()
    
    def start(self):
        self.running = True
        self.thread = threading.Thread(target=self.start_server)
        self.thread.daemon = True
        self.thread.start()
        print("Collecteur MQTT démarré (simulation)")
    
    def stop(self):
        self.running = False