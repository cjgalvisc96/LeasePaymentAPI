"""Initial_db

Revision ID: 092aaa20aee6
Revises: 
Create Date: 2021-05-20 12:56:41.257911

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '092aaa20aee6'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('payment',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('lessee_id', sa.Integer(), nullable=True),
    sa.Column('property_code', sa.String(length=20), nullable=True),
    sa.Column('paid_value', sa.Integer(), nullable=True),
    sa.Column('payment_date', sa.Date(), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('lessee_id'),
    sa.UniqueConstraint('property_code')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('payment')
    # ### end Alembic commands ###
