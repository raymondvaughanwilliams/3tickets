"""empty message

Revision ID: 9cbacc6f013d
Revises: a37bea8a2133
Create Date: 2022-12-10 22:24:31.511102

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import sqlite

# revision identifiers, used by Alembic.
revision = '9cbacc6f013d'
down_revision = 'a37bea8a2133'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('events',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=100), nullable=True),
    sa.Column('date', sa.Date(), nullable=True),
    sa.Column('time', sa.Time(), nullable=True),
    sa.Column('location', sa.String(length=100), nullable=True),
    sa.Column('description', sa.Text(), nullable=True),
    sa.Column('days', sa.Integer(), nullable=True),
    sa.Column('image1', sa.String(length=100), nullable=True),
    sa.Column('image2', sa.String(length=100), nullable=True),
    sa.Column('image3', sa.String(length=100), nullable=True),
    sa.Column('status', sa.String(length=20), nullable=True),
    sa.Column('number', sa.String(length=20), nullable=True),
    sa.Column('email', sa.String(length=100), nullable=True),
    sa.Column('views', sa.Integer(), nullable=True),
    sa.Column('tags', sa.JSON(), nullable=True),
    sa.Column('eventtags', sa.String(length=200), nullable=True),
    sa.Column('baseprice', sa.Integer(), nullable=True),
    sa.PrimaryKeyConstraint('id', name=op.f('pk_events'))
    )
    op.drop_table('event')
    with op.batch_alter_table('articles', schema=None) as batch_op:
        batch_op.drop_constraint('fk_articles_event_id_event', type_='foreignkey')
        batch_op.create_foreign_key(batch_op.f('fk_articles_event_id_events'), 'events', ['event_id'], ['id'])

    with op.batch_alter_table('items', schema=None) as batch_op:
        batch_op.create_foreign_key(batch_op.f('fk_items_event_id_events'), 'events', ['event_id'], ['id'])

    with op.batch_alter_table('tickets', schema=None) as batch_op:
        batch_op.drop_constraint('fk_tickets_event_id_event', type_='foreignkey')
        batch_op.create_foreign_key(batch_op.f('fk_tickets_event_id_events'), 'events', ['event_id'], ['id'])

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('tickets', schema=None) as batch_op:
        batch_op.drop_constraint(batch_op.f('fk_tickets_event_id_events'), type_='foreignkey')
        batch_op.create_foreign_key('fk_tickets_event_id_event', 'event', ['event_id'], ['id'])

    with op.batch_alter_table('items', schema=None) as batch_op:
        batch_op.drop_constraint(batch_op.f('fk_items_event_id_events'), type_='foreignkey')

    with op.batch_alter_table('articles', schema=None) as batch_op:
        batch_op.drop_constraint(batch_op.f('fk_articles_event_id_events'), type_='foreignkey')
        batch_op.create_foreign_key('fk_articles_event_id_event', 'event', ['event_id'], ['id'])

    op.create_table('event',
    sa.Column('id', sa.INTEGER(), nullable=False),
    sa.Column('name', sa.VARCHAR(length=100), nullable=True),
    sa.Column('date', sa.DATE(), nullable=True),
    sa.Column('time', sa.TIME(), nullable=True),
    sa.Column('location', sa.VARCHAR(length=100), nullable=True),
    sa.Column('description', sa.TEXT(), nullable=True),
    sa.Column('days', sa.INTEGER(), nullable=True),
    sa.Column('image1', sa.VARCHAR(length=100), nullable=True),
    sa.Column('image2', sa.VARCHAR(length=100), nullable=True),
    sa.Column('image3', sa.VARCHAR(length=100), nullable=True),
    sa.Column('status', sa.VARCHAR(length=20), nullable=True),
    sa.Column('number', sa.VARCHAR(length=20), nullable=True),
    sa.Column('email', sa.VARCHAR(length=100), nullable=True),
    sa.Column('tags', sqlite.JSON(), nullable=True),
    sa.Column('views', sa.INTEGER(), nullable=True),
    sa.Column('eventtags', sa.VARCHAR(length=200), nullable=True),
    sa.Column('baseprice', sa.INTEGER(), nullable=True),
    sa.PrimaryKeyConstraint('id', name='pk_event')
    )
    op.drop_table('events')
    # ### end Alembic commands ###