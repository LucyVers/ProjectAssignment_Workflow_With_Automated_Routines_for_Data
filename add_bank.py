from src.models.database_models import session_scope, Bank

def add_bank():
    with session_scope() as session:
        bank = Bank(name='Huvudbanken', banknr='SE8902')
        session.add(bank)
        session.commit()
        print("Bank added successfully!")

if __name__ == "__main__":
    add_bank() 