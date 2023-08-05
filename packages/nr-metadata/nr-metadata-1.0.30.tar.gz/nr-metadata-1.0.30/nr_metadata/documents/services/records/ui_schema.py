import marshmallow as ma
from marshmallow import fields as ma_fields
from oarepo_runtime.i18n.ui_schema import (
    I18nStrUIField,
    MultilingualLocalizedUIField,
    MultilingualUIField,
)
from oarepo_runtime.ui import marshmallow as l10n
from oarepo_runtime.ui.marshmallow import InvenioUISchema
from oarepo_vocabularies.services.ui_schemas import (
    HierarchyUISchema,
    VocabularyI18nStrUIField,
)

from nr_metadata.common.services.records.ui_schema import (
    AdditionalTitlesUISchema,
    NRAccessRightsVocabularyUISchema,
    NRAuthorityUIUISchema,
    NRContributorUISchema,
    NREventUISchema,
    NRExternalLocationUISchema,
    NRFundingReferenceUISchema,
    NRGeoLocationUISchema,
    NRLanguageVocabularyUISchema,
    NRLicenseVocabularyUISchema,
    NRRelatedItemUISchema,
    NRResourceTypeVocabularyUISchema,
    NRSeriesUISchema,
    NRSubjectCategoryVocabularyUISchema,
    NRSubjectUISchema,
)
from nr_metadata.ui_schema.identifiers import (
    NRObjectIdentifierUISchema,
    NRSystemIdentifierUISchema,
)


class NRDegreeGrantorUISchema(ma.Schema):
    """NRDegreeGrantorUISchema schema."""

    _id = ma_fields.String(data_key="id", attribute="id")
    title = VocabularyI18nStrUIField()
    type = ma_fields.String()
    hierarchy = ma_fields.Nested(lambda: HierarchyUISchema())
    _version = ma_fields.String(data_key="@v", attribute="@v")


class NRThesisUISchema(ma.Schema):
    """NRThesisUISchema schema."""

    dateDefended = l10n.LocalizedDate()
    defended = ma_fields.Boolean()
    degreeGrantors = ma_fields.List(ma_fields.Nested(lambda: NRDegreeGrantorUISchema()))
    studyFields = ma_fields.List(ma_fields.String())


class NRDocumentMetadataUISchema(ma.Schema):
    """NRDocumentMetadataUISchema schema."""

    thesis = ma_fields.Nested(lambda: NRThesisUISchema())
    collection = ma_fields.String()
    title = ma_fields.String()
    additionalTitles = ma_fields.List(
        ma_fields.Nested(lambda: AdditionalTitlesUISchema())
    )
    creators = ma_fields.List(ma_fields.Nested(lambda: NRAuthorityUIUISchema()))
    contributors = ma_fields.List(ma_fields.Nested(lambda: NRContributorUISchema()))
    resourceType = ma_fields.Nested(lambda: NRResourceTypeVocabularyUISchema())
    dateAvailable = l10n.LocalizedEDTF()
    dateModified = l10n.LocalizedEDTF()
    subjects = ma_fields.List(ma_fields.Nested(lambda: NRSubjectUISchema()))
    publishers = ma_fields.List(ma_fields.String())
    subjectCategories = ma_fields.List(
        ma_fields.Nested(lambda: NRSubjectCategoryVocabularyUISchema())
    )
    languages = ma_fields.List(ma_fields.Nested(lambda: NRLanguageVocabularyUISchema()))
    notes = ma_fields.List(ma_fields.String())
    abstract = MultilingualUIField(I18nStrUIField())
    methods = MultilingualUIField(I18nStrUIField())
    technicalInfo = MultilingualUIField(I18nStrUIField())
    rights = ma_fields.List(ma_fields.Nested(lambda: NRLicenseVocabularyUISchema()))
    accessRights = ma_fields.Nested(lambda: NRAccessRightsVocabularyUISchema())
    relatedItems = ma_fields.List(ma_fields.Nested(lambda: NRRelatedItemUISchema()))
    fundingReferences = ma_fields.List(
        ma_fields.Nested(lambda: NRFundingReferenceUISchema())
    )
    version = ma_fields.String()
    geoLocations = ma_fields.List(ma_fields.Nested(lambda: NRGeoLocationUISchema()))
    accessibility = MultilingualLocalizedUIField(I18nStrUIField())
    series = ma_fields.List(ma_fields.Nested(lambda: NRSeriesUISchema()))
    externalLocation = ma_fields.Nested(lambda: NRExternalLocationUISchema())
    originalRecord = ma_fields.String()
    objectIdentifiers = ma_fields.List(
        ma_fields.Nested(lambda: NRObjectIdentifierUISchema())
    )
    systemIdentifiers = ma_fields.List(
        ma_fields.Nested(lambda: NRSystemIdentifierUISchema())
    )
    events = ma_fields.List(ma_fields.Nested(lambda: NREventUISchema()))


class NRDocumentRecordUISchema(InvenioUISchema):
    """NRDocumentRecordUISchema schema."""

    metadata = ma_fields.Nested(lambda: NRDocumentMetadataUISchema())
    _id = ma_fields.String(data_key="id", attribute="id")
    created = l10n.LocalizedDate()
    updated = l10n.LocalizedDate()
    _schema = ma_fields.String(data_key="$schema", attribute="$schema")
