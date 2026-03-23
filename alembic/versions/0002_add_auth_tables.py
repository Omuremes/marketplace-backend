"""add auth tables

Revision ID: 0002
Revises: 0001
Create Date: 2026-03-23

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '0002'
down_revision = '0001'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # Create admins table
    op.create_table(
        'admins',
        sa.Column('id', sa.String(), nullable=False),
        sa.Column('email', sa.Text(), nullable=False),
        sa.Column('password_hash', sa.Text(), nullable=False),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_admins_email'), 'admins', ['email'], unique=True)
    
    # Add columns to sellers natively
    op.add_column('sellers', sa.Column('email', sa.Text(), nullable=True))
    op.add_column('sellers', sa.Column('password_hash', sa.Text(), nullable=True))
    
    # Fill in a dummy hash/email for existing sellers to make them non-nullable
    op.execute("UPDATE sellers SET email = 'temp_' || id || '@seller.com' WHERE email IS NULL")
    op.execute("UPDATE sellers SET password_hash = 'temp_hash' WHERE password_hash IS NULL")
    
    op.alter_column('sellers', 'email', existing_type=sa.Text(), nullable=False)
    op.alter_column('sellers', 'password_hash', existing_type=sa.Text(), nullable=False)
    
    op.create_index(op.f('ix_sellers_email'), 'sellers', ['email'], unique=True)


def downgrade() -> None:
    op.drop_index(op.f('ix_sellers_email'), table_name='sellers')
    op.drop_column('sellers', 'password_hash')
    op.drop_column('sellers', 'email')
    
    op.drop_index(op.f('ix_admins_email'), table_name='admins')
    op.drop_table('admins')
