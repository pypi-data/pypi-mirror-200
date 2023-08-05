"""create invoice_data table

Revision ID: 824f9117cea4
Revises: d190af5edcec
Create Date: 2022-11-17 16:39:46.853161

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '824f9117cea4'
down_revision = 'd190af5edcec'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('invoice_data',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=30), nullable=False),
    sa.Column('zip_code', sa.String(length=4), nullable=False),
    sa.Column('city', sa.String(length=25), nullable=False),
    sa.Column('address', sa.String(length=25), nullable=False),
    sa.Column('tax_number', sa.String(length=25), nullable=True),
    sa.Column('description', sa.String(length=50), nullable=True),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('invoice_data')
    # ### end Alembic commands ###
