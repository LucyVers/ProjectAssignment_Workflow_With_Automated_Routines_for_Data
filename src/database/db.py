import os
import psycopg2
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Singleton to reuse the same connection across instances
class Db:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(Db, cls).__new__(cls)
            cls._instance.conn = cls._create_conn()
        return cls._instance

    @staticmethod
    def _create_conn():
        return psycopg2.connect(
            dbname=os.getenv('DB_NAME', 'bank_db'),
            user=os.getenv('DB_USER', 'postgres'),
            password=os.getenv('DB_PASSWORD', 'postgres'),
            host=os.getenv('DB_HOST', 'localhost'),
            port=os.getenv('DB_PORT', '5432')
        )

    def get_conn(self):
        return self.conn
