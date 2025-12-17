import sqlite3
import json
from datetime import datetime

class CacheManager:
    def __init__(self, db_path='gateway_cache.db'):
        self.conn = sqlite3.connect(db_path, check_same_thread=False)
        self.create_table()
    
    def create_table(self):
        """Créer la table de cache"""
        self.conn.execute('''
            CREATE TABLE IF NOT EXISTS cached_data (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                sensor_id TEXT,
                data TEXT,
                priority TEXT,
                timestamp TEXT,
                synced INTEGER DEFAULT 0
            )
        ''')
        self.conn.commit()
    
    def add(self, sensor_id, data, priority='normal'):
        """Ajouter une donnée au cache"""
        self.conn.execute('''
            INSERT INTO cached_data (sensor_id, data, priority, timestamp)
            VALUES (?, ?, ?, ?)
        ''', (sensor_id, json.dumps(data), priority, datetime.now().isoformat()))
        self.conn.commit()
        print(f"💾 Donnée mise en cache: {sensor_id}")
    
    def get_unsynced(self, limit=10):
        """Récupérer les données non synchronisées"""
        cursor = self.conn.execute('''
            SELECT id, sensor_id, data, priority, timestamp 
            FROM cached_data 
            WHERE synced = 0 
            ORDER BY priority DESC, timestamp ASC
            LIMIT ?
        ''', (limit,))
        
        rows = cursor.fetchall()
        return [{
            'id': row[0],
            'sensor_id': row[1],
            'data': json.loads(row[2]),
            'priority': row[3],
            'timestamp': row[4]
        } for row in rows]
    
    def mark_synced(self, cache_id):
        """Marquer une donnée comme synchronisée"""
        self.conn.execute('UPDATE cached_data SET synced = 1 WHERE id = ?', (cache_id,))
        self.conn.commit()
        print(f"✅ Donnée synchronisée (ID: {cache_id})")
    
    def count_cached(self):
        """Compter les données en cache"""
        cursor = self.conn.execute('SELECT COUNT(*) FROM cached_data WHERE synced = 0')
        return cursor.fetchone()[0]
    
    def clear_synced(self):
        """Supprimer les données synchronisées anciennes"""
        self.conn.execute('DELETE FROM cached_data WHERE synced = 1')
        self.conn.commit()