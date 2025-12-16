from flask import Flask, render_template, jsonify
import random
from datetime import datetime

app = Flask(__name__)

# Données simulées pour la démo
simulated_data = []

def generate_simulated_stats():
    """Générer des statistiques simulées"""
    global simulated_data
    
    # Ajouter une donnée simulée toutes les 30 secondes
    if len(simulated_data) < 10 or random.random() > 0.7:
        sensor_types = ['http_sensor_1', 'modbus_sensor_1', 'mqtt_sensor']
        sensor_id = random.choice(sensor_types)
        
        simulated_data.append({
            'sensor_id': sensor_id,
            'data': {
                'temperature': random.uniform(20, 30),
                'pressure': random.uniform(1000, 1020),
                'voltage': random.uniform(220, 240),
                'type': random.choice(['normal', 'critical'])
            },
            'timestamp': datetime.now().isoformat()
        })
    
    # Garder max 20 entrées
    if len(simulated_data) > 20:
        simulated_data = simulated_data[-20:]
    
    total = len(simulated_data)
    routed = int(total * 0.85)  # 85% de succès
    
    return {
        'total_cached': 0,  # Pas de cache dans notre version simplifiée
        'total_routed': routed,
        'unique_sensors': len(set([d['sensor_id'] for d in simulated_data])),
        'cache_hit_rate': 0,
        'recent_data': simulated_data[-10:]  # 10 dernières
    }

@app.route('/')
def index():
    return render_template('dashboard.html')

@app.route('/api/stats')
def api_stats():
    return jsonify(generate_simulated_stats())

@app.route('/api/clear_cache')
def clear_cache():
    global simulated_data
    simulated_data = []
    return jsonify({"status": "données réinitialisées"})

if __name__ == '__main__':
    print("📊 Dashboard démarré sur http://localhost:5000")
    print("⚠️  Mode SIMULATION (SQLite désactivé)")
    app.run(host='0.0.0.0', port=5000, debug=True)