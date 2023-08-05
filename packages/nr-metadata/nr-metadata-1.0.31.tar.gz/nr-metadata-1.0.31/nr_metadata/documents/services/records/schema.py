import marshmallow as ma
from edtf import Date as EDTFDate
from invenio_records_resources.services.records.schema import (
    BaseRecordSchema as InvenioBaseRecordSchema,
)
from invenio_vocabularies.services.schema import i18n_strings
from marshmallow import fields as ma_fields
from marshmallow_utils.fields import edtfdatestring as mu_fields_edtf
from oarepo_runtime.i18n.schema import I18nStrField, MultilingualField
from oarepo_runtime.validation import validate_date
from oarepo_vocabularies.services.schemas import HierarchySchema

from nr_metadata.common.services.records.schema import (
    AdditionalTitlesSchema,
    NRAccessRightsVocabularySchema,
    NRAuthoritySchema,
    NRContributorSchema,
    NREventSchema,
    NRExternalLocationSchema,
    NRFundingReferenceSchema,
    NRGeoLocationSchema,
    NRLanguageVocabularySchema,
    NRLicenseVocabularySchema,
    NRRelatedItemSchema,
    NRResourceTypeVocabularySchema,
    NRSeriesSchema,
    NRSubjectCategoryVocabularySchema,
    NRSubjectSchema,
)
from nr_metadata.schema.identifiers import (
    NRObjectIdentifierSchema,
    NRSystemIdentifierSchema,
)


class NRDegreeGrantorSchema(ma.Schema):
    """NRDegreeGrantorSchema schema."""

    _id = ma_fields.String(data_key="id", attribute="id")
    title = i18n_strings
    type = ma_fields.String()
    hierarchy = ma_fields.Nested(lambda: HierarchySchema())
    _version = ma_fields.String(data_key="@v", attribute="@v")


class NRThesisSchema(ma.Schema):
    """NRThesisSchema schema."""

    dateDefended = ma_fields.String(validate=[validate_date("%Y-%m-%d")])
    defended = ma_fields.Boolean()
    degreeGrantors = ma_fields.List(ma_fields.Nested(lambda: NRDegreeGrantorSchema()))
    studyFields = ma_fields.List(ma_fields.String())


class NRDocumentMetadataSchema(ma.Schema):
    """NRDocumentMetadataSchema schema."""

    thesis = ma_fields.Nested(lambda: NRThesisSchema())
    collection = ma_fields.String()
    title = ma_fields.String()
    additionalTitles = ma_fields.List(
        ma_fields.Nested(lambda: AdditionalTitlesSchema())
    )
    creators = ma_fields.List(ma_fields.Nested(lambda: NRAuthoritySchema()))
    contributors = ma_fields.List(ma_fields.Nested(lambda: NRContributorSchema()))
    resourceType = ma_fields.Nested(lambda: NRResourceTypeVocabularySchema())
    dateAvailable = ma_fields.String(
        validate=[mu_fields_edtf.EDTFValidator(types=(EDTFDate,))]
    )
    dateModified = ma_fields.String(
        validate=[mu_fields_edtf.EDTFValidator(types=(EDTFDate,))]
    )
    subjects = ma_fields.List(ma_fields.Nested(lambda: NRSubjectSchema()))
    publishers = ma_fields.List(ma_fields.String())
    subjectCategories = ma_fields.List(
        ma_fields.Nested(lambda: NRSubjectCategoryVocabularySchema())
    )
    languages = ma_fields.List(ma_fields.Nested(lambda: NRLanguageVocabularySchema()))
    notes = ma_fields.List(ma_fields.String())
    abstract = MultilingualField(I18nStrField())
    methods = MultilingualField(I18nStrField())
    technicalInfo = MultilingualField(I18nStrField())
    rights = ma_fields.List(ma_fields.Nested(lambda: NRLicenseVocabularySchema()))
    accessRights = ma_fields.Nested(lambda: NRAccessRightsVocabularySchema())
    relatedItems = ma_fields.List(ma_fields.Nested(lambda: NRRelatedItemSchema()))
    fundingReferences = ma_fields.List(
        ma_fields.Nested(lambda: NRFundingReferenceSchema())
    )
    version = ma_fields.String()
    geoLocations = ma_fields.List(ma_fields.Nested(lambda: NRGeoLocationSchema()))
    accessibility = MultilingualField(I18nStrField())
    series = ma_fields.List(ma_fields.Nested(lambda: NRSeriesSchema()))
    externalLocation = ma_fields.Nested(lambda: NRExternalLocationSchema())
    originalRecord = ma_fields.String()
    objectIdentifiers = ma_fields.List(
        ma_fields.Nested(lambda: NRObjectIdentifierSchema())
    )
    systemIdentifiers = ma_fields.List(
        ma_fields.Nested(lambda: NRSystemIdentifierSchema())
    )
    events = ma_fields.List(ma_fields.Nested(lambda: NREventSchema()))


class NRDocumentRecordSchema(InvenioBaseRecordSchema):
    """NRDocumentRecordSchema schema."""

    metadata = ma_fields.Nested(lambda: NRDocumentMetadataSchema())
