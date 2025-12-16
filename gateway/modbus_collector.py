import socket
import json
import time
import threading

class ModbusCollector:
    def __init__(self, callback):
        self.callback = callback
        self.running = False
    
    def collect(self):
        while self.running:
            try:
                # Simulation simple de connexion Modbus
                client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                client.connect(('localhost', 5021))
                client.settimeout(2.0)
                
                # Recevoir les données
                data = client.recv(1024)
                if data:
                    parsed_data = json.loads(data.decode())
                    self.callback("modbus_sensor", parsed_data)
                
                client.close()
            except Exception as e:
                print(f"Erreur Modbus: {e}")
            
            time.sleep(8)  # Collecte toutes les 8 secondes
    
    def start(self):
        self.running = True
        self.thread = threading.Thread(target=self.collect)
        self.thread.daemon = True
        self.thread.start()
        print("Collecteur Modbus démarré")
    
    def stop(self):
        self.running = False