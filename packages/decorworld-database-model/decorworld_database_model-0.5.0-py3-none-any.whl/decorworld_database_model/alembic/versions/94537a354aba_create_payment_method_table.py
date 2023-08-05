"""create payment_method table

Revision ID: 94537a354aba
Revises: 57c6c9633e32
Create Date: 2022-11-17 18:19:57.038988

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '94537a354aba'
down_revision = '57c6c9633e32'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('payment_methods',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('name', sa.String(length=30), nullable=False),
    sa.Column('price', sa.Integer(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('payment_methods')
    # ### end Alembic commands ###
