import requests
import time
import threading
from datetime import datetime

class AdaptiveRouter:
    def __init__(self):
        self.clouds = {
            'fast_cloud': {
                'url': 'http://localhost:8080/api/data',
                'cost': 0.10,
                'reliability': 0.95,
                'available': True,
                'name': 'Fast Cloud',
                'last_check': datetime.now()
            },
            'slow_cloud': {
                'url': 'http://localhost:8081/api/data',
                'cost': 0.05,
                'reliability': 0.99,
                'available': True,
                'name': 'Slow Cloud',
                'last_check': datetime.now()
            }
        }
        self.request_count = 0
        self.health_check_interval = 30  # Vérifier toutes les 30 secondes
        
        # Démarrer le thread de vérification santé
        self.health_check_thread = threading.Thread(target=self.health_check_loop, daemon=True)
        self.health_check_thread.start()
    
    def health_check_loop(self):
        """Vérifier périodiquement la santé de tous les clouds"""
        while True:
            time.sleep(self.health_check_interval)
            self.check_all_clouds()
    
    def check_all_clouds(self):
        """Vérifier tous les clouds (même ceux marqués indisponibles)"""
        print(f"\n🔄 Vérification santé des clouds ({datetime.now().strftime('%H:%M:%S')})")
        
        for name, cloud in self.clouds.items():
            try:
                # Essayer de contacter le endpoint de santé
                health_url = cloud['url'].replace('/api/data', '/stats')
                response = requests.get(health_url, timeout=2)
                
                was_available = cloud['available']
                cloud['available'] = (response.status_code == 200)
                cloud['last_check'] = datetime.now()
                
                if not was_available and cloud['available']:
                    print(f"✅ {cloud['name']} est de nouveau disponible!")
                elif was_available and not cloud['available']:
                    print(f"❌ {cloud['name']} est devenu indisponible")
                    
            except requests.exceptions.RequestException:
                was_available = cloud['available']
                cloud['available'] = False
                cloud['last_check'] = datetime.now()
                
                if was_available:
                    print(f"❌ {cloud['name']} est devenu indisponible")
    
    def select_cloud(self, data):
        """Sélectionner le cloud selon la priorité et la disponibilité"""
        priority = data.get('priority', 'normal')
        available_clouds = [c for c in self.clouds.values() if c['available']]
        
        if not available_clouds:
            print("⚠️ Aucun cloud disponible - données mises en cache")
            return None
        
        # MODIFICATION : Stratégie avec préférence pour Fast Cloud
        if priority == 'high':
            # Priorité haute → cloud le plus fiable
            return max(available_clouds, key=lambda x: x['reliability'])
        else:
            # Priorité normale → PRÉFÉRER Fast Cloud quand disponible
            fast_cloud = next((c for c in available_clouds if 'fast' in c['url'].lower()), None)
            
            if fast_cloud and self.request_count % 10 < 8:  # 80% vers Fast Cloud
                self.request_count += 1
                return fast_cloud
            else:
                # Utiliser un autre cloud
                self.request_count += 1
                return available_clouds[self.request_count % len(available_clouds)]
    
    def route(self, data):
        """Router les données vers le cloud sélectionné"""
        selected_cloud = self.select_cloud(data)
        
        if not selected_cloud:
            return False
        
        try:
            print(f"📤 Envoi à {selected_cloud['name']} ({selected_cloud['url']})...")
            
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
                print(f"✅ Envoyé à {selected_cloud['name']}")
                return True
            else:
                print(f"❌ HTTP {response.status_code} de {selected_cloud['name']}")
                # Marquer temporairement comme indisponible
                selected_cloud['available'] = False
                return False
                
        except requests.exceptions.ConnectionError:
            print(f"🔌 Cloud inaccessible: {selected_cloud['name']}")
            selected_cloud['available'] = False
            
            # RETRY avec un autre cloud
            print("🔄 Tentative avec un autre cloud...")
            fallback_cloud = self.select_cloud(data)  # Obtenir un autre cloud
            if fallback_cloud and fallback_cloud != selected_cloud:
                # Réessayer avec le fallback
                data['retry'] = True
                return self.route_with_fallback(data, fallback_cloud)
            return False
            
        except Exception as e:
            print(f"⚠️ Erreur: {e}")
            return False
    
    def route_with_fallback(self, data, fallback_cloud):
        """Route vers un cloud de secours spécifique"""
        try:
            print(f"🔄 Réessai avec {fallback_cloud['name']}...")
            response = requests.post(
                fallback_cloud['url'],
                json={
                    'sensor_id': data['sensor_id'],
                    'data': data['data'],
                    'priority': data.get('priority', 'normal'),
                    'retry': True,
                    'timestamp': datetime.now().isoformat()
                },
                timeout=3
            )
            
            if response.status_code == 200:
                print(f"✅ Envoyé à {fallback_cloud['name']} (fallback)")
                return True
            else:
                return False
        except:
            return False
    
    def get_status(self):
        """Obtenir le statut actuel de tous les clouds"""
        status = {}
        for name, cloud in self.clouds.items():
            status[name] = {
                'name': cloud['name'],
                'available': cloud['available'],
                'last_check': cloud['last_check'].strftime('%H:%M:%S') if cloud['last_check'] else 'Never',
                'url': cloud['url']
            }
        return status