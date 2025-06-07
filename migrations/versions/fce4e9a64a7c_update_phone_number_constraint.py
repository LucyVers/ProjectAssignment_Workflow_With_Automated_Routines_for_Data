"""update phone number constraint

Revision ID: fce4e9a64a7c
Revises: aa1c006394e2
Create Date: 2025-06-07 11:23:45.123456

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'fce4e9a64a7c'
down_revision: Union[str, None] = 'aa1c006394e2'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # Drop the old constraint
    op.drop_constraint('valid_phone_format', 'customers', type_='check')
    
    # Add new constraint that accepts international numbers
    op.create_check_constraint(
        'valid_phone_format',
        'customers',
        "phone ~ '^\\+\\d{1,3}\\s*\\(\\d{1,4}\\)\\s*\\d{1,}$'"
    )


def downgrade() -> None:
    """Downgrade schema."""
    # Drop the new constraint
    op.drop_constraint('valid_phone_format', 'customers', type_='check')
    
    # Restore the old constraint (Swedish numbers only)
    op.create_check_constraint(
        'valid_phone_format',
        'customers',
        "phone ~ '^\\+46\\s*\\(\\d{1,4}\\)\\s*\\d{3}\\s*\\d{2}\\s*\\d{2}$'"
    )
