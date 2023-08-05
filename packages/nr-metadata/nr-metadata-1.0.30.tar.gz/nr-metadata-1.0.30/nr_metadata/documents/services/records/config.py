from invenio_records_resources.services import (
    RecordLink,
    RecordServiceConfig,
    pagination_links,
)

from nr_metadata.documents.records.api import DocumentsRecord
from nr_metadata.documents.services.records.permissions import DocumentsPermissionPolicy
from nr_metadata.documents.services.records.schema import NRDocumentRecordSchema
from nr_metadata.documents.services.records.search import DocumentsSearchOptions


class DocumentsServiceConfig(RecordServiceConfig):
    """DocumentsRecord service config."""

    url_prefix = "/nr-metadata.documents/"

    permission_policy_cls = DocumentsPermissionPolicy

    schema = NRDocumentRecordSchema

    search = DocumentsSearchOptions

    record_cls = DocumentsRecord
    service_id = "documents"

    components = [*RecordServiceConfig.components]

    model = "documents"

    @property
    def links_item(self):
        return {
            "self": RecordLink("{self.url_prefix}{id}"),
        }

    @property
    def links_search(self):
        return pagination_links("{self.url_prefix}{?args*}")
