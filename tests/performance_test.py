import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import time
import statistics
from datetime import datetime

class PerformanceTest:
    def __init__(self):
        self.results = {
            'preprocessing_times': [],
            'routing_times': [],
            'end_to_end_times': [],
            'throughput': 0
        }
    
    def test_preprocessing_latency(self, processor, data_batch):
        """Mesurer le temps de prétraitement"""
        start = time.time()
        processed = processor.process(data_batch)
        elapsed = (time.time() - start) * 1000
        
        self.results['preprocessing_times'].append(elapsed)
        print(f"⏱️  Prétraitement: {elapsed:.2f}ms pour {len(data_batch)} données")
        return processed
    
    def test_end_to_end_simulation(self, processor, router, num_tests=10):
        """Mesurer latence end-to-end"""
        print(f"\n🎯 Test End-to-End avec {num_tests} échantillons...")
        
        for i in range(num_tests):
            start = time.time()
            
            test_data = [{
                'sensor_id': f'test_sensor_{i}',
                'data': {'temperature': 25.0 + i, 'pressure': 1000.0 + i},
                'timestamp': datetime.now()
            }]
            
            processed = processor.process(test_data)
            if processed:
                time.sleep(0.001)
            
            elapsed = (time.time() - start) * 1000
            self.results['end_to_end_times'].append(elapsed)
        
        avg = statistics.mean(self.results['end_to_end_times'])
        print(f"✅ Moyenne end-to-end: {avg:.2f}ms")
    
    def test_throughput_simulation(self, processor, num_messages=100):
        """Mesurer throughput"""
        print(f"\n🚀 Test de throughput avec {num_messages} messages...")
        
        start = time.time()
        for i in range(num_messages):
            test_data = [{
                'sensor_id': f'test_sensor_{i % 3}',
                'data': {'value': i, 'timestamp': time.time()},
                'timestamp': datetime.now()
            }]
            processor.process(test_data)
        
        elapsed = time.time() - start
        if elapsed < 0.001:
            elapsed = 0.001
        
        throughput = num_messages / elapsed
        self.results['throughput'] = throughput
        print(f"📊 Throughput: {throughput:.2f} msg/s")
    
    def generate_report(self):
        """Générer rapport de performance"""
        print("\n" + "="*60)
        print("📊 RAPPORT DE PERFORMANCE - PASSERELLE INTELLIGENTE")
        print("="*60)
        
        if self.results['preprocessing_times']:
            print(f"\n⚡ Prétraitement des données:")
            print(f"  - Moyenne: {statistics.mean(self.results['preprocessing_times']):.2f}ms")
            print(f"  - Min: {min(self.results['preprocessing_times']):.2f}ms")
            print(f"  - Max: {max(self.results['preprocessing_times']):.2f}ms")
            if len(self.results['preprocessing_times']) >= 2:
                print(f"  - Écart-type: {statistics.stdev(self.results['preprocessing_times']):.2f}ms")
        
        if self.results['end_to_end_times']:
            print(f"\n🎯 Latence End-to-End:")
            print(f"  - Moyenne: {statistics.mean(self.results['end_to_end_times']):.2f}ms")
            print(f"  - Min: {min(self.results['end_to_end_times']):.2f}ms")
            print(f"  - Max: {max(self.results['end_to_end_times']):.2f}ms")
            print(f"  - Médiane: {statistics.median(self.results['end_to_end_times']):.2f}ms")
        
        if self.results['throughput']:
            print(f"\n📈 Débit (Throughput):")
            print(f"  - {self.results['throughput']:.2f} messages/seconde")
            print(f"  - {self.results['throughput'] * 60:.2f} messages/minute")
        
        print("\n" + "="*60)
        print("✅ Tests terminés avec succès")
        print("="*60)

if __name__ == "__main__":
    from gateway.data_processor import DataProcessor
    from gateway.adaptive_router import AdaptiveRouter
    
    print("="*60)
    print("🧪 TESTS DE PERFORMANCE - PASSERELLE INTELLIGENTE")
    print("="*60)
    print("\n⚠️  Note: Les tests utilisent des données simulées")
    print("   pour éviter de surcharger les clouds réels\n")
    
    time.sleep(1)
    
    processor = DataProcessor()
    router = AdaptiveRouter()
    tester = PerformanceTest()
    
    # Test 1
    print("\n📦 Test 1: Latence de prétraitement")
    print("-" * 60)
    test_data = [
        {'sensor_id': f'test_{i}', 'data': {'temp': 25 + i, 'pressure': 1000 + i}, 'timestamp': datetime.now()}
        for i in range(20)
    ]
    tester.test_preprocessing_latency(processor, test_data)
    
    # Test 2
    print("\n📦 Test 2: Latence End-to-End")
    print("-" * 60)
    tester.test_end_to_end_simulation(processor, router, num_tests=15)
    
    # Test 3
    print("\n📦 Test 3: Débit (Throughput)")
    print("-" * 60)
    tester.test_throughput_simulation(processor, num_messages=100)
    
    # Rapport
    tester.generate_report()
    
    print("\n💡 Pour tester avec de vraies données:")
    print("   1. Assurez-vous que les clouds sont démarrés")
    print("   2. Lancez la passerelle: python gateway/main.py")
    print("   3. Observez les logs en temps réel\n")