"""add page images table

Revision ID: 1f52b78d99b5
Revises: b2424975cff5
Create Date: 2022-11-25 17:07:54.940915

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = '1f52b78d99b5'
down_revision = 'b2424975cff5'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('page_images',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('image', mysql.LONGBLOB(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('page_images')
    # ### end Alembic commands ###
