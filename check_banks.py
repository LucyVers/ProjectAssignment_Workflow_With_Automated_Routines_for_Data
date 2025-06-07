from src.models.database_models import session_scope, Bank

def check_banks():
    with session_scope() as session:
        banks = session.query(Bank).all()
        if not banks:
            print("Inga banker hittades i databasen")
        else:
            print("\nBanker i databasen:")
            for bank in banks:
                print(f"ID: {bank.id}, Namn: {bank.name}, Banknummer: {bank.banknr}")

if __name__ == "__main__":
    check_banks() 