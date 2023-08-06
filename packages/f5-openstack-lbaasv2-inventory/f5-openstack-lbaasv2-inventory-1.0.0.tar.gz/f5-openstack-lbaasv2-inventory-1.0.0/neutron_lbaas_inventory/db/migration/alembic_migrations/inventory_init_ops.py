# Initial operations for LBaaSv2 device inventory

from alembic import op
import sqlalchemy as sa


def upgrade():
    op.create_table(
        u'lbaas_devices',
        sa.Column(u'project_id', sa.String(255), nullable=True),
        sa.Column(u'id', sa.String(36), nullable=False),
        sa.Column(u'name', sa.String(255), nullable=True),
        sa.Column(u'description', sa.String(255), nullable=True),
        sa.Column(u'type', sa.String(16), nullable=False),
        sa.Column(u'shared', sa.Boolean(), nullable=False),
        sa.Column(u'admin_state_up', sa.Boolean(), nullable=False),
        sa.Column(u'availability_zone', sa.String(255), nullable=True),
        sa.Column(u'provisioning_status', sa.String(255), nullable=True),
        sa.Column(u'operating_status', sa.String(255), nullable=True),
        sa.Column(u'device_info', sa.String(4095), nullable=True),
        sa.Column(u'last_error', sa.String(4095), nullable=True),
        sa.PrimaryKeyConstraint(u'id')
    )
