from neutron.db import api as db_api
from neutron.db import db_base_plugin_common
from neutron.db import _model_query as model_query
from neutron.db import _utils as db_utils
from neutron_lbaas.agent_scheduler import LoadbalancerAgentBinding


class LbDeviceBindingDbPlugin(db_base_plugin_common.DbBasePluginCommon):

    @db_api.retry_if_session_inactive()
    def get_bindings(self, context, filters=None):
        return [
            binding
            for binding in model_query.get_collection(
                context, LoadbalancerAgentBinding, self._binding_dict,
                filters=filters)
        ]

    def _binding_dict(self, binding_db, fields=None):
        binding = dict((k, binding_db[k])
                       for k in binding_db.keys())
        return db_utils.resource_fields(binding, fields)
