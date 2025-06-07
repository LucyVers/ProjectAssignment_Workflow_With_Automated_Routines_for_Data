"""update transaction constraints

Revision ID: fd400d2b9aae
Revises: fce4e9a64a7c
Create Date: 2025-06-07 12:34:56.789012

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'fd400d2b9aae'
down_revision: Union[str, None] = 'fce4e9a64a7c'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # Drop the existing unique constraint on transaction_id
    op.drop_constraint('transactions_transaction_id_key', 'transactions', type_='unique')
    
    # Add compound unique constraint on transaction_id and transaction_type
    op.create_unique_constraint(
        'transactions_transaction_id_type_key',
        'transactions',
        ['transaction_id', 'transaction_type']
    )


def downgrade() -> None:
    """Downgrade schema."""
    # Drop the compound unique constraint
    op.drop_constraint('transactions_transaction_id_type_key', 'transactions', type_='unique')
    
    # Restore the original unique constraint on transaction_id
    op.create_unique_constraint(
        'transactions_transaction_id_key',
        'transactions',
        ['transaction_id']
    )
