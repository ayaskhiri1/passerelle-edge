class SmartGateway:
    def __init__(self):
        self.data_buffer = []
        self.processor = DataProcessor()
        self.router = AdaptiveRouter()  # Utilise la nouvelle version
        self.cache = CacheManager()
        self.status_check_interval = 30  # Afficher le statut toutes les 30 secondes
        self.last_status_check = time.time()

        self.collectors = [
            HTTPCollector(self.on_data_received),
            ModbusCollector(self.on_data_received)
        ]
    
    def on_data_received(self, sensor_id, data):
        print(f"[{datetime.now().strftime('%H:%M:%S')}] {sensor_id}: {data}")
        
        # Afficher le statut périodiquement
        current_time = time.time()
        if current_time - self.last_status_check > self.status_check_interval:
            self.display_cloud_status()
            self.last_status_check = current_time
        
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
                self.cache.add(sensor_id, processed[0]['data'], processed[0]['priority'])
    
    def display_cloud_status(self):
        """Afficher le statut des clouds"""
        print("\n" + "="*50)
        print("📊 STATUT DES CLOUDS")
        print("="*50)
        
        status = self.router.get_status()
        for name, info in status.items():
            status_icon = "✅" if info['available'] else "❌"
            print(f"{status_icon} {info['name']}: {'Disponible' if info['available'] else 'Indisponible'}")
            print(f"   Dernière vérification: {info['last_check']}")
        print("="*50 + "\n")
    
    def start(self):
        print("=== Passerelle Intelligente ===")
        print("Système de routage adaptatif avec vérification santé automatique")
        print(f"Vérification santé toutes les {self.router.health_check_interval} secondes")
        
        # Afficher le statut initial
        self.display_cloud_status()
        
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
        print("\nPasserelle arrêtée")