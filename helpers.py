from db import MysqlConnector
import os 
db_config = {
    "host": "localhost",
    "user": "root",
    "password": "Dimawydad@1937",
    "database": "geeksDB",
}

db_config_env = {
    "host": os.getenv("DB_URL"),
    "user": os.getenv("DB_USERNAME"),
    "password": os.getenv("DB_PASSWORD"),
    "database": os.getenv("DB_NAME"),
}

def init_db():
    """Create table if it doesn't exist"""
    conn =MysqlConnector(**db_config).connection()
    cursor = conn.cursor()
    create_table_query = """
    CREATE TABLE IF NOT EXISTS blog (
        id INT AUTO_INCREMENT PRIMARY KEY,
        title TEXT,
        content TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
    );
    """
    cursor.execute(create_table_query)
    conn.commit()
    print("table created")
    cursor.close()
    conn.close()
