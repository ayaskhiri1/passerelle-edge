import time
import json
import random
import socket

print("Modbus Sensor démarré...")

def send_modbus_data():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server.bind(('0.0.0.0', 5021))
    server.listen(5)
    server.settimeout(30.0)  # Timeout pour éviter le blocage
    
    print("Modbus prêt sur port 5021")
    
    while True:
        try:
            client, addr = server.accept()
            
            # Générer données
            data = {
                "sensor_id": "modbus_sensor_1",
                "voltage": random.uniform(220.0, 240.0),
                "current": random.uniform(1.0, 5.0),
                "timestamp": time.time(),
                "type": "normal"
            }
            
            # Envoyer
            client.send(json.dumps(data).encode())
            client.close()
            
            print(f"Modbus → {addr}: {data}")
            time.sleep(8)  # Attente entre envois
            
        except socket.timeout:
            continue  # Juste réessayer
        except Exception as e:
            print(f"Erreur Modbus (non fatale): {e}")
            time.sleep(2)

if __name__ == "__main__":
    send_modbus_data()