"""initial schema

Revision ID: 0001
Revises: 
Create Date: 2026-03-18

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers
revision = '0001'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        'sellers',
        sa.Column('id', sa.String(), nullable=False),
        sa.Column('name', sa.String(), nullable=False),
        sa.Column('rating', sa.Float(), nullable=False),
        sa.PrimaryKeyConstraint('id')
    )

    op.create_table(
        'products',
        sa.Column('id', sa.String(), nullable=False),
        sa.Column('name', sa.String(), nullable=False),
        sa.Column('price_amount', sa.Float(), nullable=False),
        sa.Column('price_currency', sa.String(), nullable=False),
        sa.Column('stock', sa.Integer(), nullable=False),
        sa.Column('image_url', sa.String(), nullable=True),
        sa.Column('thumbnail_url', sa.String(), nullable=True),
        sa.Column('attributes', postgresql.JSONB(astext_type=sa.Text()), nullable=False, server_default='[]'),
        sa.PrimaryKeyConstraint('id')
    )

    op.create_table(
        'offers',
        sa.Column('id', sa.String(), nullable=False),
        sa.Column('product_id', sa.String(), nullable=False),
        sa.Column('seller_id', sa.String(), nullable=False),
        sa.Column('price_amount', sa.Float(), nullable=False),
        sa.Column('price_currency', sa.String(), nullable=False),
        sa.Column('delivery_date', sa.Date(), nullable=False),
        sa.ForeignKeyConstraint(['product_id'], ['products.id'], ondelete='CASCADE'),
        sa.ForeignKeyConstraint(['seller_id'], ['sellers.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id')
    )

    op.create_index('ix_offers_product_id', 'offers', ['product_id'])
    op.create_index('ix_offers_seller_id', 'offers', ['seller_id'])


def downgrade() -> None:
    op.drop_index('ix_offers_seller_id', table_name='offers')
    op.drop_index('ix_offers_product_id', table_name='offers')
    op.drop_table('offers')
    op.drop_table('products')
    op.drop_table('sellers')
