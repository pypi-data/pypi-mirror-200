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

from nr_metadata.ui_schema.identifiers import (
    NRAuthorityIdentifierUISchema,
    NRObjectIdentifierUISchema,
    NRSystemIdentifierUISchema,
)


class AdditionalTitlesUISchema(ma.Schema):
    """AdditionalTitlesUISchema schema."""

    title = I18nStrUIField()
    titleType = l10n.LocalizedEnum(value_prefix="nr_metadata.documents")


class NRAffiliationVocabularyUISchema(ma.Schema):
    """NRAffiliationVocabularyUISchema schema."""

    _id = ma_fields.String(data_key="id", attribute="id")
    title = VocabularyI18nStrUIField()
    type = ma_fields.String()
    hierarchy = ma_fields.Nested(lambda: HierarchyUISchema())
    _version = ma_fields.String(data_key="@v", attribute="@v")


class NRAuthorityUIUISchema(ma.Schema):
    """NRAuthorityUIUISchema schema."""

    affiliations = ma_fields.List(
        ma_fields.Nested(lambda: NRAffiliationVocabularyUISchema())
    )
    nameType = l10n.LocalizedEnum(value_prefix="nr_metadata.documents")
    fullName = ma_fields.String()
    authorityIdentifiers = ma_fields.List(
        ma_fields.Nested(lambda: NRAuthorityIdentifierUISchema())
    )


class NRAuthorityRoleVocabularyUISchema(ma.Schema):
    """NRAuthorityRoleVocabularyUISchema schema."""

    _id = ma_fields.String(data_key="id", attribute="id")
    title = VocabularyI18nStrUIField()
    type = ma_fields.String()
    _version = ma_fields.String(data_key="@v", attribute="@v")


class NRContributorUISchema(ma.Schema):
    """NRContributorUISchema schema."""

    role = ma_fields.Nested(lambda: NRAuthorityRoleVocabularyUISchema())
    affiliations = ma_fields.List(
        ma_fields.Nested(lambda: NRAffiliationVocabularyUISchema())
    )
    nameType = l10n.LocalizedEnum(value_prefix="nr_metadata.documents")
    fullName = ma_fields.String()
    authorityIdentifiers = ma_fields.List(
        ma_fields.Nested(lambda: NRAuthorityIdentifierUISchema())
    )


class NRResourceTypeVocabularyUISchema(ma.Schema):
    """NRResourceTypeVocabularyUISchema schema."""

    _id = ma_fields.String(data_key="id", attribute="id")
    title = VocabularyI18nStrUIField()
    type = ma_fields.String()
    _version = ma_fields.String(data_key="@v", attribute="@v")


class NRSubjectUISchema(ma.Schema):
    """NRSubjectUISchema schema."""

    subjectScheme = ma_fields.String()
    subject = MultilingualLocalizedUIField(I18nStrUIField())
    valueURI = ma_fields.String()
    classificationCode = ma_fields.String()


class NRSubjectCategoryVocabularyUISchema(ma.Schema):
    """NRSubjectCategoryVocabularyUISchema schema."""

    _id = ma_fields.String(data_key="id", attribute="id")
    title = VocabularyI18nStrUIField()
    type = ma_fields.String()
    _version = ma_fields.String(data_key="@v", attribute="@v")


class NRLanguageVocabularyUISchema(ma.Schema):
    """NRLanguageVocabularyUISchema schema."""

    _id = ma_fields.String(data_key="id", attribute="id")
    title = VocabularyI18nStrUIField()
    type = ma_fields.String()
    _version = ma_fields.String(data_key="@v", attribute="@v")


class NRLicenseVocabularyUISchema(ma.Schema):
    """NRLicenseVocabularyUISchema schema."""

    _id = ma_fields.String(data_key="id", attribute="id")
    title = VocabularyI18nStrUIField()
    type = ma_fields.String()
    _version = ma_fields.String(data_key="@v", attribute="@v")


class NRAccessRightsVocabularyUISchema(ma.Schema):
    """NRAccessRightsVocabularyUISchema schema."""

    _id = ma_fields.String(data_key="id", attribute="id")
    title = VocabularyI18nStrUIField()
    type = ma_fields.String()
    _version = ma_fields.String(data_key="@v", attribute="@v")


class NRItemRelationTypeVocabularyUISchema(ma.Schema):
    """NRItemRelationTypeVocabularyUISchema schema."""

    _id = ma_fields.String(data_key="id", attribute="id")
    title = VocabularyI18nStrUIField()
    type = ma_fields.String()
    _version = ma_fields.String(data_key="@v", attribute="@v")


class NRRelatedItemUISchema(ma.Schema):
    """NRRelatedItemUISchema schema."""

    itemTitle = ma_fields.String()
    itemCreators = ma_fields.List(ma_fields.Nested(lambda: NRAuthorityUIUISchema()))
    itemContributors = ma_fields.List(ma_fields.Nested(lambda: NRAuthorityUIUISchema()))
    itemPIDs = ma_fields.List(ma_fields.Nested(lambda: NRObjectIdentifierUISchema()))
    itemURL = ma_fields.String()
    itemYear = ma_fields.Integer()
    itemVolume = ma_fields.String()
    itemIssue = ma_fields.String()
    itemStartPage = ma_fields.String()
    itemEndPage = ma_fields.String()
    itemPublisher = ma_fields.String()
    itemRelationType = ma_fields.Nested(lambda: NRItemRelationTypeVocabularyUISchema())
    itemResourceType = ma_fields.Nested(lambda: NRResourceTypeVocabularyUISchema())


class NRFunderVocabularyUISchema(ma.Schema):
    """NRFunderVocabularyUISchema schema."""

    _id = ma_fields.String(data_key="id", attribute="id")
    title = VocabularyI18nStrUIField()
    type = ma_fields.String()
    _version = ma_fields.String(data_key="@v", attribute="@v")


class NRFundingReferenceUISchema(ma.Schema):
    """NRFundingReferenceUISchema schema."""

    projectID = ma_fields.String()
    projectName = ma_fields.String()
    fundingProgram = ma_fields.String()
    funder = ma_fields.Nested(lambda: NRFunderVocabularyUISchema())


class NRGeoLocationPointUISchema(ma.Schema):
    """NRGeoLocationPointUISchema schema."""

    pointLongitude = ma_fields.Float()
    pointLatitude = ma_fields.Float()


class NRGeoLocationUISchema(ma.Schema):
    """NRGeoLocationUISchema schema."""

    geoLocationPlace = ma_fields.String()
    geoLocationPoint = ma_fields.Nested(lambda: NRGeoLocationPointUISchema())


class NRSeriesUISchema(ma.Schema):
    """NRSeriesUISchema schema."""

    seriesTitle = ma_fields.String()
    seriesVolume = ma_fields.String()


class NRExternalLocationUISchema(ma.Schema):
    """NRExternalLocationUISchema schema."""

    externalLocationURL = ma_fields.String()
    externalLocationNote = ma_fields.String()


class NRCountryVocabularyUISchema(ma.Schema):
    """NRCountryVocabularyUISchema schema."""

    _id = ma_fields.String(data_key="id", attribute="id")
    title = VocabularyI18nStrUIField()
    type = ma_fields.String()
    _version = ma_fields.String(data_key="@v", attribute="@v")


class NRLocationUISchema(ma.Schema):
    """NRLocationUISchema schema."""

    place = ma_fields.String()
    country = ma_fields.Nested(lambda: NRCountryVocabularyUISchema())


class NREventUISchema(ma.Schema):
    """NREventUISchema schema."""

    eventNameOriginal = ma_fields.String()
    eventNameAlternate = ma_fields.List(ma_fields.String())
    eventDate = l10n.LocalizedEDTFInterval()
    eventLocation = ma_fields.Nested(lambda: NRLocationUISchema())


class NRCommonMetadataUISchema(ma.Schema):
    """NRCommonMetadataUISchema schema."""

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


class NRCommonRecordUISchema(InvenioUISchema):
    """NRCommonRecordUISchema schema."""

    metadata = ma_fields.Nested(lambda: NRCommonMetadataUISchema())
    _id = ma_fields.String(data_key="id", attribute="id")
    created = l10n.LocalizedDate()
    updated = l10n.LocalizedDate()
    _schema = ma_fields.String(data_key="$schema", attribute="$schema")
