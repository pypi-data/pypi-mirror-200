from neutron.db.migration.models import head


def get_metadata():
    return head.model_base.BASEV2.metadata
