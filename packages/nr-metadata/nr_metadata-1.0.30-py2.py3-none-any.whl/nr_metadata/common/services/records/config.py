from invenio_records_resources.services import (
    RecordLink,
    RecordServiceConfig,
    pagination_links,
)

from nr_metadata.common.records.api import CommonRecord
from nr_metadata.common.services.records.permissions import CommonPermissionPolicy
from nr_metadata.common.services.records.schema import NRCommonRecordSchema
from nr_metadata.common.services.records.search import CommonSearchOptions


class CommonServiceConfig(RecordServiceConfig):
    """CommonRecord service config."""

    url_prefix = "/nr-metadata.common/"

    permission_policy_cls = CommonPermissionPolicy

    schema = NRCommonRecordSchema

    search = CommonSearchOptions

    record_cls = CommonRecord
    service_id = "common"

    components = [*RecordServiceConfig.components]

    model = "common"

    @property
    def links_item(self):
        return {
            "self": RecordLink("{self.url_prefix}{id}"),
        }

    @property
    def links_search(self):
        return pagination_links("{self.url_prefix}{?args*}")
