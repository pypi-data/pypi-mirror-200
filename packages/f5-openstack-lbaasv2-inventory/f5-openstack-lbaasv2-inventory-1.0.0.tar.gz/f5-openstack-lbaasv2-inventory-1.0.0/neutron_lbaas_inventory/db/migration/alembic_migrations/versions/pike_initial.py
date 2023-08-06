from neutron_lbaas_inventory.db.migration.alembic_migrations import inventory_init_ops  # noqa

"""pike_initial

Revision ID: pike
Revises: None

"""

# revision identifiers, used by Alembic.
revision = "pike"
down_revision = None


def upgrade():
    inventory_init_ops.upgrade()
