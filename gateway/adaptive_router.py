import requests
import time
import random
from datetime import datetime

class AdaptiveRouter:
    def __init__(self):
        self.clouds = {
            'fast_cloud': {
                'url': 'http://localhost:8080/api/data',
                'cost': 0.10,
                'reliability': 0.95,
                'available': True
            },
            'slow_cloud': {
                'url': 'http://localhost:8081/api/data',
                'cost': 0.05,
                'reliability': 0.99,
                'available': True
            }
        }
    
    def select_cloud(self, data):
        priority = data.get('priority', 'normal')
        available_clouds = [c for c in self.clouds.values() if c['available']]
        
        if not available_clouds:
            return None
        
        if priority == 'high':
            return max(available_clouds, key=lambda x: x['reliability'])
        else:
            return min(available_clouds, key=lambda x: x['cost'])
    
    def route(self, data):
        selected_cloud = self.select_cloud(data)
        
        if not selected_cloud:
            print("❌ Aucun cloud disponible")
            return False
        
        try:
            # ENVOI RÉEL
            print(f"📤 Envoi à {selected_cloud['url']}...")
            
            response = requests.post(
                selected_cloud['url'],
                json={
                    'sensor_id': data['sensor_id'],
                    'data': data['data'],
                    'priority': data.get('priority', 'normal'),
                    'timestamp': datetime.now().isoformat()
                },
                timeout=3
            )
            
            if response.status_code == 200:
                print(f"✅ Envoyé à {selected_cloud['url']}")
                return True
            else:
                print(f"❌ HTTP {response.status_code}")
                return False
                
        except requests.exceptions.ConnectionError:
            print(f"🔌 Cloud inaccessible: {selected_cloud['url']}")
            selected_cloud['available'] = False
            return False
        except Exception as e:
            print(f"⚠️ Erreur: {e}")
            return False