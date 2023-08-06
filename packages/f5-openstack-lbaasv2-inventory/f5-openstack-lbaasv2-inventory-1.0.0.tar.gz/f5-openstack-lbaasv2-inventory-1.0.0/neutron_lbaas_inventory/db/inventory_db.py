from neutron.db import api as db_api
from neutron.db import db_base_plugin_common
from neutron.db import _model_query as model_query
from neutron.db import _utils as db_utils

from neutron_lbaas_inventory.common import constants
from neutron_lbaas_inventory.common import exceptions as exc
from neutron_lbaas_inventory.db.models import inventory as models

from oslo_serialization import jsonutils
from oslo_log import log as logging
from oslo_utils import uuidutils
from sqlalchemy.orm import exc as db_exc

LOG = logging.getLogger(__name__)


class InventoryDbPlugin(db_base_plugin_common.DbBasePluginCommon):

    @db_api.retry_if_session_inactive()
    def create_device(self, context, payload):
        device = payload["device"]

        with db_api.context_manager.writer.using(context):
            args = {
                "id": device.get("id") or uuidutils.generate_uuid(),
                "name": device.get("name"),
                "description": device.get("description"),
                "project_id": device["project_id"],
                "type": device["type"],
                "shared": device.get("shared", True),
                "admin_state_up": device.get("admin_state_up", True),
                "availability_zone": device.get("availability_zone"),
                "provisioning_status": jsonutils.dumps(
                    {"status": constants.IDLE}),
                "operating_status": jsonutils.dumps(
                    {"status": constants.ONLINE}),
                "device_info": jsonutils.dumps(device["device_info"]),
                "last_error": jsonutils.dumps("{}"),
            }
            device_db = models.Device(**args)
            context.session.add(device_db)

        return self._device_dict(device_db)

    @db_api.retry_if_session_inactive()
    def delete_device(self, context, id):
        with context.session.begin(subtransactions=True):
            in_use, lb_ids = self._device_in_use(id)
            if in_use:
                raise exc.DeviceInUse(device_id=id, loadbalancer_ids=lb_ids)
            else:
                device = self._get_device(context, id)
                context.session.delete(device)

    @db_api.retry_if_session_inactive()
    def get_devices(self, context, filters=None):
        return [
            device
            for device in model_query.get_collection(
                context, models.Device, self._device_dict, filters=filters)
        ]

    @db_api.retry_if_session_inactive()
    def get_device(self, context, id):
        return self._device_dict(self._get_device(context, id))

    @db_api.retry_if_session_inactive()
    def update_device(self, context, id, payload):
        json_keys = [
            "provisioning_status",
            "operating_status",
            "device_info",
            "last_error"
        ]
        device = payload["device"]
        for key in json_keys:
            if key in device:
                device[key] = jsonutils.dumps(device[key])

        with context.session.begin(subtransactions=True):
            device_db = self._get_device(context, id)
            if device:
                device_db.update(device)

        return self._device_dict(device_db)

    def _get_device(self, context, id):
        try:
            device = model_query.get_by_id(
                context, models.Device, id)
        except db_exc.NoResultFound:
            raise exc.DeviceNotFound(device_id=id)
        return device

    def _device_in_use(self, id):
        # TODO(qzhao): Need to query agent binding table
        return False, []

    def _device_dict(self, device_db, fields=None):
        json_keys = [
            "provisioning_status",
            "operating_status",
            "device_info",
            "last_error"
        ]

        device = dict((k, device_db[k])
                      for k in device_db.keys() if k not in json_keys)
        for k in json_keys:
            device[k] = self._get_dict(device_db, k)

        return db_utils.resource_fields(device, fields)

    def _get_dict(self, device_db, dict_name, ignore_missing=False):
        json_string = None
        try:
            json_string = getattr(device_db, dict_name)
            json_dict = jsonutils.loads(json_string)
        except Exception:
            if json_string or not ignore_missing:
                msg = "Dictionary %(dict_name)s for device %(id)s is invalid."
                LOG.warning(msg, {"dict_name": dict_name,
                                  "id": device_db.id})
            json_dict = {}
        return json_dict
