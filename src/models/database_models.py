from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Numeric, CheckConstraint, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker, scoped_session
from sqlalchemy.pool import QueuePool
from sqlalchemy.exc import SQLAlchemyError, OperationalError
from contextlib import contextmanager
import os
from dotenv import load_dotenv
import logging
from typing import Generator
import time
from functools import wraps

# Konfigurera logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Ladda miljövariabler
load_dotenv()

# Databasanslutningskonfiguration
DB_CONFIG = {
    'host': os.getenv('DB_HOST', 'localhost'),
    'port': os.getenv('DB_PORT', '5432'),
    'database': os.getenv('DB_NAME', 'bank_db'),
    'user': os.getenv('DB_USER', 'postgres'),
    'password': os.getenv('DB_PASSWORD', '')
}

# Skapa connection URL
DATABASE_URL = f"postgresql://{DB_CONFIG['user']}:{DB_CONFIG['password']}@{DB_CONFIG['host']}:{DB_CONFIG['port']}/{DB_CONFIG['database']}"

# Retry decorator för databasoperationer
def retry_on_error(max_retries: int = 3, delay: float = 1.0):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            retries = 0
            while retries < max_retries:
                try:
                    return func(*args, **kwargs)
                except SQLAlchemyError as e:
                    retries += 1
                    if retries == max_retries:
                        logger.error(f"Max retries ({max_retries}) reached. Error: {str(e)}")
                        raise
                    logger.warning(f"Database operation failed. Retrying ({retries}/{max_retries})...")
                    time.sleep(delay * retries)
            return None
        return wrapper
    return decorator

# Skapa engine med connection pooling
engine = create_engine(
    DATABASE_URL,
    poolclass=QueuePool,
    pool_size=5,
    max_overflow=10,
    pool_timeout=30,
    pool_recycle=1800,  # Recycle connections after 30 minutes
    echo=bool(os.getenv('SQL_ECHO', 'False'))
)

# Skapa session factory
SessionFactory = sessionmaker(bind=engine)
ScopedSession = scoped_session(SessionFactory)

# Context manager för sessionshantering
@contextmanager
def session_scope() -> Generator:
    """Provide a transactional scope around a series of operations."""
    session = ScopedSession()
    try:
        yield session
        session.commit()
    except SQLAlchemyError as e:
        logger.error(f"Database error occurred: {str(e)}")
        session.rollback()
        raise
    finally:
        session.close()

Base = declarative_base()

class Bank(Base):
    __tablename__ = 'banks'
    
    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    banknr = Column(String(10), unique=True, nullable=False)  # Unikt banknummer
    
    # Relationships
    customers = relationship("Customer", back_populates="bank")
    accounts = relationship("Account", back_populates="bank")

class Customer(Base):
    __tablename__ = 'customers'
    
    id = Column(Integer, primary_key=True)
    bank_id = Column(Integer, ForeignKey('banks.id'), nullable=False)  # Kunden måste tillhöra en bank
    personnummer = Column(String(11), unique=True, nullable=False)  # Format: YYMMDD-XXXX
    name = Column(String(100), nullable=False)
    phone = Column(String(20))
    address = Column(String(100))
    city = Column(String(50))
    postal_code = Column(String(5))
    guardian_info = Column(String(100))  # För minderåriga kunder
    
    # Constraints för datakvalitet
    __table_args__ = (
        CheckConstraint(r"personnummer ~ '^\d{6}-\d{4}$'", name='valid_personnummer_format'),
        CheckConstraint(r"postal_code ~ '^\d{5}$'", name='valid_postal_code_format'),
        CheckConstraint(r"phone ~ '^\+46\s*\(\d{1,4}\)\s*\d{3}\s*\d{2}\s*\d{2}$'", name='valid_phone_format'),
    )
    
    # Relationships
    bank = relationship("Bank", back_populates="customers")
    accounts = relationship("Account", back_populates="customer")

class Account(Base):
    __tablename__ = 'accounts'
    
    id = Column(Integer, primary_key=True)
    bank_id = Column(Integer, ForeignKey('banks.id'), nullable=False)  # Kontot måste tillhöra en bank
    account_number = Column(String(24), unique=True, nullable=False)  # Format: SE8902XXXX[14 digits]
    customer_id = Column(Integer, ForeignKey('customers.id'), nullable=False)
    type = Column(String(20), nullable=False)  # savings, checking, etc.
    created_at = Column(DateTime, nullable=False)
    
    # Constraints
    __table_args__ = (
        CheckConstraint(r"account_number ~ '^SE8902[A-Z]{4}\d{14}$'", name='valid_account_number_format'),
    )
    
    # Relationships
    bank = relationship("Bank", back_populates="accounts")
    customer = relationship("Customer", back_populates="accounts")
    transactions = relationship("Transaction", back_populates="account")

class Transaction(Base):
    __tablename__ = 'transactions'
    
    id = Column(Integer, primary_key=True)
    transaction_id = Column(String(36), unique=True, nullable=False)  # UUID format
    account_id = Column(Integer, ForeignKey('accounts.id'), nullable=False)
    amount = Column(Numeric(10, 2), nullable=False)
    currency = Column(String(3), nullable=False)
    timestamp = Column(DateTime, nullable=False)
    sender_country = Column(String(50))
    sender_municipality = Column(String(50))
    receiver_country = Column(String(50))
    receiver_municipality = Column(String(50))
    transaction_type = Column(String(20), nullable=False)  # incoming/outgoing
    notes = Column(String(200))
    
    # Relationships
    account = relationship("Account", back_populates="transactions") 