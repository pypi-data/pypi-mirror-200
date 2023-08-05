"""create address table

Revision ID: a2a05856eb15
Revises: 72c749f78b2c
Create Date: 2022-11-17 15:11:09.260426

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'a2a05856eb15'
down_revision = '72c749f78b2c'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('addresses',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('zip_code', sa.String(length=4), nullable=False),
    sa.Column('city', sa.String(length=25), nullable=False),
    sa.Column('address', sa.String(length=25), nullable=False),
    sa.Column('description', sa.String(length=50), nullable=True),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('addresses')
    # ### end Alembic commands ###
