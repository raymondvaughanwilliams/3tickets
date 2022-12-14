"""empty message

Revision ID: b4d52573338e
Revises: 77b5b5891ebc
Create Date: 2022-12-07 09:10:39.832491

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'b4d52573338e'
down_revision = '77b5b5891ebc'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('event', schema=None) as batch_op:
        batch_op.add_column(sa.Column('number', sa.String(length=20), nullable=True))
        batch_op.add_column(sa.Column('email', sa.String(length=100), nullable=True))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('event', schema=None) as batch_op:
        batch_op.drop_column('email')
        batch_op.drop_column('number')

    # ### end Alembic commands ###
