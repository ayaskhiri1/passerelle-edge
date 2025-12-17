import socket
import json
import time
import threading

class CANCollector:
    def __init__(self, callback):
        self.callback = callback
        self.running = False
    
    def collect(self):
        """Collecter les données CAN Bus"""
        while self.running:
            try:
                # Connexion au capteur CAN sur port 5022
                client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                client.connect(('localhost', 5022))
                client.settimeout(2.0)
                
                # Recevoir les données
                data = client.recv(1024)
                if data:
                    parsed_data = json.loads(data.decode())
                    self.callback("can_sensor", parsed_data)
                
                client.close()
            except socket.timeout:
                pass  # Timeout normal
            except ConnectionRefusedError:
                print("⚠️ Capteur CAN non disponible")
                time.sleep(5)
            except Exception as e:
                print(f"Erreur CAN Collector: {e}")
            
            time.sleep(7)  # Collecte toutes les 7 secondes
    
    def start(self):
        self.running = True
        self.thread = threading.Thread(target=self.collect)
        self.thread.daemon = True
        self.thread.start()
        print("Collecteur CAN démarré")
    
    def stop(self):
        self.running = False