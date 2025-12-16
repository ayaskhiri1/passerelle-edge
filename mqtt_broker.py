import paho.mqtt.client as mqtt

def on_connect(client, userdata, flags, rc):
    print(f"Broker MQTT prêt. Code: {rc}")

def on_message(client, userdata, msg):
    print(f"Message reçu: {msg.topic} -> {msg.payload.decode()}")

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

client.connect("localhost", 1883, 60)
print("Broker MQTT démarré sur localhost:1883")
client.loop_forever()