import time
from datetime import datetime

# Modules corrigés
from mqtt_collector import MQTTCollector
from http_collector import HTTPCollector
from modbus_collector import ModbusCollector
from data_processor import DataProcessor
from adaptive_router import AdaptiveRouter

class SmartGateway:
    def __init__(self):
        
        self.data_buffer = []
        self.processor = DataProcessor()
        self.router = AdaptiveRouter()
        
        self.collectors = [
            HTTPCollector(self.on_data_received),
            ModbusCollector(self.on_data_received)
        ]
        
        # SIMPLIFIÉ: pas de SQLite pour la démo
        print("Passerelle démarrée (sans cache SQLite)")
    
    def on_data_received(self, sensor_id, data):
        print(f"[{datetime.now().strftime('%H:%M:%S')}] {sensor_id}: {data}")
        
        # Traitement immédiat
        processed = self.processor.process([{
            'sensor_id': sensor_id,
            'data': data,
            'timestamp': datetime.now()
        }])
        
        # Routage immédiat
        if processed:
            success = self.router.route(processed[0])
            if not success:
                print(f"⚠️ Données perdues: {sensor_id}")
    
    def start(self):
        print("=== Passerelle Intelligente ===")
        
        for collector in self.collectors:
            collector.start()
        
        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            self.stop()
    
    def stop(self):
        for collector in self.collectors:
            collector.stop()
        print("Passerelle arrêtée")

if __name__ == "__main__":
    gateway = SmartGateway()
    gateway.start()