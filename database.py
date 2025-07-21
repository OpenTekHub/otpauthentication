import mysql.connector
from mysql.connector import Error
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

class DatabaseConnection:
    def __init__(self):
        self.host = os.getenv("DB_HOST", "localhost")
        self.database = os.getenv("DB_NAME", "harish")
        self.username = os.getenv("DB_USER", "root")
        self.password = os.getenv("DB_PASSWORD", "Varshini@123")
        self.port = os.getenv("DB_PORT", 3306)
        
    def create_connection(self):
        """Create a connection to MySQL database"""
        try:
            connection = mysql.connector.connect(
                host=self.host,
                database=self.database,
                user=self.username,
                password=self.password,
                port=self.port
            )
            
            if connection.is_connected():
                print("Successfully connected to MySQL database")
                return connection
                
        except Error as e:
            print(f"Error connecting to MySQL database: {e}")
            return None
    
    def close_connection(self, connection):
        """Close the database connection"""
        if connection and connection.is_connected():
            connection.close()
            print("MySQL connection closed")

# Global database instance
db = DatabaseConnection()

def get_db_connection():
    """Get database connection"""
    return db.create_connection()

def execute_query(query, params=None):
    """Execute a query and return results"""
    connection = get_db_connection()
    if connection:
        cursor = None
        try:
            cursor = connection.cursor(dictionary=True)
            cursor.execute(query, params)
            
            if query.strip().upper().startswith('SELECT') or query.strip().upper().startswith('SHOW') or query.strip().upper().startswith('DESCRIBE'):
                result = cursor.fetchall()
                # Consume any remaining results
                while cursor.nextset():
                    pass
            else:
                connection.commit()
                result = cursor.rowcount
            
            return result
        except Error as e:
            print(f"Error executing query: {e}")
            return None
        finally:
            if cursor:
                cursor.close()
            db.close_connection(connection)
    return None
