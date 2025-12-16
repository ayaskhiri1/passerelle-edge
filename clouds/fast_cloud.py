from flask import Flask, request, jsonify

app = Flask(__name__)
received_data = []

@app.route('/api/data', methods=['POST'])
def receive_data():
    try:
        data = request.json
        
        # Gérer différents formats
        if 'sensor_id' in data:
            sensor_id = data['sensor_id']
        elif 'test' in data:  # Pour les tests manuels
            sensor_id = "test_manual"
        else:
            sensor_id = "unknown"
        
        print(f"✅ Fast Cloud a reçu: {sensor_id} - {data}")
        received_data.append(data)
        
        return jsonify({
            "status": "received", 
            "cloud": "fast",
            "sensor_id": sensor_id
        }), 200
        
    except Exception as e:
        print(f"❌ Erreur Fast Cloud: {e}")
        return jsonify({"error": str(e)}), 500

@app.route('/stats', methods=['GET'])
def get_stats():
    return jsonify({
        "total_received": len(received_data),
        "last_received": received_data[-1] if received_data else None
    })

if __name__ == '__main__':
    print("🌥️ Fast Cloud démarré sur http://localhost:8080")
    app.run(host='0.0.0.0', port=8080, debug=False)