import time
import json
import random
import socket

def simulate_can_bus():
    """
    Simuler un capteur CAN Bus (Controller Area Network)
    Typiquement utilisé dans l'automobile et l'industrie
    """
    print("🚗 Capteur CAN Bus démarré (simulation)...")
    print("Port: 5022 (TCP)")
    
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    
    try:
        server.bind(('0.0.0.0', 5022))
        server.listen(5)
        server.settimeout(30.0)
        
        print("✅ CAN Bus prêt sur port 5022")
        
        while True:
            try:
                client, addr = server.accept()
                
                # Simuler des données typiques CAN Bus
                # (vitesse moteur, température moteur, niveau carburant)
                data = {
                    "sensor_id": "can_sensor_1",
                    "can_id": hex(random.randint(0x100, 0x7FF)),  # CAN ID standard
                    "engine_rpm": random.randint(800, 6000),       # Tours/minute
                    "engine_temp": random.uniform(80.0, 105.0),    # Température °C
                    "fuel_level": random.uniform(10.0, 100.0),     # Niveau %
                    "vehicle_speed": random.uniform(0.0, 120.0),   # Vitesse km/h
                    "timestamp": time.time(),
                    "type": "critical" if random.uniform(80.0, 105.0) > 100 else "normal"
                }
                
                # Envoyer les données
                client.send(json.dumps(data).encode())
                client.close()
                
                print(f"📡 CAN → {addr}: RPM={data['engine_rpm']}, Temp={data['engine_temp']:.1f}°C")
                
                time.sleep(7)  # Collecte toutes les 7 secondes
                
            except socket.timeout:
                continue
            except Exception as e:
                print(f"⚠️ Erreur CAN (non fatale): {e}")
                time.sleep(2)
                
    except Exception as e:
        print(f"❌ Erreur fatale CAN: {e}")
    finally:
        server.close()

if __name__ == "__main__":
    simulate_can_bus()