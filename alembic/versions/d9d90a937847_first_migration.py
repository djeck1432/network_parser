"""first migration

Revision ID: d9d90a937847
Revises: 
Create Date: 2023-06-07 21:27:48.687493

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'd9d90a937847'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('network_config',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('connection', sa.Integer(), nullable=True),
    sa.Column('name', sa.String(length=255), nullable=False),
    sa.Column('description', sa.String(length=255), nullable=True),
    sa.Column('config', sa.JSON(), nullable=True),
    sa.Column('type', sa.String(length=50), nullable=True),
    sa.Column('infra_type', sa.String(length=50), nullable=True),
    sa.Column('port_channel_id', sa.Integer(), nullable=True),
    sa.Column('max_frame_size', sa.Integer(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_network_config_name'), 'network_config', ['name'], unique=False)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_network_config_name'), table_name='network_config')
    op.drop_table('network_config')
    # ### end Alembic commands ###
