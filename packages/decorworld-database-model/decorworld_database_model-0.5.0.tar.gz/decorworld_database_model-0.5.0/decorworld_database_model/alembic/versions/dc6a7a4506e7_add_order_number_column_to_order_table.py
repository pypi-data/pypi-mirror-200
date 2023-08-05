"""add order number column to order table

Revision ID: dc6a7a4506e7
Revises: 68b8e7a46dc0
Create Date: 2022-11-21 18:24:22.320177

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'dc6a7a4506e7'
down_revision = '68b8e7a46dc0'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('orders', sa.Column('order_number', sa.String(length=25), nullable=False))
    op.create_unique_constraint(None, 'orders', ['order_number'])
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'orders', type_='unique')
    op.drop_column('orders', 'order_number')
    # ### end Alembic commands ###
