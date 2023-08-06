from oslo_log import log

from neutron_lbaas_inventory.db.inventory_db import InventoryDbPlugin
from neutron_lbaas_inventory.db.lb_device_binding_db \
    import LbDeviceBindingDbPlugin
from neutron_lbaas_inventory.extensions import lbaasdevice

LOG = log.getLogger(__name__)


class LbaasDevicePlugin(lbaasdevice.LbaasDevicePluginBase):

    supported_extension_aliases = ["lbaas-device"]
    device_db = InventoryDbPlugin()
    lb_device_db = LbDeviceBindingDbPlugin()

    def get_devices(self, context, filters=None, fields=None,
                    sorts=None, limit=None, marker=None,
                    page_reverse=False):
        LOG.debug("List lbaas devices")
        devices = self.device_db.get_devices(context, filters=filters)
        return devices

    def get_device(self, context, id, fields=None):
        LOG.debug("Get a lbaas device, id: {}".format(id))
        return self.device_db.get_device(context, id)

    def create_device(self, context, device):
        LOG.debug("Create lbaas device, device_info: {}".format(device))
        return self.device_db.create_device(context, device)

    def delete_device(self, context, id):
        LOG.debug("Delete lbaas device, id: {}".format(id))
        self.device_db.delete_device(context, id)

    def update_device(self, context, id, device):
        LOG.debug("Update lbaas device, id: {}, device: {}".format(id, device))
        return self.device_db.update_device(context, id, device)

    def get_loadbalanceragentbindings(self, context, filters=None, fields=None,
                                      sorts=None, limit=None, marker=None,
                                      page_reverse=False):
        LOG.debug("List loadbalancer device bindings")
        lb_device_bindings = self.lb_device_db.get_bindings(context,
                                                            filters=filters)
        return lb_device_bindings
