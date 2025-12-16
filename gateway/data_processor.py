class DataProcessor:
    def process(self, batch):
        """Traiter un lot de données"""
        processed = []
        
        for item in batch:
            data = item['data']
            sensor_id = item['sensor_id']
            
            # 1. Filtrage des valeurs aberrantes
            if self.filter_outliers(data):
                print(f"Données filtrées (outlier): {sensor_id}")
                continue
            
            # 2. Ajout de métadonnées
            processed_item = {
                'sensor_id': sensor_id,
                'data': data,
                'processed_time': item['timestamp'].isoformat(),
                'priority': 'high' if data.get('type') == 'critical' else 'normal'
            }
            
            # 3. Agrégation simple (simulée)
            if 'temperature' in data:
                processed_item['data']['temperature_celsius'] = data['temperature']
                if 'humidity' in data:
                    processed_item['data']['heat_index'] = self.calculate_heat_index(
                        data['temperature'], data['humidity']
                    )
            
            processed.append(processed_item)
        
        return processed
    
    def filter_outliers(self, data):
        """Filtrer les valeurs aberrantes"""
        if 'temperature' in data and (data['temperature'] < -50 or data['temperature'] > 100):
            return True
        if 'pressure' in data and (data['pressure'] < 800 or data['pressure'] > 1200):
            return True
        return False
    
    def calculate_heat_index(self, temp, humidity):
        """Calculer l'indice de chaleur (simplifié)"""
        return temp + 0.05 * humidity  # Formule simplifiée