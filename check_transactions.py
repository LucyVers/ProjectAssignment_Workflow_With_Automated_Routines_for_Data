from src.models.database_models import Transaction, session_scope

def check_transactions():
    with session_scope() as session:
        transactions = session.query(Transaction).all()
        print(f'Antal transaktioner: {len(transactions)}')
        
        if transactions:
            print('\nExempel på transaktioner:')
            for t in transactions[:5]:
                print(f'- {t.transaction_id}: {t.amount} {t.currency} ({t.transaction_type})')
        else:
            print('\nInga transaktioner hittades.')

if __name__ == '__main__':
    check_transactions() 