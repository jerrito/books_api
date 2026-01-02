"""Create initial tables for users and books

Revision ID: c2d0598167cf
Revises: 
Create Date: 2025-12-14 19:21:24.018782

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
import sqlmodel
from sqlalchemy.dialects import postgresql


# revision identifiers, used by Alembic.
revision: str = 'c2d0598167cf'
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # Create users table
    op.create_table(
        'users',
        sa.Column('uuid', postgresql.UUID(), nullable=False),
        sa.Column('username', sa.String(), nullable=False),
        sa.Column('email', sa.String(), nullable=False),
        sa.Column('first_name', sa.String(), nullable=False),
        sa.Column('last_name', sa.String(), nullable=False),
        sa.Column('is_verified', sa.Boolean(), nullable=False, server_default='false'),
        sa.Column('created_at', postgresql.TIMESTAMP(), nullable=True),
        sa.Column('updated_at', postgresql.TIMESTAMP(), nullable=True),
        sa.PrimaryKeyConstraint('uuid')
    )
    
    # Create books table
    op.create_table(
        'books',
        sa.Column('uid', postgresql.UUID(), nullable=False),
        sa.Column('title', sa.String(), nullable=False),
        sa.Column('author', sa.String(), nullable=False),
        sa.Column('publisher', sa.String(), nullable=False),
        sa.Column('published_date', sa.Date(), nullable=False),
        sa.Column('language', sa.String(), nullable=False),
        sa.Column('pages', sa.Integer(), nullable=False),
        sa.Column('isbn', sa.String(), nullable=False),
        sa.Column('price', sa.Float(), nullable=False),
        sa.Column('available', sa.Boolean(), nullable=False),
        sa.Column('created_at', postgresql.TIMESTAMP(), nullable=True),
        sa.Column('updated_at', postgresql.TIMESTAMP(), nullable=True),
        sa.PrimaryKeyConstraint('uid')
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_table('books')
    op.drop_table('users') 
