"""empty message

Revision ID: 9d6d360c5a1a
Revises: 3f79f0d8dde4
Create Date: 2021-04-03 09:15:48.850653

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = '9d6d360c5a1a'
down_revision = '3f79f0d8dde4'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('device', sa.Column('device_id', sa.Integer(), nullable=False))
    op.drop_constraint('device_ibfk_1', 'device', type_='foreignkey')
    op.create_foreign_key(None, 'device', 'device', ['device_id'], ['id'])
    op.drop_column('device', 'device_data_id')
    op.add_column('device_data', sa.Column('device_data_id', sa.Integer(), nullable=True))
    op.create_foreign_key(None, 'device_data', 'device_data', ['device_data_id'], ['id'])
    op.drop_constraint('user_ibfk_1', 'user', type_='foreignkey')
    op.drop_column('user', 'device_id')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('user', sa.Column('device_id', mysql.INTEGER(display_width=11), autoincrement=False, nullable=False))
    op.create_foreign_key('user_ibfk_1', 'user', 'device', ['device_id'], ['id'])
    op.drop_constraint(None, 'device_data', type_='foreignkey')
    op.drop_column('device_data', 'device_data_id')
    op.add_column('device', sa.Column('device_data_id', mysql.INTEGER(display_width=11), autoincrement=False, nullable=True))
    op.drop_constraint(None, 'device', type_='foreignkey')
    op.create_foreign_key('device_ibfk_1', 'device', 'device_data', ['device_data_id'], ['id'])
    op.drop_column('device', 'device_id')
    # ### end Alembic commands ###
