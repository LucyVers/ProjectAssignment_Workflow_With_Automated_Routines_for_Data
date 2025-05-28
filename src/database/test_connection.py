from db import Db

def test_database_connection():
    try:
        # Försök skapa en anslutning
        db = Db()
        conn = db.get_conn()
        
        # Om vi kommer hit lyckades anslutningen
        print("✅ Databasanslutningen lyckades!")
        
        # Testa köra en enkel query
        cur = conn.cursor()
        cur.execute("SELECT version();")
        version = cur.fetchone()
        print(f"PostgreSQL version: {version[0]}")
        
        cur.close()
        
    except Exception as e:
        print("❌ Kunde inte ansluta till databasen")
        print(f"Fel: {str(e)}")

if __name__ == "__main__":
    test_database_connection() 