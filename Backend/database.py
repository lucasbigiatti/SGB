# database.py
import mysql.connector
from mysql.connector import pooling
import logging

class DatabaseManager:
    _instance = None
    _connection_pool = None
    
    @classmethod
    def get_instance(cls):
        if cls._instance is None:
            cls._instance = DatabaseManager()
            cls._initialize_pool()
        return cls._instance
    
    @classmethod
    def _initialize_pool(cls):
        try:
            cls._connection_pool = pooling.MySQLConnectionPool(
                pool_name="bebidas_pool",
                pool_size=5,
                host="127.0.0.1",
                user="root",
                password="",
                database="gestionbebidas"
            )
            logging.info("Pool de conexiones iniciado correctamente")
        except mysql.connector.Error as e:
            logging.error(f"Error al inicializar el pool de conexiones: {e}")
            cls._connection_pool = None
    
    def get_connection(self):
        if self._connection_pool:
            try:
                return self._connection_pool.get_connection()
            except mysql.connector.Error as e:
                logging.error(f"Error al obtener conexión del pool: {e}")
        return None
        
    def execute_query(self, query, params=None, fetch=True):
        """Ejecuta una consulta y devuelve los resultados"""
        connection = None
        cursor = None
        try:
            connection = self.get_connection()
            if not connection:
                return None
                
            cursor = connection.cursor()
            cursor.execute(query, params or ())
            
            if fetch:
                result = cursor.fetchall()
                return result
            else:
                connection.commit()
                return cursor.lastrowid
        except mysql.connector.Error as e:
            if connection:
                connection.rollback()
            logging.error(f"Error en consulta: {e}")
            return None
        finally:
            if cursor:
                cursor.close()
            if connection:
                connection.close()

# Función para compatibilidad con código existente
def conectar_db():
    return DatabaseManager.get_instance().get_connection()