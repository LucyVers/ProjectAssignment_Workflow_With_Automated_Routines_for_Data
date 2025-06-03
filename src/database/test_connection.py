from src.models.database_models import session_scope, Bank, engine, retry_on_error
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy import text
import time
import logging

# Konfigurera logging för tester
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def test_database_connection():
    """Test basic database connectivity and version"""
    try:
        with session_scope() as session:
            # Testa databasversion med SQLAlchemy
            result = session.execute(text("SELECT version();"))
            version = result.scalar()
            logger.info("✅ Databasanslutningen lyckades!")
            logger.info(f"PostgreSQL version: {version}")
            return True
            
    except SQLAlchemyError as e:
        logger.error("❌ Kunde inte ansluta till databasen")
        logger.error(f"Fel: {str(e)}")
        return False

def test_connection_pooling():
    """Test that connection pooling works correctly"""
    try:
        logger.info("Testar connection pooling...")
        
        # Test 1: Verifiera att poolen skapas
        if not hasattr(engine, 'pool'):
            raise SQLAlchemyError("Connection pool saknas")
        
        # Test 2: Kontrollera pool-storlek
        logger.info(f"Pool size: {engine.pool.size()}")
        logger.info(f"Checkedout connections: {engine.pool.checkedout()}")
        
        # Test 3: Testa flera samtidiga anslutningar
        sessions = []
        try:
            for i in range(3):
                with session_scope() as session:
                    # Gör en enkel query i varje session
                    session.execute(text("SELECT 1"))
                    sessions.append(session)
                    logger.info(f"Session {i+1} skapad och testad")
            
            logger.info("✅ Connection pooling fungerar korrekt!")
            return True
            
        finally:
            sessions.clear()
            
    except SQLAlchemyError as e:
        logger.error("❌ Problem med connection pooling")
        logger.error(f"Fel: {str(e)}")
        return False

@retry_on_error(max_retries=3, delay=0.1)  # Kortare delay för testet
def test_retry_mechanism():
    """Test that retry mechanism works"""
    logger.info("Testar retry-mekanismen...")
    
    # Reset attempts counter for each test run
    test_retry_mechanism.attempts = getattr(test_retry_mechanism, 'attempts', 0)
    test_retry_mechanism.attempts += 1
    
    # Simulera fel på första och andra försöket
    if test_retry_mechanism.attempts <= 2:
        logger.info(f"Simulerar fel (försök {test_retry_mechanism.attempts}/3)")
        raise SQLAlchemyError("Simulerat tillfälligt fel")
    
    # Tredje försöket lyckas
    logger.info("✅ Retry-mekanismen fungerar som förväntat!")
    logger.info(f"Lyckades efter {test_retry_mechanism.attempts} försök")
    return True

def test_transaction_management():
    """Test transaction management and rollback"""
    try:
        logger.info("Testar transaktionshantering...")
        
        with session_scope() as session:
            # Skapa en testbank
            test_bank = Bank(name="TestBank", banknr="TEST12345")
            session.add(test_bank)
            
            # Simulera ett fel för att testa rollback
            raise SQLAlchemyError("Simulerat fel för rollback-test")
            
    except SQLAlchemyError:
        # Verifiera att banken inte finns i databasen (rollback lyckades)
        with session_scope() as verify_session:
            bank = verify_session.query(Bank).filter_by(banknr="TEST12345").first()
            if bank is None:
                logger.info("✅ Transaktionshantering och rollback fungerar!")
                return True
            else:
                logger.error("❌ Rollback misslyckades")
                return False

def run_all_tests():
    """Kör alla tester i sekvens"""
    logger.info("=== Startar omfattande databastester ===")
    
    tests = [
        ("Grundläggande anslutningstest", test_database_connection),
        ("Connection pooling test", test_connection_pooling),
        ("Retry-mekanism test", test_retry_mechanism),
        ("Transaktionshantering test", test_transaction_management)
    ]
    
    results = []
    for test_name, test_func in tests:
        logger.info(f"\nKör test: {test_name}")
        try:
            # För retry-mekanismen, tillåt att den hanterar sina egna fel
            if test_name == "Retry-mekanism test":
                result = test_func()  # Låt retry-dekoratorn hantera felen
            else:
                result = test_func()
            results.append((test_name, result))
        except Exception as e:
            logger.error(f"Test {test_name} kraschade: {str(e)}")
            results.append((test_name, False))
    
    # Visa testresultat
    logger.info("\n=== Testresultat ===")
    for test_name, result in results:
        status = "✅ Lyckades" if result else "❌ Misslyckades"
        logger.info(f"{test_name}: {status}")

if __name__ == "__main__":
    run_all_tests() 