from models.database_models import session_scope, engine
from sqlalchemy import inspect, text

def check_database_tables():
    """Kontrollerar vilka tabeller som finns i databasen och deras struktur"""
    inspector = inspect(engine)
    
    # Lista alla tabeller
    tables = inspector.get_table_names()
    print("\nTabeller i databasen:")
    print("=" * 50)
    
    with engine.connect() as connection:
        for table in tables:
            print(f"\nTabell: {table}")
            print("-" * 30)
            
            # Visa antal rader
            result = connection.execute(text(f"SELECT COUNT(*) FROM {table}"))
            count = result.scalar()
            print(f"Antal rader: {count}")
            
            if count > 0:
                # Visa exempel på data
                result = connection.execute(text(f"SELECT * FROM {table} LIMIT 3"))
                rows = result.fetchall()
                print("\nExempel på data:")
                for row in rows:
                    print(row)
            
            # Visa kolumner för varje tabell
            columns = inspector.get_columns(table)
            print("\nKolumner:")
            for col in columns:
                print(f"  - {col['name']}: {col['type']}")
                
            # Visa foreign keys
            fks = inspector.get_foreign_keys(table)
            if fks:
                print("\nForeign Keys:")
                for fk in fks:
                    print(f"  - {fk['constrained_columns']} -> {fk['referred_table']}.{fk['referred_columns']}")
            
            # Visa constraints
            constraints = inspector.get_check_constraints(table)
            if constraints:
                print("\nCheck Constraints:")
                for const in constraints:
                    print(f"  - {const['name']}: {const['sqltext']}")

if __name__ == "__main__":
    check_database_tables() 