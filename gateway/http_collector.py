import requests
import time
import threading

class HTTPCollector:
    def __init__(self, callback):
        self.callback = callback
        self.running = False
        self.url = "http://localhost:5001/data"
    
    def collect(self):
        while self.running:
            try:
                response = requests.get(self.url, timeout=5)
                if response.status_code == 200:
                    data = response.json()
                    self.callback("http_sensor", data)
            except Exception as e:
                print(f"Erreur HTTP: {e}")
            
            time.sleep(6)  # Collecte toutes les 6 secondes
    
    def start(self):
        self.running = True
        self.thread = threading.Thread(target=self.collect)
        self.thread.daemon = True
        self.thread.start()
        print("Collecteur HTTP démarré")
    
    def stop(self):
        self.running = False