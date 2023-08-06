from neutron_lib.db import model_base
import sqlalchemy as sa


class Device(model_base.BASEV2, model_base.HasId, model_base.HasProject):
    """Represents a backend device"""

    NAME = "device"

    __tablename__ = "lbaas_devices"

    name = sa.Column(sa.String(255), nullable=True)
    description = sa.Column(sa.String(255), nullable=True)
    type = sa.Column(sa.String(16), nullable=False)
    shared = sa.Column(sa.Boolean(), nullable=False)
    admin_state_up = sa.Column(sa.Boolean(), nullable=False)
    availability_zone = sa.Column(sa.String(255), nullable=True)
    provisioning_status = sa.Column(sa.String(255), nullable=True)
    operating_status = sa.Column(sa.String(255), nullable=True)
    device_info = sa.Column(sa.String(4095), nullable=True)
    last_error = sa.Column(sa.String(4095), nullable=True)
