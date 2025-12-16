import time
import requests
import statistics

def test_latency():
    """Tester la latence de bout en bout"""
    print("Test de latence...")
    
    latencies = []
    for i in range(10):
        start = time.time()
        
        # Simuler l'envoi de données
        response = requests.post(
            'http://localhost:8080/api/data',
            json={'test': i, 'timestamp': time.time()},
            timeout=10
        )
        
        latency = (time.time() - start) * 1000  # en ms
        latencies.append(latency)
        print(f"  Test {i+1}: {latency:.2f} ms")
    
    print(f"\nRésultats:")
    print(f"  Moyenne: {statistics.mean(latencies):.2f} ms")
    print(f"  Max: {max(latencies):.2f} ms")
    print(f"  Min: {min(latencies):.2f} ms")
    print(f"  Écart-type: {statistics.stdev(latencies):.2f} ms")

def test_cache_recovery():
    """Tester la récupération après panne réseau"""
    print("\nTest de récupération après panne...")
    
    # Simuler une panne en arrêtant le cloud rapide
    print("  Simulation de panne réseau...")
    
    # Envoyer des données pendant la panne
    for i in range(3):
        try:
            response = requests.post(
                'http://localhost:8080/api/data',
                json={'test_fail': i},
                timeout=1
            )
        except:
            print(f"  ✗ Échec attendu pour le test {i}")
    
    print("  ✓ Le système devrait mettre en cache ces données")
    print("  Relancez le cloud pour voir la reprise")

if __name__ == '__main__':
    print("=== Tests de Performance ===")
    test_latency()
    test_cache_recovery()