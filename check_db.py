from src.models.database_models import session_scope, Customer, Account, Transaction

def check_database():
    with session_scope() as session:
        customer_count = session.query(Customer).count()
        account_count = session.query(Account).count()
        transaction_count = session.query(Transaction).count()
        
        print(f"Antal kunder i databasen: {customer_count}")
        print(f"Antal konton i databasen: {account_count}")
        print(f"Antal transaktioner i databasen: {transaction_count}")
        
        if customer_count > 0:
            # Kolla några exempel på kunder
            print("\nExempel på kunder:")
            for customer in session.query(Customer).limit(3):
                print(f"- {customer.name}: {customer.phone}")

if __name__ == "__main__":
    check_database() 