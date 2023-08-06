"""
Type annotations for guardduty service type definitions.

[Open documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_guardduty/type_defs/)

Usage::

    ```python
    from mypy_boto3_guardduty.type_defs import AcceptAdministratorInvitationRequestRequestTypeDef

    data: AcceptAdministratorInvitationRequestRequestTypeDef = {...}
    ```
"""
import sys
from datetime import datetime
from typing import Dict, List, Mapping, Sequence

from .literals import (
    AdminStatusType,
    AutoEnableMembersType,
    CoverageFilterCriterionKeyType,
    CoverageSortKeyType,
    CoverageStatisticsTypeType,
    CoverageStatusType,
    CriterionKeyType,
    DataSourceStatusType,
    DataSourceType,
    DetectorFeatureResultType,
    DetectorFeatureType,
    DetectorStatusType,
    EbsSnapshotPreservationType,
    FeatureStatusType,
    FeedbackType,
    FilterActionType,
    FindingPublishingFrequencyType,
    FreeTrialFeatureResultType,
    IpSetFormatType,
    IpSetStatusType,
    OrderByType,
    OrgFeatureStatusType,
    OrgFeatureType,
    PublishingStatusType,
    ScanResultType,
    ScanStatusType,
    ThreatIntelSetFormatType,
    ThreatIntelSetStatusType,
    UsageFeatureType,
    UsageStatisticTypeType,
)

if sys.version_info >= (3, 9):
    from typing import Literal
else:
    from typing_extensions import Literal
if sys.version_info >= (3, 9):
    from typing import TypedDict
else:
    from typing_extensions import TypedDict


__all__ = (
    "AcceptAdministratorInvitationRequestRequestTypeDef",
    "AcceptInvitationRequestRequestTypeDef",
    "AccessControlListTypeDef",
    "AccessKeyDetailsTypeDef",
    "AccountDetailTypeDef",
    "FreeTrialFeatureConfigurationResultTypeDef",
    "BlockPublicAccessTypeDef",
    "DnsRequestActionTypeDef",
    "AddonDetailsTypeDef",
    "AdminAccountTypeDef",
    "AdministratorTypeDef",
    "ArchiveFindingsRequestRequestTypeDef",
    "DomainDetailsTypeDef",
    "RemoteAccountDetailsTypeDef",
    "BucketPolicyTypeDef",
    "CityTypeDef",
    "CloudTrailConfigurationResultTypeDef",
    "ConditionTypeDef",
    "SecurityContextTypeDef",
    "VolumeMountTypeDef",
    "CountryTypeDef",
    "CoverageFilterConditionTypeDef",
    "CoverageSortCriteriaTypeDef",
    "CoverageStatisticsTypeDef",
    "ResponseMetadataTypeDef",
    "CreateIPSetRequestRequestTypeDef",
    "UnprocessedAccountTypeDef",
    "DestinationPropertiesTypeDef",
    "CreateSampleFindingsRequestRequestTypeDef",
    "CreateThreatIntelSetRequestRequestTypeDef",
    "DNSLogsConfigurationResultTypeDef",
    "FlowLogsConfigurationResultTypeDef",
    "S3LogsConfigurationResultTypeDef",
    "S3LogsConfigurationTypeDef",
    "DataSourceFreeTrialTypeDef",
    "DeclineInvitationsRequestRequestTypeDef",
    "DefaultServerSideEncryptionTypeDef",
    "DeleteDetectorRequestRequestTypeDef",
    "DeleteFilterRequestRequestTypeDef",
    "DeleteIPSetRequestRequestTypeDef",
    "DeleteInvitationsRequestRequestTypeDef",
    "DeleteMembersRequestRequestTypeDef",
    "DeletePublishingDestinationRequestRequestTypeDef",
    "DeleteThreatIntelSetRequestRequestTypeDef",
    "PaginatorConfigTypeDef",
    "SortCriteriaTypeDef",
    "DescribeOrganizationConfigurationRequestRequestTypeDef",
    "DescribePublishingDestinationRequestRequestTypeDef",
    "DestinationTypeDef",
    "DetectorAdditionalConfigurationResultTypeDef",
    "DetectorAdditionalConfigurationTypeDef",
    "DisableOrganizationAdminAccountRequestRequestTypeDef",
    "DisassociateFromAdministratorAccountRequestRequestTypeDef",
    "DisassociateFromMasterAccountRequestRequestTypeDef",
    "DisassociateMembersRequestRequestTypeDef",
    "VolumeDetailTypeDef",
    "EbsVolumesResultTypeDef",
    "TagTypeDef",
    "EnableOrganizationAdminAccountRequestRequestTypeDef",
    "ThreatIntelligenceDetailTypeDef",
    "FilterConditionTypeDef",
    "FindingStatisticsTypeDef",
    "GeoLocationTypeDef",
    "GetAdministratorAccountRequestRequestTypeDef",
    "GetDetectorRequestRequestTypeDef",
    "GetFilterRequestRequestTypeDef",
    "GetIPSetRequestRequestTypeDef",
    "GetMalwareScanSettingsRequestRequestTypeDef",
    "GetMasterAccountRequestRequestTypeDef",
    "MasterTypeDef",
    "GetMemberDetectorsRequestRequestTypeDef",
    "GetMembersRequestRequestTypeDef",
    "MemberTypeDef",
    "GetRemainingFreeTrialDaysRequestRequestTypeDef",
    "GetThreatIntelSetRequestRequestTypeDef",
    "UsageCriteriaTypeDef",
    "HighestSeverityThreatDetailsTypeDef",
    "HostPathTypeDef",
    "IamInstanceProfileTypeDef",
    "ProductCodeTypeDef",
    "InvitationTypeDef",
    "InviteMembersRequestRequestTypeDef",
    "KubernetesAuditLogsConfigurationResultTypeDef",
    "KubernetesAuditLogsConfigurationTypeDef",
    "KubernetesUserDetailsTypeDef",
    "LineageObjectTypeDef",
    "ListDetectorsRequestRequestTypeDef",
    "ListFiltersRequestRequestTypeDef",
    "ListIPSetsRequestRequestTypeDef",
    "ListInvitationsRequestRequestTypeDef",
    "ListMembersRequestRequestTypeDef",
    "ListOrganizationAdminAccountsRequestRequestTypeDef",
    "ListPublishingDestinationsRequestRequestTypeDef",
    "ListTagsForResourceRequestRequestTypeDef",
    "ListThreatIntelSetsRequestRequestTypeDef",
    "LocalIpDetailsTypeDef",
    "LocalPortDetailsTypeDef",
    "LoginAttributeTypeDef",
    "ScanEc2InstanceWithFindingsTypeDef",
    "MemberAdditionalConfigurationResultTypeDef",
    "MemberAdditionalConfigurationTypeDef",
    "RemotePortDetailsTypeDef",
    "PrivateIpAddressDetailsTypeDef",
    "SecurityGroupTypeDef",
    "OrganizationAdditionalConfigurationResultTypeDef",
    "OrganizationAdditionalConfigurationTypeDef",
    "OrganizationS3LogsConfigurationResultTypeDef",
    "OrganizationS3LogsConfigurationTypeDef",
    "OrganizationEbsVolumesResultTypeDef",
    "OrganizationEbsVolumesTypeDef",
    "OrganizationKubernetesAuditLogsConfigurationResultTypeDef",
    "OrganizationKubernetesAuditLogsConfigurationTypeDef",
    "OrganizationTypeDef",
    "OwnerTypeDef",
    "RdsDbUserDetailsTypeDef",
    "ResourceDetailsTypeDef",
    "ScanConditionPairTypeDef",
    "ScannedItemCountTypeDef",
    "ThreatsDetectedItemCountTypeDef",
    "ScanFilePathTypeDef",
    "ScanResultDetailsTypeDef",
    "TriggerDetailsTypeDef",
    "ServiceAdditionalInfoTypeDef",
    "StartMonitoringMembersRequestRequestTypeDef",
    "StopMonitoringMembersRequestRequestTypeDef",
    "TagResourceRequestRequestTypeDef",
    "TotalTypeDef",
    "UnarchiveFindingsRequestRequestTypeDef",
    "UntagResourceRequestRequestTypeDef",
    "UpdateFindingsFeedbackRequestRequestTypeDef",
    "UpdateIPSetRequestRequestTypeDef",
    "UpdateThreatIntelSetRequestRequestTypeDef",
    "CreateMembersRequestRequestTypeDef",
    "AccountLevelPermissionsTypeDef",
    "CoverageEksClusterDetailsTypeDef",
    "BucketLevelPermissionsTypeDef",
    "FindingCriteriaTypeDef",
    "ContainerTypeDef",
    "CoverageFilterCriterionTypeDef",
    "CreateFilterResponseTypeDef",
    "CreateIPSetResponseTypeDef",
    "CreatePublishingDestinationResponseTypeDef",
    "CreateThreatIntelSetResponseTypeDef",
    "GetAdministratorAccountResponseTypeDef",
    "GetCoverageStatisticsResponseTypeDef",
    "GetIPSetResponseTypeDef",
    "GetInvitationsCountResponseTypeDef",
    "GetThreatIntelSetResponseTypeDef",
    "ListDetectorsResponseTypeDef",
    "ListFiltersResponseTypeDef",
    "ListFindingsResponseTypeDef",
    "ListIPSetsResponseTypeDef",
    "ListOrganizationAdminAccountsResponseTypeDef",
    "ListTagsForResourceResponseTypeDef",
    "ListThreatIntelSetsResponseTypeDef",
    "UpdateFilterResponseTypeDef",
    "CreateMembersResponseTypeDef",
    "DeclineInvitationsResponseTypeDef",
    "DeleteInvitationsResponseTypeDef",
    "DeleteMembersResponseTypeDef",
    "DisassociateMembersResponseTypeDef",
    "InviteMembersResponseTypeDef",
    "StartMonitoringMembersResponseTypeDef",
    "StopMonitoringMembersResponseTypeDef",
    "UpdateMemberDetectorsResponseTypeDef",
    "CreatePublishingDestinationRequestRequestTypeDef",
    "DescribePublishingDestinationResponseTypeDef",
    "UpdatePublishingDestinationRequestRequestTypeDef",
    "KubernetesDataSourceFreeTrialTypeDef",
    "MalwareProtectionDataSourceFreeTrialTypeDef",
    "ListDetectorsRequestListDetectorsPaginateTypeDef",
    "ListFiltersRequestListFiltersPaginateTypeDef",
    "ListIPSetsRequestListIPSetsPaginateTypeDef",
    "ListInvitationsRequestListInvitationsPaginateTypeDef",
    "ListMembersRequestListMembersPaginateTypeDef",
    "ListOrganizationAdminAccountsRequestListOrganizationAdminAccountsPaginateTypeDef",
    "ListThreatIntelSetsRequestListThreatIntelSetsPaginateTypeDef",
    "GetFindingsRequestRequestTypeDef",
    "ListPublishingDestinationsResponseTypeDef",
    "DetectorFeatureConfigurationResultTypeDef",
    "DetectorFeatureConfigurationTypeDef",
    "EbsVolumeDetailsTypeDef",
    "ScanEc2InstanceWithFindingsResultTypeDef",
    "EksClusterDetailsTypeDef",
    "RdsDbInstanceDetailsTypeDef",
    "EvidenceTypeDef",
    "FilterCriterionTypeDef",
    "GetFindingsStatisticsResponseTypeDef",
    "GetMasterAccountResponseTypeDef",
    "GetMembersResponseTypeDef",
    "ListMembersResponseTypeDef",
    "GetUsageStatisticsRequestRequestTypeDef",
    "VolumeTypeDef",
    "ListInvitationsResponseTypeDef",
    "KubernetesConfigurationResultTypeDef",
    "KubernetesConfigurationTypeDef",
    "ProcessDetailsTypeDef",
    "MalwareProtectionConfigurationTypeDef",
    "MemberFeaturesConfigurationResultTypeDef",
    "MemberFeaturesConfigurationTypeDef",
    "NetworkInterfaceTypeDef",
    "OrganizationFeatureConfigurationResultTypeDef",
    "OrganizationFeatureConfigurationTypeDef",
    "OrganizationScanEc2InstanceWithFindingsResultTypeDef",
    "OrganizationScanEc2InstanceWithFindingsTypeDef",
    "OrganizationKubernetesConfigurationResultTypeDef",
    "OrganizationKubernetesConfigurationTypeDef",
    "RemoteIpDetailsTypeDef",
    "ScanConditionTypeDef",
    "ScanThreatNameTypeDef",
    "ScanTypeDef",
    "UsageAccountResultTypeDef",
    "UsageDataSourceResultTypeDef",
    "UsageFeatureResultTypeDef",
    "UsageResourceResultTypeDef",
    "CoverageResourceDetailsTypeDef",
    "PermissionConfigurationTypeDef",
    "CreateFilterRequestRequestTypeDef",
    "GetFilterResponseTypeDef",
    "GetFindingsStatisticsRequestRequestTypeDef",
    "ListFindingsRequestListFindingsPaginateTypeDef",
    "ListFindingsRequestRequestTypeDef",
    "UpdateFilterRequestRequestTypeDef",
    "CoverageFilterCriteriaTypeDef",
    "DataSourcesFreeTrialTypeDef",
    "MalwareProtectionConfigurationResultTypeDef",
    "FilterCriteriaTypeDef",
    "EcsTaskDetailsTypeDef",
    "KubernetesWorkloadDetailsTypeDef",
    "RuntimeContextTypeDef",
    "DataSourceConfigurationsTypeDef",
    "InstanceDetailsTypeDef",
    "OrganizationMalwareProtectionConfigurationResultTypeDef",
    "OrganizationMalwareProtectionConfigurationTypeDef",
    "AwsApiCallActionTypeDef",
    "KubernetesApiCallActionTypeDef",
    "NetworkConnectionActionTypeDef",
    "PortProbeDetailTypeDef",
    "RdsLoginAttemptActionTypeDef",
    "ScanResourceCriteriaTypeDef",
    "ThreatDetectedByNameTypeDef",
    "DescribeMalwareScansResponseTypeDef",
    "UsageStatisticsTypeDef",
    "CoverageResourceTypeDef",
    "PublicAccessTypeDef",
    "GetCoverageStatisticsRequestRequestTypeDef",
    "ListCoverageRequestListCoveragePaginateTypeDef",
    "ListCoverageRequestRequestTypeDef",
    "AccountFreeTrialInfoTypeDef",
    "DataSourceConfigurationsResultTypeDef",
    "UnprocessedDataSourcesResultTypeDef",
    "DescribeMalwareScansRequestDescribeMalwareScansPaginateTypeDef",
    "DescribeMalwareScansRequestRequestTypeDef",
    "EcsClusterDetailsTypeDef",
    "KubernetesDetailsTypeDef",
    "RuntimeDetailsTypeDef",
    "CreateDetectorRequestRequestTypeDef",
    "UpdateDetectorRequestRequestTypeDef",
    "UpdateMemberDetectorsRequestRequestTypeDef",
    "OrganizationDataSourceConfigurationsResultTypeDef",
    "OrganizationDataSourceConfigurationsTypeDef",
    "PortProbeActionTypeDef",
    "GetMalwareScanSettingsResponseTypeDef",
    "UpdateMalwareScanSettingsRequestRequestTypeDef",
    "ScanDetectionsTypeDef",
    "GetUsageStatisticsResponseTypeDef",
    "ListCoverageResponseTypeDef",
    "S3BucketDetailTypeDef",
    "GetRemainingFreeTrialDaysResponseTypeDef",
    "GetDetectorResponseTypeDef",
    "MemberDataSourceConfigurationTypeDef",
    "CreateDetectorResponseTypeDef",
    "DescribeOrganizationConfigurationResponseTypeDef",
    "UpdateOrganizationConfigurationRequestRequestTypeDef",
    "ActionTypeDef",
    "EbsVolumeScanDetailsTypeDef",
    "ResourceTypeDef",
    "GetMemberDetectorsResponseTypeDef",
    "ServiceTypeDef",
    "FindingTypeDef",
    "GetFindingsResponseTypeDef",
)

AcceptAdministratorInvitationRequestRequestTypeDef = TypedDict(
    "AcceptAdministratorInvitationRequestRequestTypeDef",
    {
        "DetectorId": str,
        "AdministratorId": str,
        "InvitationId": str,
    },
)

AcceptInvitationRequestRequestTypeDef = TypedDict(
    "AcceptInvitationRequestRequestTypeDef",
    {
        "DetectorId": str,
        "MasterId": str,
        "InvitationId": str,
    },
)

AccessControlListTypeDef = TypedDict(
    "AccessControlListTypeDef",
    {
        "AllowsPublicReadAccess": bool,
        "AllowsPublicWriteAccess": bool,
    },
    total=False,
)

AccessKeyDetailsTypeDef = TypedDict(
    "AccessKeyDetailsTypeDef",
    {
        "AccessKeyId": str,
        "PrincipalId": str,
        "UserName": str,
        "UserType": str,
    },
    total=False,
)

AccountDetailTypeDef = TypedDict(
    "AccountDetailTypeDef",
    {
        "AccountId": str,
        "Email": str,
    },
)

FreeTrialFeatureConfigurationResultTypeDef = TypedDict(
    "FreeTrialFeatureConfigurationResultTypeDef",
    {
        "Name": FreeTrialFeatureResultType,
        "FreeTrialDaysRemaining": int,
    },
    total=False,
)

BlockPublicAccessTypeDef = TypedDict(
    "BlockPublicAccessTypeDef",
    {
        "IgnorePublicAcls": bool,
        "RestrictPublicBuckets": bool,
        "BlockPublicAcls": bool,
        "BlockPublicPolicy": bool,
    },
    total=False,
)

DnsRequestActionTypeDef = TypedDict(
    "DnsRequestActionTypeDef",
    {
        "Domain": str,
        "Protocol": str,
        "Blocked": bool,
    },
    total=False,
)

AddonDetailsTypeDef = TypedDict(
    "AddonDetailsTypeDef",
    {
        "AddonVersion": str,
        "AddonStatus": str,
    },
    total=False,
)

AdminAccountTypeDef = TypedDict(
    "AdminAccountTypeDef",
    {
        "AdminAccountId": str,
        "AdminStatus": AdminStatusType,
    },
    total=False,
)

AdministratorTypeDef = TypedDict(
    "AdministratorTypeDef",
    {
        "AccountId": str,
        "InvitationId": str,
        "RelationshipStatus": str,
        "InvitedAt": str,
    },
    total=False,
)

ArchiveFindingsRequestRequestTypeDef = TypedDict(
    "ArchiveFindingsRequestRequestTypeDef",
    {
        "DetectorId": str,
        "FindingIds": Sequence[str],
    },
)

DomainDetailsTypeDef = TypedDict(
    "DomainDetailsTypeDef",
    {
        "Domain": str,
    },
    total=False,
)

RemoteAccountDetailsTypeDef = TypedDict(
    "RemoteAccountDetailsTypeDef",
    {
        "AccountId": str,
        "Affiliated": bool,
    },
    total=False,
)

BucketPolicyTypeDef = TypedDict(
    "BucketPolicyTypeDef",
    {
        "AllowsPublicReadAccess": bool,
        "AllowsPublicWriteAccess": bool,
    },
    total=False,
)

CityTypeDef = TypedDict(
    "CityTypeDef",
    {
        "CityName": str,
    },
    total=False,
)

CloudTrailConfigurationResultTypeDef = TypedDict(
    "CloudTrailConfigurationResultTypeDef",
    {
        "Status": DataSourceStatusType,
    },
)

ConditionTypeDef = TypedDict(
    "ConditionTypeDef",
    {
        "Eq": Sequence[str],
        "Neq": Sequence[str],
        "Gt": int,
        "Gte": int,
        "Lt": int,
        "Lte": int,
        "Equals": Sequence[str],
        "NotEquals": Sequence[str],
        "GreaterThan": int,
        "GreaterThanOrEqual": int,
        "LessThan": int,
        "LessThanOrEqual": int,
    },
    total=False,
)

SecurityContextTypeDef = TypedDict(
    "SecurityContextTypeDef",
    {
        "Privileged": bool,
    },
    total=False,
)

VolumeMountTypeDef = TypedDict(
    "VolumeMountTypeDef",
    {
        "Name": str,
        "MountPath": str,
    },
    total=False,
)

CountryTypeDef = TypedDict(
    "CountryTypeDef",
    {
        "CountryCode": str,
        "CountryName": str,
    },
    total=False,
)

CoverageFilterConditionTypeDef = TypedDict(
    "CoverageFilterConditionTypeDef",
    {
        "Equals": Sequence[str],
        "NotEquals": Sequence[str],
    },
    total=False,
)

CoverageSortCriteriaTypeDef = TypedDict(
    "CoverageSortCriteriaTypeDef",
    {
        "AttributeName": CoverageSortKeyType,
        "OrderBy": OrderByType,
    },
    total=False,
)

CoverageStatisticsTypeDef = TypedDict(
    "CoverageStatisticsTypeDef",
    {
        "CountByResourceType": Dict[Literal["EKS"], int],
        "CountByCoverageStatus": Dict[CoverageStatusType, int],
    },
    total=False,
)

ResponseMetadataTypeDef = TypedDict(
    "ResponseMetadataTypeDef",
    {
        "RequestId": str,
        "HostId": str,
        "HTTPStatusCode": int,
        "HTTPHeaders": Dict[str, str],
        "RetryAttempts": int,
    },
)

_RequiredCreateIPSetRequestRequestTypeDef = TypedDict(
    "_RequiredCreateIPSetRequestRequestTypeDef",
    {
        "DetectorId": str,
        "Name": str,
        "Format": IpSetFormatType,
        "Location": str,
        "Activate": bool,
    },
)
_OptionalCreateIPSetRequestRequestTypeDef = TypedDict(
    "_OptionalCreateIPSetRequestRequestTypeDef",
    {
        "ClientToken": str,
        "Tags": Mapping[str, str],
    },
    total=False,
)


class CreateIPSetRequestRequestTypeDef(
    _RequiredCreateIPSetRequestRequestTypeDef, _OptionalCreateIPSetRequestRequestTypeDef
):
    pass


UnprocessedAccountTypeDef = TypedDict(
    "UnprocessedAccountTypeDef",
    {
        "AccountId": str,
        "Result": str,
    },
)

DestinationPropertiesTypeDef = TypedDict(
    "DestinationPropertiesTypeDef",
    {
        "DestinationArn": str,
        "KmsKeyArn": str,
    },
    total=False,
)

_RequiredCreateSampleFindingsRequestRequestTypeDef = TypedDict(
    "_RequiredCreateSampleFindingsRequestRequestTypeDef",
    {
        "DetectorId": str,
    },
)
_OptionalCreateSampleFindingsRequestRequestTypeDef = TypedDict(
    "_OptionalCreateSampleFindingsRequestRequestTypeDef",
    {
        "FindingTypes": Sequence[str],
    },
    total=False,
)


class CreateSampleFindingsRequestRequestTypeDef(
    _RequiredCreateSampleFindingsRequestRequestTypeDef,
    _OptionalCreateSampleFindingsRequestRequestTypeDef,
):
    pass


_RequiredCreateThreatIntelSetRequestRequestTypeDef = TypedDict(
    "_RequiredCreateThreatIntelSetRequestRequestTypeDef",
    {
        "DetectorId": str,
        "Name": str,
        "Format": ThreatIntelSetFormatType,
        "Location": str,
        "Activate": bool,
    },
)
_OptionalCreateThreatIntelSetRequestRequestTypeDef = TypedDict(
    "_OptionalCreateThreatIntelSetRequestRequestTypeDef",
    {
        "ClientToken": str,
        "Tags": Mapping[str, str],
    },
    total=False,
)


class CreateThreatIntelSetRequestRequestTypeDef(
    _RequiredCreateThreatIntelSetRequestRequestTypeDef,
    _OptionalCreateThreatIntelSetRequestRequestTypeDef,
):
    pass


DNSLogsConfigurationResultTypeDef = TypedDict(
    "DNSLogsConfigurationResultTypeDef",
    {
        "Status": DataSourceStatusType,
    },
)

FlowLogsConfigurationResultTypeDef = TypedDict(
    "FlowLogsConfigurationResultTypeDef",
    {
        "Status": DataSourceStatusType,
    },
)

S3LogsConfigurationResultTypeDef = TypedDict(
    "S3LogsConfigurationResultTypeDef",
    {
        "Status": DataSourceStatusType,
    },
)

S3LogsConfigurationTypeDef = TypedDict(
    "S3LogsConfigurationTypeDef",
    {
        "Enable": bool,
    },
)

DataSourceFreeTrialTypeDef = TypedDict(
    "DataSourceFreeTrialTypeDef",
    {
        "FreeTrialDaysRemaining": int,
    },
    total=False,
)

DeclineInvitationsRequestRequestTypeDef = TypedDict(
    "DeclineInvitationsRequestRequestTypeDef",
    {
        "AccountIds": Sequence[str],
    },
)

DefaultServerSideEncryptionTypeDef = TypedDict(
    "DefaultServerSideEncryptionTypeDef",
    {
        "EncryptionType": str,
        "KmsMasterKeyArn": str,
    },
    total=False,
)

DeleteDetectorRequestRequestTypeDef = TypedDict(
    "DeleteDetectorRequestRequestTypeDef",
    {
        "DetectorId": str,
    },
)

DeleteFilterRequestRequestTypeDef = TypedDict(
    "DeleteFilterRequestRequestTypeDef",
    {
        "DetectorId": str,
        "FilterName": str,
    },
)

DeleteIPSetRequestRequestTypeDef = TypedDict(
    "DeleteIPSetRequestRequestTypeDef",
    {
        "DetectorId": str,
        "IpSetId": str,
    },
)

DeleteInvitationsRequestRequestTypeDef = TypedDict(
    "DeleteInvitationsRequestRequestTypeDef",
    {
        "AccountIds": Sequence[str],
    },
)

DeleteMembersRequestRequestTypeDef = TypedDict(
    "DeleteMembersRequestRequestTypeDef",
    {
        "DetectorId": str,
        "AccountIds": Sequence[str],
    },
)

DeletePublishingDestinationRequestRequestTypeDef = TypedDict(
    "DeletePublishingDestinationRequestRequestTypeDef",
    {
        "DetectorId": str,
        "DestinationId": str,
    },
)

DeleteThreatIntelSetRequestRequestTypeDef = TypedDict(
    "DeleteThreatIntelSetRequestRequestTypeDef",
    {
        "DetectorId": str,
        "ThreatIntelSetId": str,
    },
)

PaginatorConfigTypeDef = TypedDict(
    "PaginatorConfigTypeDef",
    {
        "MaxItems": int,
        "PageSize": int,
        "StartingToken": str,
    },
    total=False,
)

SortCriteriaTypeDef = TypedDict(
    "SortCriteriaTypeDef",
    {
        "AttributeName": str,
        "OrderBy": OrderByType,
    },
    total=False,
)

_RequiredDescribeOrganizationConfigurationRequestRequestTypeDef = TypedDict(
    "_RequiredDescribeOrganizationConfigurationRequestRequestTypeDef",
    {
        "DetectorId": str,
    },
)
_OptionalDescribeOrganizationConfigurationRequestRequestTypeDef = TypedDict(
    "_OptionalDescribeOrganizationConfigurationRequestRequestTypeDef",
    {
        "MaxResults": int,
        "NextToken": str,
    },
    total=False,
)


class DescribeOrganizationConfigurationRequestRequestTypeDef(
    _RequiredDescribeOrganizationConfigurationRequestRequestTypeDef,
    _OptionalDescribeOrganizationConfigurationRequestRequestTypeDef,
):
    pass


DescribePublishingDestinationRequestRequestTypeDef = TypedDict(
    "DescribePublishingDestinationRequestRequestTypeDef",
    {
        "DetectorId": str,
        "DestinationId": str,
    },
)

DestinationTypeDef = TypedDict(
    "DestinationTypeDef",
    {
        "DestinationId": str,
        "DestinationType": Literal["S3"],
        "Status": PublishingStatusType,
    },
)

DetectorAdditionalConfigurationResultTypeDef = TypedDict(
    "DetectorAdditionalConfigurationResultTypeDef",
    {
        "Name": Literal["EKS_ADDON_MANAGEMENT"],
        "Status": FeatureStatusType,
        "UpdatedAt": datetime,
    },
    total=False,
)

DetectorAdditionalConfigurationTypeDef = TypedDict(
    "DetectorAdditionalConfigurationTypeDef",
    {
        "Name": Literal["EKS_ADDON_MANAGEMENT"],
        "Status": FeatureStatusType,
    },
    total=False,
)

DisableOrganizationAdminAccountRequestRequestTypeDef = TypedDict(
    "DisableOrganizationAdminAccountRequestRequestTypeDef",
    {
        "AdminAccountId": str,
    },
)

DisassociateFromAdministratorAccountRequestRequestTypeDef = TypedDict(
    "DisassociateFromAdministratorAccountRequestRequestTypeDef",
    {
        "DetectorId": str,
    },
)

DisassociateFromMasterAccountRequestRequestTypeDef = TypedDict(
    "DisassociateFromMasterAccountRequestRequestTypeDef",
    {
        "DetectorId": str,
    },
)

DisassociateMembersRequestRequestTypeDef = TypedDict(
    "DisassociateMembersRequestRequestTypeDef",
    {
        "DetectorId": str,
        "AccountIds": Sequence[str],
    },
)

VolumeDetailTypeDef = TypedDict(
    "VolumeDetailTypeDef",
    {
        "VolumeArn": str,
        "VolumeType": str,
        "DeviceName": str,
        "VolumeSizeInGB": int,
        "EncryptionType": str,
        "SnapshotArn": str,
        "KmsKeyArn": str,
    },
    total=False,
)

EbsVolumesResultTypeDef = TypedDict(
    "EbsVolumesResultTypeDef",
    {
        "Status": DataSourceStatusType,
        "Reason": str,
    },
    total=False,
)

TagTypeDef = TypedDict(
    "TagTypeDef",
    {
        "Key": str,
        "Value": str,
    },
    total=False,
)

EnableOrganizationAdminAccountRequestRequestTypeDef = TypedDict(
    "EnableOrganizationAdminAccountRequestRequestTypeDef",
    {
        "AdminAccountId": str,
    },
)

ThreatIntelligenceDetailTypeDef = TypedDict(
    "ThreatIntelligenceDetailTypeDef",
    {
        "ThreatListName": str,
        "ThreatNames": List[str],
    },
    total=False,
)

FilterConditionTypeDef = TypedDict(
    "FilterConditionTypeDef",
    {
        "EqualsValue": str,
        "GreaterThan": int,
        "LessThan": int,
    },
    total=False,
)

FindingStatisticsTypeDef = TypedDict(
    "FindingStatisticsTypeDef",
    {
        "CountBySeverity": Dict[str, int],
    },
    total=False,
)

GeoLocationTypeDef = TypedDict(
    "GeoLocationTypeDef",
    {
        "Lat": float,
        "Lon": float,
    },
    total=False,
)

GetAdministratorAccountRequestRequestTypeDef = TypedDict(
    "GetAdministratorAccountRequestRequestTypeDef",
    {
        "DetectorId": str,
    },
)

GetDetectorRequestRequestTypeDef = TypedDict(
    "GetDetectorRequestRequestTypeDef",
    {
        "DetectorId": str,
    },
)

GetFilterRequestRequestTypeDef = TypedDict(
    "GetFilterRequestRequestTypeDef",
    {
        "DetectorId": str,
        "FilterName": str,
    },
)

GetIPSetRequestRequestTypeDef = TypedDict(
    "GetIPSetRequestRequestTypeDef",
    {
        "DetectorId": str,
        "IpSetId": str,
    },
)

GetMalwareScanSettingsRequestRequestTypeDef = TypedDict(
    "GetMalwareScanSettingsRequestRequestTypeDef",
    {
        "DetectorId": str,
    },
)

GetMasterAccountRequestRequestTypeDef = TypedDict(
    "GetMasterAccountRequestRequestTypeDef",
    {
        "DetectorId": str,
    },
)

MasterTypeDef = TypedDict(
    "MasterTypeDef",
    {
        "AccountId": str,
        "InvitationId": str,
        "RelationshipStatus": str,
        "InvitedAt": str,
    },
    total=False,
)

GetMemberDetectorsRequestRequestTypeDef = TypedDict(
    "GetMemberDetectorsRequestRequestTypeDef",
    {
        "DetectorId": str,
        "AccountIds": Sequence[str],
    },
)

GetMembersRequestRequestTypeDef = TypedDict(
    "GetMembersRequestRequestTypeDef",
    {
        "DetectorId": str,
        "AccountIds": Sequence[str],
    },
)

_RequiredMemberTypeDef = TypedDict(
    "_RequiredMemberTypeDef",
    {
        "AccountId": str,
        "MasterId": str,
        "Email": str,
        "RelationshipStatus": str,
        "UpdatedAt": str,
    },
)
_OptionalMemberTypeDef = TypedDict(
    "_OptionalMemberTypeDef",
    {
        "DetectorId": str,
        "InvitedAt": str,
        "AdministratorId": str,
    },
    total=False,
)


class MemberTypeDef(_RequiredMemberTypeDef, _OptionalMemberTypeDef):
    pass


_RequiredGetRemainingFreeTrialDaysRequestRequestTypeDef = TypedDict(
    "_RequiredGetRemainingFreeTrialDaysRequestRequestTypeDef",
    {
        "DetectorId": str,
    },
)
_OptionalGetRemainingFreeTrialDaysRequestRequestTypeDef = TypedDict(
    "_OptionalGetRemainingFreeTrialDaysRequestRequestTypeDef",
    {
        "AccountIds": Sequence[str],
    },
    total=False,
)


class GetRemainingFreeTrialDaysRequestRequestTypeDef(
    _RequiredGetRemainingFreeTrialDaysRequestRequestTypeDef,
    _OptionalGetRemainingFreeTrialDaysRequestRequestTypeDef,
):
    pass


GetThreatIntelSetRequestRequestTypeDef = TypedDict(
    "GetThreatIntelSetRequestRequestTypeDef",
    {
        "DetectorId": str,
        "ThreatIntelSetId": str,
    },
)

UsageCriteriaTypeDef = TypedDict(
    "UsageCriteriaTypeDef",
    {
        "AccountIds": Sequence[str],
        "DataSources": Sequence[DataSourceType],
        "Resources": Sequence[str],
        "Features": Sequence[UsageFeatureType],
    },
    total=False,
)

HighestSeverityThreatDetailsTypeDef = TypedDict(
    "HighestSeverityThreatDetailsTypeDef",
    {
        "Severity": str,
        "ThreatName": str,
        "Count": int,
    },
    total=False,
)

HostPathTypeDef = TypedDict(
    "HostPathTypeDef",
    {
        "Path": str,
    },
    total=False,
)

IamInstanceProfileTypeDef = TypedDict(
    "IamInstanceProfileTypeDef",
    {
        "Arn": str,
        "Id": str,
    },
    total=False,
)

ProductCodeTypeDef = TypedDict(
    "ProductCodeTypeDef",
    {
        "Code": str,
        "ProductType": str,
    },
    total=False,
)

InvitationTypeDef = TypedDict(
    "InvitationTypeDef",
    {
        "AccountId": str,
        "InvitationId": str,
        "RelationshipStatus": str,
        "InvitedAt": str,
    },
    total=False,
)

_RequiredInviteMembersRequestRequestTypeDef = TypedDict(
    "_RequiredInviteMembersRequestRequestTypeDef",
    {
        "DetectorId": str,
        "AccountIds": Sequence[str],
    },
)
_OptionalInviteMembersRequestRequestTypeDef = TypedDict(
    "_OptionalInviteMembersRequestRequestTypeDef",
    {
        "DisableEmailNotification": bool,
        "Message": str,
    },
    total=False,
)


class InviteMembersRequestRequestTypeDef(
    _RequiredInviteMembersRequestRequestTypeDef, _OptionalInviteMembersRequestRequestTypeDef
):
    pass


KubernetesAuditLogsConfigurationResultTypeDef = TypedDict(
    "KubernetesAuditLogsConfigurationResultTypeDef",
    {
        "Status": DataSourceStatusType,
    },
)

KubernetesAuditLogsConfigurationTypeDef = TypedDict(
    "KubernetesAuditLogsConfigurationTypeDef",
    {
        "Enable": bool,
    },
)

KubernetesUserDetailsTypeDef = TypedDict(
    "KubernetesUserDetailsTypeDef",
    {
        "Username": str,
        "Uid": str,
        "Groups": List[str],
    },
    total=False,
)

LineageObjectTypeDef = TypedDict(
    "LineageObjectTypeDef",
    {
        "StartTime": datetime,
        "NamespacePid": int,
        "UserId": int,
        "Name": str,
        "Pid": int,
        "Uuid": str,
        "ExecutablePath": str,
        "Euid": int,
        "ParentUuid": str,
    },
    total=False,
)

ListDetectorsRequestRequestTypeDef = TypedDict(
    "ListDetectorsRequestRequestTypeDef",
    {
        "MaxResults": int,
        "NextToken": str,
    },
    total=False,
)

_RequiredListFiltersRequestRequestTypeDef = TypedDict(
    "_RequiredListFiltersRequestRequestTypeDef",
    {
        "DetectorId": str,
    },
)
_OptionalListFiltersRequestRequestTypeDef = TypedDict(
    "_OptionalListFiltersRequestRequestTypeDef",
    {
        "MaxResults": int,
        "NextToken": str,
    },
    total=False,
)


class ListFiltersRequestRequestTypeDef(
    _RequiredListFiltersRequestRequestTypeDef, _OptionalListFiltersRequestRequestTypeDef
):
    pass


_RequiredListIPSetsRequestRequestTypeDef = TypedDict(
    "_RequiredListIPSetsRequestRequestTypeDef",
    {
        "DetectorId": str,
    },
)
_OptionalListIPSetsRequestRequestTypeDef = TypedDict(
    "_OptionalListIPSetsRequestRequestTypeDef",
    {
        "MaxResults": int,
        "NextToken": str,
    },
    total=False,
)


class ListIPSetsRequestRequestTypeDef(
    _RequiredListIPSetsRequestRequestTypeDef, _OptionalListIPSetsRequestRequestTypeDef
):
    pass


ListInvitationsRequestRequestTypeDef = TypedDict(
    "ListInvitationsRequestRequestTypeDef",
    {
        "MaxResults": int,
        "NextToken": str,
    },
    total=False,
)

_RequiredListMembersRequestRequestTypeDef = TypedDict(
    "_RequiredListMembersRequestRequestTypeDef",
    {
        "DetectorId": str,
    },
)
_OptionalListMembersRequestRequestTypeDef = TypedDict(
    "_OptionalListMembersRequestRequestTypeDef",
    {
        "MaxResults": int,
        "NextToken": str,
        "OnlyAssociated": str,
    },
    total=False,
)


class ListMembersRequestRequestTypeDef(
    _RequiredListMembersRequestRequestTypeDef, _OptionalListMembersRequestRequestTypeDef
):
    pass


ListOrganizationAdminAccountsRequestRequestTypeDef = TypedDict(
    "ListOrganizationAdminAccountsRequestRequestTypeDef",
    {
        "MaxResults": int,
        "NextToken": str,
    },
    total=False,
)

_RequiredListPublishingDestinationsRequestRequestTypeDef = TypedDict(
    "_RequiredListPublishingDestinationsRequestRequestTypeDef",
    {
        "DetectorId": str,
    },
)
_OptionalListPublishingDestinationsRequestRequestTypeDef = TypedDict(
    "_OptionalListPublishingDestinationsRequestRequestTypeDef",
    {
        "MaxResults": int,
        "NextToken": str,
    },
    total=False,
)


class ListPublishingDestinationsRequestRequestTypeDef(
    _RequiredListPublishingDestinationsRequestRequestTypeDef,
    _OptionalListPublishingDestinationsRequestRequestTypeDef,
):
    pass


ListTagsForResourceRequestRequestTypeDef = TypedDict(
    "ListTagsForResourceRequestRequestTypeDef",
    {
        "ResourceArn": str,
    },
)

_RequiredListThreatIntelSetsRequestRequestTypeDef = TypedDict(
    "_RequiredListThreatIntelSetsRequestRequestTypeDef",
    {
        "DetectorId": str,
    },
)
_OptionalListThreatIntelSetsRequestRequestTypeDef = TypedDict(
    "_OptionalListThreatIntelSetsRequestRequestTypeDef",
    {
        "MaxResults": int,
        "NextToken": str,
    },
    total=False,
)


class ListThreatIntelSetsRequestRequestTypeDef(
    _RequiredListThreatIntelSetsRequestRequestTypeDef,
    _OptionalListThreatIntelSetsRequestRequestTypeDef,
):
    pass


LocalIpDetailsTypeDef = TypedDict(
    "LocalIpDetailsTypeDef",
    {
        "IpAddressV4": str,
    },
    total=False,
)

LocalPortDetailsTypeDef = TypedDict(
    "LocalPortDetailsTypeDef",
    {
        "Port": int,
        "PortName": str,
    },
    total=False,
)

LoginAttributeTypeDef = TypedDict(
    "LoginAttributeTypeDef",
    {
        "User": str,
        "Application": str,
        "FailedLoginAttempts": int,
        "SuccessfulLoginAttempts": int,
    },
    total=False,
)

ScanEc2InstanceWithFindingsTypeDef = TypedDict(
    "ScanEc2InstanceWithFindingsTypeDef",
    {
        "EbsVolumes": bool,
    },
    total=False,
)

MemberAdditionalConfigurationResultTypeDef = TypedDict(
    "MemberAdditionalConfigurationResultTypeDef",
    {
        "Name": Literal["EKS_ADDON_MANAGEMENT"],
        "Status": FeatureStatusType,
        "UpdatedAt": datetime,
    },
    total=False,
)

MemberAdditionalConfigurationTypeDef = TypedDict(
    "MemberAdditionalConfigurationTypeDef",
    {
        "Name": Literal["EKS_ADDON_MANAGEMENT"],
        "Status": FeatureStatusType,
    },
    total=False,
)

RemotePortDetailsTypeDef = TypedDict(
    "RemotePortDetailsTypeDef",
    {
        "Port": int,
        "PortName": str,
    },
    total=False,
)

PrivateIpAddressDetailsTypeDef = TypedDict(
    "PrivateIpAddressDetailsTypeDef",
    {
        "PrivateDnsName": str,
        "PrivateIpAddress": str,
    },
    total=False,
)

SecurityGroupTypeDef = TypedDict(
    "SecurityGroupTypeDef",
    {
        "GroupId": str,
        "GroupName": str,
    },
    total=False,
)

OrganizationAdditionalConfigurationResultTypeDef = TypedDict(
    "OrganizationAdditionalConfigurationResultTypeDef",
    {
        "Name": Literal["EKS_ADDON_MANAGEMENT"],
        "AutoEnable": OrgFeatureStatusType,
    },
    total=False,
)

OrganizationAdditionalConfigurationTypeDef = TypedDict(
    "OrganizationAdditionalConfigurationTypeDef",
    {
        "Name": Literal["EKS_ADDON_MANAGEMENT"],
        "AutoEnable": OrgFeatureStatusType,
    },
    total=False,
)

OrganizationS3LogsConfigurationResultTypeDef = TypedDict(
    "OrganizationS3LogsConfigurationResultTypeDef",
    {
        "AutoEnable": bool,
    },
)

OrganizationS3LogsConfigurationTypeDef = TypedDict(
    "OrganizationS3LogsConfigurationTypeDef",
    {
        "AutoEnable": bool,
    },
)

OrganizationEbsVolumesResultTypeDef = TypedDict(
    "OrganizationEbsVolumesResultTypeDef",
    {
        "AutoEnable": bool,
    },
    total=False,
)

OrganizationEbsVolumesTypeDef = TypedDict(
    "OrganizationEbsVolumesTypeDef",
    {
        "AutoEnable": bool,
    },
    total=False,
)

OrganizationKubernetesAuditLogsConfigurationResultTypeDef = TypedDict(
    "OrganizationKubernetesAuditLogsConfigurationResultTypeDef",
    {
        "AutoEnable": bool,
    },
)

OrganizationKubernetesAuditLogsConfigurationTypeDef = TypedDict(
    "OrganizationKubernetesAuditLogsConfigurationTypeDef",
    {
        "AutoEnable": bool,
    },
)

OrganizationTypeDef = TypedDict(
    "OrganizationTypeDef",
    {
        "Asn": str,
        "AsnOrg": str,
        "Isp": str,
        "Org": str,
    },
    total=False,
)

OwnerTypeDef = TypedDict(
    "OwnerTypeDef",
    {
        "Id": str,
    },
    total=False,
)

RdsDbUserDetailsTypeDef = TypedDict(
    "RdsDbUserDetailsTypeDef",
    {
        "User": str,
        "Application": str,
        "Database": str,
        "Ssl": str,
        "AuthMethod": str,
    },
    total=False,
)

ResourceDetailsTypeDef = TypedDict(
    "ResourceDetailsTypeDef",
    {
        "InstanceArn": str,
    },
    total=False,
)

_RequiredScanConditionPairTypeDef = TypedDict(
    "_RequiredScanConditionPairTypeDef",
    {
        "Key": str,
    },
)
_OptionalScanConditionPairTypeDef = TypedDict(
    "_OptionalScanConditionPairTypeDef",
    {
        "Value": str,
    },
    total=False,
)


class ScanConditionPairTypeDef(
    _RequiredScanConditionPairTypeDef, _OptionalScanConditionPairTypeDef
):
    pass


ScannedItemCountTypeDef = TypedDict(
    "ScannedItemCountTypeDef",
    {
        "TotalGb": int,
        "Files": int,
        "Volumes": int,
    },
    total=False,
)

ThreatsDetectedItemCountTypeDef = TypedDict(
    "ThreatsDetectedItemCountTypeDef",
    {
        "Files": int,
    },
    total=False,
)

ScanFilePathTypeDef = TypedDict(
    "ScanFilePathTypeDef",
    {
        "FilePath": str,
        "VolumeArn": str,
        "Hash": str,
        "FileName": str,
    },
    total=False,
)

ScanResultDetailsTypeDef = TypedDict(
    "ScanResultDetailsTypeDef",
    {
        "ScanResult": ScanResultType,
    },
    total=False,
)

TriggerDetailsTypeDef = TypedDict(
    "TriggerDetailsTypeDef",
    {
        "GuardDutyFindingId": str,
        "Description": str,
    },
    total=False,
)

ServiceAdditionalInfoTypeDef = TypedDict(
    "ServiceAdditionalInfoTypeDef",
    {
        "Value": str,
        "Type": str,
    },
    total=False,
)

StartMonitoringMembersRequestRequestTypeDef = TypedDict(
    "StartMonitoringMembersRequestRequestTypeDef",
    {
        "DetectorId": str,
        "AccountIds": Sequence[str],
    },
)

StopMonitoringMembersRequestRequestTypeDef = TypedDict(
    "StopMonitoringMembersRequestRequestTypeDef",
    {
        "DetectorId": str,
        "AccountIds": Sequence[str],
    },
)

TagResourceRequestRequestTypeDef = TypedDict(
    "TagResourceRequestRequestTypeDef",
    {
        "ResourceArn": str,
        "Tags": Mapping[str, str],
    },
)

TotalTypeDef = TypedDict(
    "TotalTypeDef",
    {
        "Amount": str,
        "Unit": str,
    },
    total=False,
)

UnarchiveFindingsRequestRequestTypeDef = TypedDict(
    "UnarchiveFindingsRequestRequestTypeDef",
    {
        "DetectorId": str,
        "FindingIds": Sequence[str],
    },
)

UntagResourceRequestRequestTypeDef = TypedDict(
    "UntagResourceRequestRequestTypeDef",
    {
        "ResourceArn": str,
        "TagKeys": Sequence[str],
    },
)

_RequiredUpdateFindingsFeedbackRequestRequestTypeDef = TypedDict(
    "_RequiredUpdateFindingsFeedbackRequestRequestTypeDef",
    {
        "DetectorId": str,
        "FindingIds": Sequence[str],
        "Feedback": FeedbackType,
    },
)
_OptionalUpdateFindingsFeedbackRequestRequestTypeDef = TypedDict(
    "_OptionalUpdateFindingsFeedbackRequestRequestTypeDef",
    {
        "Comments": str,
    },
    total=False,
)


class UpdateFindingsFeedbackRequestRequestTypeDef(
    _RequiredUpdateFindingsFeedbackRequestRequestTypeDef,
    _OptionalUpdateFindingsFeedbackRequestRequestTypeDef,
):
    pass


_RequiredUpdateIPSetRequestRequestTypeDef = TypedDict(
    "_RequiredUpdateIPSetRequestRequestTypeDef",
    {
        "DetectorId": str,
        "IpSetId": str,
    },
)
_OptionalUpdateIPSetRequestRequestTypeDef = TypedDict(
    "_OptionalUpdateIPSetRequestRequestTypeDef",
    {
        "Name": str,
        "Location": str,
        "Activate": bool,
    },
    total=False,
)


class UpdateIPSetRequestRequestTypeDef(
    _RequiredUpdateIPSetRequestRequestTypeDef, _OptionalUpdateIPSetRequestRequestTypeDef
):
    pass


_RequiredUpdateThreatIntelSetRequestRequestTypeDef = TypedDict(
    "_RequiredUpdateThreatIntelSetRequestRequestTypeDef",
    {
        "DetectorId": str,
        "ThreatIntelSetId": str,
    },
)
_OptionalUpdateThreatIntelSetRequestRequestTypeDef = TypedDict(
    "_OptionalUpdateThreatIntelSetRequestRequestTypeDef",
    {
        "Name": str,
        "Location": str,
        "Activate": bool,
    },
    total=False,
)


class UpdateThreatIntelSetRequestRequestTypeDef(
    _RequiredUpdateThreatIntelSetRequestRequestTypeDef,
    _OptionalUpdateThreatIntelSetRequestRequestTypeDef,
):
    pass


CreateMembersRequestRequestTypeDef = TypedDict(
    "CreateMembersRequestRequestTypeDef",
    {
        "DetectorId": str,
        "AccountDetails": Sequence[AccountDetailTypeDef],
    },
)

AccountLevelPermissionsTypeDef = TypedDict(
    "AccountLevelPermissionsTypeDef",
    {
        "BlockPublicAccess": BlockPublicAccessTypeDef,
    },
    total=False,
)

CoverageEksClusterDetailsTypeDef = TypedDict(
    "CoverageEksClusterDetailsTypeDef",
    {
        "ClusterName": str,
        "CoveredNodes": int,
        "CompatibleNodes": int,
        "AddonDetails": AddonDetailsTypeDef,
    },
    total=False,
)

BucketLevelPermissionsTypeDef = TypedDict(
    "BucketLevelPermissionsTypeDef",
    {
        "AccessControlList": AccessControlListTypeDef,
        "BucketPolicy": BucketPolicyTypeDef,
        "BlockPublicAccess": BlockPublicAccessTypeDef,
    },
    total=False,
)

FindingCriteriaTypeDef = TypedDict(
    "FindingCriteriaTypeDef",
    {
        "Criterion": Mapping[str, ConditionTypeDef],
    },
    total=False,
)

ContainerTypeDef = TypedDict(
    "ContainerTypeDef",
    {
        "ContainerRuntime": str,
        "Id": str,
        "Name": str,
        "Image": str,
        "ImagePrefix": str,
        "VolumeMounts": List[VolumeMountTypeDef],
        "SecurityContext": SecurityContextTypeDef,
    },
    total=False,
)

CoverageFilterCriterionTypeDef = TypedDict(
    "CoverageFilterCriterionTypeDef",
    {
        "CriterionKey": CoverageFilterCriterionKeyType,
        "FilterCondition": CoverageFilterConditionTypeDef,
    },
    total=False,
)

CreateFilterResponseTypeDef = TypedDict(
    "CreateFilterResponseTypeDef",
    {
        "Name": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

CreateIPSetResponseTypeDef = TypedDict(
    "CreateIPSetResponseTypeDef",
    {
        "IpSetId": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

CreatePublishingDestinationResponseTypeDef = TypedDict(
    "CreatePublishingDestinationResponseTypeDef",
    {
        "DestinationId": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

CreateThreatIntelSetResponseTypeDef = TypedDict(
    "CreateThreatIntelSetResponseTypeDef",
    {
        "ThreatIntelSetId": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

GetAdministratorAccountResponseTypeDef = TypedDict(
    "GetAdministratorAccountResponseTypeDef",
    {
        "Administrator": AdministratorTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

GetCoverageStatisticsResponseTypeDef = TypedDict(
    "GetCoverageStatisticsResponseTypeDef",
    {
        "CoverageStatistics": CoverageStatisticsTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

GetIPSetResponseTypeDef = TypedDict(
    "GetIPSetResponseTypeDef",
    {
        "Name": str,
        "Format": IpSetFormatType,
        "Location": str,
        "Status": IpSetStatusType,
        "Tags": Dict[str, str],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

GetInvitationsCountResponseTypeDef = TypedDict(
    "GetInvitationsCountResponseTypeDef",
    {
        "InvitationsCount": int,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

GetThreatIntelSetResponseTypeDef = TypedDict(
    "GetThreatIntelSetResponseTypeDef",
    {
        "Name": str,
        "Format": ThreatIntelSetFormatType,
        "Location": str,
        "Status": ThreatIntelSetStatusType,
        "Tags": Dict[str, str],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ListDetectorsResponseTypeDef = TypedDict(
    "ListDetectorsResponseTypeDef",
    {
        "DetectorIds": List[str],
        "NextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ListFiltersResponseTypeDef = TypedDict(
    "ListFiltersResponseTypeDef",
    {
        "FilterNames": List[str],
        "NextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ListFindingsResponseTypeDef = TypedDict(
    "ListFindingsResponseTypeDef",
    {
        "FindingIds": List[str],
        "NextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ListIPSetsResponseTypeDef = TypedDict(
    "ListIPSetsResponseTypeDef",
    {
        "IpSetIds": List[str],
        "NextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ListOrganizationAdminAccountsResponseTypeDef = TypedDict(
    "ListOrganizationAdminAccountsResponseTypeDef",
    {
        "AdminAccounts": List[AdminAccountTypeDef],
        "NextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ListTagsForResourceResponseTypeDef = TypedDict(
    "ListTagsForResourceResponseTypeDef",
    {
        "Tags": Dict[str, str],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ListThreatIntelSetsResponseTypeDef = TypedDict(
    "ListThreatIntelSetsResponseTypeDef",
    {
        "ThreatIntelSetIds": List[str],
        "NextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

UpdateFilterResponseTypeDef = TypedDict(
    "UpdateFilterResponseTypeDef",
    {
        "Name": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

CreateMembersResponseTypeDef = TypedDict(
    "CreateMembersResponseTypeDef",
    {
        "UnprocessedAccounts": List[UnprocessedAccountTypeDef],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

DeclineInvitationsResponseTypeDef = TypedDict(
    "DeclineInvitationsResponseTypeDef",
    {
        "UnprocessedAccounts": List[UnprocessedAccountTypeDef],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

DeleteInvitationsResponseTypeDef = TypedDict(
    "DeleteInvitationsResponseTypeDef",
    {
        "UnprocessedAccounts": List[UnprocessedAccountTypeDef],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

DeleteMembersResponseTypeDef = TypedDict(
    "DeleteMembersResponseTypeDef",
    {
        "UnprocessedAccounts": List[UnprocessedAccountTypeDef],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

DisassociateMembersResponseTypeDef = TypedDict(
    "DisassociateMembersResponseTypeDef",
    {
        "UnprocessedAccounts": List[UnprocessedAccountTypeDef],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

InviteMembersResponseTypeDef = TypedDict(
    "InviteMembersResponseTypeDef",
    {
        "UnprocessedAccounts": List[UnprocessedAccountTypeDef],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

StartMonitoringMembersResponseTypeDef = TypedDict(
    "StartMonitoringMembersResponseTypeDef",
    {
        "UnprocessedAccounts": List[UnprocessedAccountTypeDef],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

StopMonitoringMembersResponseTypeDef = TypedDict(
    "StopMonitoringMembersResponseTypeDef",
    {
        "UnprocessedAccounts": List[UnprocessedAccountTypeDef],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

UpdateMemberDetectorsResponseTypeDef = TypedDict(
    "UpdateMemberDetectorsResponseTypeDef",
    {
        "UnprocessedAccounts": List[UnprocessedAccountTypeDef],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

_RequiredCreatePublishingDestinationRequestRequestTypeDef = TypedDict(
    "_RequiredCreatePublishingDestinationRequestRequestTypeDef",
    {
        "DetectorId": str,
        "DestinationType": Literal["S3"],
        "DestinationProperties": DestinationPropertiesTypeDef,
    },
)
_OptionalCreatePublishingDestinationRequestRequestTypeDef = TypedDict(
    "_OptionalCreatePublishingDestinationRequestRequestTypeDef",
    {
        "ClientToken": str,
    },
    total=False,
)


class CreatePublishingDestinationRequestRequestTypeDef(
    _RequiredCreatePublishingDestinationRequestRequestTypeDef,
    _OptionalCreatePublishingDestinationRequestRequestTypeDef,
):
    pass


DescribePublishingDestinationResponseTypeDef = TypedDict(
    "DescribePublishingDestinationResponseTypeDef",
    {
        "DestinationId": str,
        "DestinationType": Literal["S3"],
        "Status": PublishingStatusType,
        "PublishingFailureStartTimestamp": int,
        "DestinationProperties": DestinationPropertiesTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

_RequiredUpdatePublishingDestinationRequestRequestTypeDef = TypedDict(
    "_RequiredUpdatePublishingDestinationRequestRequestTypeDef",
    {
        "DetectorId": str,
        "DestinationId": str,
    },
)
_OptionalUpdatePublishingDestinationRequestRequestTypeDef = TypedDict(
    "_OptionalUpdatePublishingDestinationRequestRequestTypeDef",
    {
        "DestinationProperties": DestinationPropertiesTypeDef,
    },
    total=False,
)


class UpdatePublishingDestinationRequestRequestTypeDef(
    _RequiredUpdatePublishingDestinationRequestRequestTypeDef,
    _OptionalUpdatePublishingDestinationRequestRequestTypeDef,
):
    pass


KubernetesDataSourceFreeTrialTypeDef = TypedDict(
    "KubernetesDataSourceFreeTrialTypeDef",
    {
        "AuditLogs": DataSourceFreeTrialTypeDef,
    },
    total=False,
)

MalwareProtectionDataSourceFreeTrialTypeDef = TypedDict(
    "MalwareProtectionDataSourceFreeTrialTypeDef",
    {
        "ScanEc2InstanceWithFindings": DataSourceFreeTrialTypeDef,
    },
    total=False,
)

ListDetectorsRequestListDetectorsPaginateTypeDef = TypedDict(
    "ListDetectorsRequestListDetectorsPaginateTypeDef",
    {
        "PaginationConfig": PaginatorConfigTypeDef,
    },
    total=False,
)

_RequiredListFiltersRequestListFiltersPaginateTypeDef = TypedDict(
    "_RequiredListFiltersRequestListFiltersPaginateTypeDef",
    {
        "DetectorId": str,
    },
)
_OptionalListFiltersRequestListFiltersPaginateTypeDef = TypedDict(
    "_OptionalListFiltersRequestListFiltersPaginateTypeDef",
    {
        "PaginationConfig": PaginatorConfigTypeDef,
    },
    total=False,
)


class ListFiltersRequestListFiltersPaginateTypeDef(
    _RequiredListFiltersRequestListFiltersPaginateTypeDef,
    _OptionalListFiltersRequestListFiltersPaginateTypeDef,
):
    pass


_RequiredListIPSetsRequestListIPSetsPaginateTypeDef = TypedDict(
    "_RequiredListIPSetsRequestListIPSetsPaginateTypeDef",
    {
        "DetectorId": str,
    },
)
_OptionalListIPSetsRequestListIPSetsPaginateTypeDef = TypedDict(
    "_OptionalListIPSetsRequestListIPSetsPaginateTypeDef",
    {
        "PaginationConfig": PaginatorConfigTypeDef,
    },
    total=False,
)


class ListIPSetsRequestListIPSetsPaginateTypeDef(
    _RequiredListIPSetsRequestListIPSetsPaginateTypeDef,
    _OptionalListIPSetsRequestListIPSetsPaginateTypeDef,
):
    pass


ListInvitationsRequestListInvitationsPaginateTypeDef = TypedDict(
    "ListInvitationsRequestListInvitationsPaginateTypeDef",
    {
        "PaginationConfig": PaginatorConfigTypeDef,
    },
    total=False,
)

_RequiredListMembersRequestListMembersPaginateTypeDef = TypedDict(
    "_RequiredListMembersRequestListMembersPaginateTypeDef",
    {
        "DetectorId": str,
    },
)
_OptionalListMembersRequestListMembersPaginateTypeDef = TypedDict(
    "_OptionalListMembersRequestListMembersPaginateTypeDef",
    {
        "OnlyAssociated": str,
        "PaginationConfig": PaginatorConfigTypeDef,
    },
    total=False,
)


class ListMembersRequestListMembersPaginateTypeDef(
    _RequiredListMembersRequestListMembersPaginateTypeDef,
    _OptionalListMembersRequestListMembersPaginateTypeDef,
):
    pass


ListOrganizationAdminAccountsRequestListOrganizationAdminAccountsPaginateTypeDef = TypedDict(
    "ListOrganizationAdminAccountsRequestListOrganizationAdminAccountsPaginateTypeDef",
    {
        "PaginationConfig": PaginatorConfigTypeDef,
    },
    total=False,
)

_RequiredListThreatIntelSetsRequestListThreatIntelSetsPaginateTypeDef = TypedDict(
    "_RequiredListThreatIntelSetsRequestListThreatIntelSetsPaginateTypeDef",
    {
        "DetectorId": str,
    },
)
_OptionalListThreatIntelSetsRequestListThreatIntelSetsPaginateTypeDef = TypedDict(
    "_OptionalListThreatIntelSetsRequestListThreatIntelSetsPaginateTypeDef",
    {
        "PaginationConfig": PaginatorConfigTypeDef,
    },
    total=False,
)


class ListThreatIntelSetsRequestListThreatIntelSetsPaginateTypeDef(
    _RequiredListThreatIntelSetsRequestListThreatIntelSetsPaginateTypeDef,
    _OptionalListThreatIntelSetsRequestListThreatIntelSetsPaginateTypeDef,
):
    pass


_RequiredGetFindingsRequestRequestTypeDef = TypedDict(
    "_RequiredGetFindingsRequestRequestTypeDef",
    {
        "DetectorId": str,
        "FindingIds": Sequence[str],
    },
)
_OptionalGetFindingsRequestRequestTypeDef = TypedDict(
    "_OptionalGetFindingsRequestRequestTypeDef",
    {
        "SortCriteria": SortCriteriaTypeDef,
    },
    total=False,
)


class GetFindingsRequestRequestTypeDef(
    _RequiredGetFindingsRequestRequestTypeDef, _OptionalGetFindingsRequestRequestTypeDef
):
    pass


ListPublishingDestinationsResponseTypeDef = TypedDict(
    "ListPublishingDestinationsResponseTypeDef",
    {
        "Destinations": List[DestinationTypeDef],
        "NextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

DetectorFeatureConfigurationResultTypeDef = TypedDict(
    "DetectorFeatureConfigurationResultTypeDef",
    {
        "Name": DetectorFeatureResultType,
        "Status": FeatureStatusType,
        "UpdatedAt": datetime,
        "AdditionalConfiguration": List[DetectorAdditionalConfigurationResultTypeDef],
    },
    total=False,
)

DetectorFeatureConfigurationTypeDef = TypedDict(
    "DetectorFeatureConfigurationTypeDef",
    {
        "Name": DetectorFeatureType,
        "Status": FeatureStatusType,
        "AdditionalConfiguration": Sequence[DetectorAdditionalConfigurationTypeDef],
    },
    total=False,
)

EbsVolumeDetailsTypeDef = TypedDict(
    "EbsVolumeDetailsTypeDef",
    {
        "ScannedVolumeDetails": List[VolumeDetailTypeDef],
        "SkippedVolumeDetails": List[VolumeDetailTypeDef],
    },
    total=False,
)

ScanEc2InstanceWithFindingsResultTypeDef = TypedDict(
    "ScanEc2InstanceWithFindingsResultTypeDef",
    {
        "EbsVolumes": EbsVolumesResultTypeDef,
    },
    total=False,
)

EksClusterDetailsTypeDef = TypedDict(
    "EksClusterDetailsTypeDef",
    {
        "Name": str,
        "Arn": str,
        "VpcId": str,
        "Status": str,
        "Tags": List[TagTypeDef],
        "CreatedAt": datetime,
    },
    total=False,
)

RdsDbInstanceDetailsTypeDef = TypedDict(
    "RdsDbInstanceDetailsTypeDef",
    {
        "DbInstanceIdentifier": str,
        "Engine": str,
        "EngineVersion": str,
        "DbClusterIdentifier": str,
        "DbInstanceArn": str,
        "Tags": List[TagTypeDef],
    },
    total=False,
)

EvidenceTypeDef = TypedDict(
    "EvidenceTypeDef",
    {
        "ThreatIntelligenceDetails": List[ThreatIntelligenceDetailTypeDef],
    },
    total=False,
)

FilterCriterionTypeDef = TypedDict(
    "FilterCriterionTypeDef",
    {
        "CriterionKey": CriterionKeyType,
        "FilterCondition": FilterConditionTypeDef,
    },
    total=False,
)

GetFindingsStatisticsResponseTypeDef = TypedDict(
    "GetFindingsStatisticsResponseTypeDef",
    {
        "FindingStatistics": FindingStatisticsTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

GetMasterAccountResponseTypeDef = TypedDict(
    "GetMasterAccountResponseTypeDef",
    {
        "Master": MasterTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

GetMembersResponseTypeDef = TypedDict(
    "GetMembersResponseTypeDef",
    {
        "Members": List[MemberTypeDef],
        "UnprocessedAccounts": List[UnprocessedAccountTypeDef],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ListMembersResponseTypeDef = TypedDict(
    "ListMembersResponseTypeDef",
    {
        "Members": List[MemberTypeDef],
        "NextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

_RequiredGetUsageStatisticsRequestRequestTypeDef = TypedDict(
    "_RequiredGetUsageStatisticsRequestRequestTypeDef",
    {
        "DetectorId": str,
        "UsageStatisticType": UsageStatisticTypeType,
        "UsageCriteria": UsageCriteriaTypeDef,
    },
)
_OptionalGetUsageStatisticsRequestRequestTypeDef = TypedDict(
    "_OptionalGetUsageStatisticsRequestRequestTypeDef",
    {
        "Unit": str,
        "MaxResults": int,
        "NextToken": str,
    },
    total=False,
)


class GetUsageStatisticsRequestRequestTypeDef(
    _RequiredGetUsageStatisticsRequestRequestTypeDef,
    _OptionalGetUsageStatisticsRequestRequestTypeDef,
):
    pass


VolumeTypeDef = TypedDict(
    "VolumeTypeDef",
    {
        "Name": str,
        "HostPath": HostPathTypeDef,
    },
    total=False,
)

ListInvitationsResponseTypeDef = TypedDict(
    "ListInvitationsResponseTypeDef",
    {
        "Invitations": List[InvitationTypeDef],
        "NextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

KubernetesConfigurationResultTypeDef = TypedDict(
    "KubernetesConfigurationResultTypeDef",
    {
        "AuditLogs": KubernetesAuditLogsConfigurationResultTypeDef,
    },
)

KubernetesConfigurationTypeDef = TypedDict(
    "KubernetesConfigurationTypeDef",
    {
        "AuditLogs": KubernetesAuditLogsConfigurationTypeDef,
    },
)

ProcessDetailsTypeDef = TypedDict(
    "ProcessDetailsTypeDef",
    {
        "Name": str,
        "ExecutablePath": str,
        "ExecutableSha256": str,
        "NamespacePid": int,
        "Pwd": str,
        "Pid": int,
        "StartTime": datetime,
        "Uuid": str,
        "ParentUuid": str,
        "User": str,
        "UserId": int,
        "Euid": int,
        "Lineage": List[LineageObjectTypeDef],
    },
    total=False,
)

MalwareProtectionConfigurationTypeDef = TypedDict(
    "MalwareProtectionConfigurationTypeDef",
    {
        "ScanEc2InstanceWithFindings": ScanEc2InstanceWithFindingsTypeDef,
    },
    total=False,
)

MemberFeaturesConfigurationResultTypeDef = TypedDict(
    "MemberFeaturesConfigurationResultTypeDef",
    {
        "Name": OrgFeatureType,
        "Status": FeatureStatusType,
        "UpdatedAt": datetime,
        "AdditionalConfiguration": List[MemberAdditionalConfigurationResultTypeDef],
    },
    total=False,
)

MemberFeaturesConfigurationTypeDef = TypedDict(
    "MemberFeaturesConfigurationTypeDef",
    {
        "Name": OrgFeatureType,
        "Status": FeatureStatusType,
        "AdditionalConfiguration": Sequence[MemberAdditionalConfigurationTypeDef],
    },
    total=False,
)

NetworkInterfaceTypeDef = TypedDict(
    "NetworkInterfaceTypeDef",
    {
        "Ipv6Addresses": List[str],
        "NetworkInterfaceId": str,
        "PrivateDnsName": str,
        "PrivateIpAddress": str,
        "PrivateIpAddresses": List[PrivateIpAddressDetailsTypeDef],
        "PublicDnsName": str,
        "PublicIp": str,
        "SecurityGroups": List[SecurityGroupTypeDef],
        "SubnetId": str,
        "VpcId": str,
    },
    total=False,
)

OrganizationFeatureConfigurationResultTypeDef = TypedDict(
    "OrganizationFeatureConfigurationResultTypeDef",
    {
        "Name": OrgFeatureType,
        "AutoEnable": OrgFeatureStatusType,
        "AdditionalConfiguration": List[OrganizationAdditionalConfigurationResultTypeDef],
    },
    total=False,
)

OrganizationFeatureConfigurationTypeDef = TypedDict(
    "OrganizationFeatureConfigurationTypeDef",
    {
        "Name": OrgFeatureType,
        "AutoEnable": OrgFeatureStatusType,
        "AdditionalConfiguration": Sequence[OrganizationAdditionalConfigurationTypeDef],
    },
    total=False,
)

OrganizationScanEc2InstanceWithFindingsResultTypeDef = TypedDict(
    "OrganizationScanEc2InstanceWithFindingsResultTypeDef",
    {
        "EbsVolumes": OrganizationEbsVolumesResultTypeDef,
    },
    total=False,
)

OrganizationScanEc2InstanceWithFindingsTypeDef = TypedDict(
    "OrganizationScanEc2InstanceWithFindingsTypeDef",
    {
        "EbsVolumes": OrganizationEbsVolumesTypeDef,
    },
    total=False,
)

OrganizationKubernetesConfigurationResultTypeDef = TypedDict(
    "OrganizationKubernetesConfigurationResultTypeDef",
    {
        "AuditLogs": OrganizationKubernetesAuditLogsConfigurationResultTypeDef,
    },
)

OrganizationKubernetesConfigurationTypeDef = TypedDict(
    "OrganizationKubernetesConfigurationTypeDef",
    {
        "AuditLogs": OrganizationKubernetesAuditLogsConfigurationTypeDef,
    },
)

RemoteIpDetailsTypeDef = TypedDict(
    "RemoteIpDetailsTypeDef",
    {
        "City": CityTypeDef,
        "Country": CountryTypeDef,
        "GeoLocation": GeoLocationTypeDef,
        "IpAddressV4": str,
        "Organization": OrganizationTypeDef,
    },
    total=False,
)

ScanConditionTypeDef = TypedDict(
    "ScanConditionTypeDef",
    {
        "MapEquals": List[ScanConditionPairTypeDef],
    },
)

ScanThreatNameTypeDef = TypedDict(
    "ScanThreatNameTypeDef",
    {
        "Name": str,
        "Severity": str,
        "ItemCount": int,
        "FilePaths": List[ScanFilePathTypeDef],
    },
    total=False,
)

ScanTypeDef = TypedDict(
    "ScanTypeDef",
    {
        "DetectorId": str,
        "AdminDetectorId": str,
        "ScanId": str,
        "ScanStatus": ScanStatusType,
        "FailureReason": str,
        "ScanStartTime": datetime,
        "ScanEndTime": datetime,
        "TriggerDetails": TriggerDetailsTypeDef,
        "ResourceDetails": ResourceDetailsTypeDef,
        "ScanResultDetails": ScanResultDetailsTypeDef,
        "AccountId": str,
        "TotalBytes": int,
        "FileCount": int,
        "AttachedVolumes": List[VolumeDetailTypeDef],
    },
    total=False,
)

UsageAccountResultTypeDef = TypedDict(
    "UsageAccountResultTypeDef",
    {
        "AccountId": str,
        "Total": TotalTypeDef,
    },
    total=False,
)

UsageDataSourceResultTypeDef = TypedDict(
    "UsageDataSourceResultTypeDef",
    {
        "DataSource": DataSourceType,
        "Total": TotalTypeDef,
    },
    total=False,
)

UsageFeatureResultTypeDef = TypedDict(
    "UsageFeatureResultTypeDef",
    {
        "Feature": UsageFeatureType,
        "Total": TotalTypeDef,
    },
    total=False,
)

UsageResourceResultTypeDef = TypedDict(
    "UsageResourceResultTypeDef",
    {
        "Resource": str,
        "Total": TotalTypeDef,
    },
    total=False,
)

CoverageResourceDetailsTypeDef = TypedDict(
    "CoverageResourceDetailsTypeDef",
    {
        "EksClusterDetails": CoverageEksClusterDetailsTypeDef,
        "ResourceType": Literal["EKS"],
    },
    total=False,
)

PermissionConfigurationTypeDef = TypedDict(
    "PermissionConfigurationTypeDef",
    {
        "BucketLevelPermissions": BucketLevelPermissionsTypeDef,
        "AccountLevelPermissions": AccountLevelPermissionsTypeDef,
    },
    total=False,
)

_RequiredCreateFilterRequestRequestTypeDef = TypedDict(
    "_RequiredCreateFilterRequestRequestTypeDef",
    {
        "DetectorId": str,
        "Name": str,
        "FindingCriteria": FindingCriteriaTypeDef,
    },
)
_OptionalCreateFilterRequestRequestTypeDef = TypedDict(
    "_OptionalCreateFilterRequestRequestTypeDef",
    {
        "Description": str,
        "Action": FilterActionType,
        "Rank": int,
        "ClientToken": str,
        "Tags": Mapping[str, str],
    },
    total=False,
)


class CreateFilterRequestRequestTypeDef(
    _RequiredCreateFilterRequestRequestTypeDef, _OptionalCreateFilterRequestRequestTypeDef
):
    pass


GetFilterResponseTypeDef = TypedDict(
    "GetFilterResponseTypeDef",
    {
        "Name": str,
        "Description": str,
        "Action": FilterActionType,
        "Rank": int,
        "FindingCriteria": FindingCriteriaTypeDef,
        "Tags": Dict[str, str],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

_RequiredGetFindingsStatisticsRequestRequestTypeDef = TypedDict(
    "_RequiredGetFindingsStatisticsRequestRequestTypeDef",
    {
        "DetectorId": str,
        "FindingStatisticTypes": Sequence[Literal["COUNT_BY_SEVERITY"]],
    },
)
_OptionalGetFindingsStatisticsRequestRequestTypeDef = TypedDict(
    "_OptionalGetFindingsStatisticsRequestRequestTypeDef",
    {
        "FindingCriteria": FindingCriteriaTypeDef,
    },
    total=False,
)


class GetFindingsStatisticsRequestRequestTypeDef(
    _RequiredGetFindingsStatisticsRequestRequestTypeDef,
    _OptionalGetFindingsStatisticsRequestRequestTypeDef,
):
    pass


_RequiredListFindingsRequestListFindingsPaginateTypeDef = TypedDict(
    "_RequiredListFindingsRequestListFindingsPaginateTypeDef",
    {
        "DetectorId": str,
    },
)
_OptionalListFindingsRequestListFindingsPaginateTypeDef = TypedDict(
    "_OptionalListFindingsRequestListFindingsPaginateTypeDef",
    {
        "FindingCriteria": FindingCriteriaTypeDef,
        "SortCriteria": SortCriteriaTypeDef,
        "PaginationConfig": PaginatorConfigTypeDef,
    },
    total=False,
)


class ListFindingsRequestListFindingsPaginateTypeDef(
    _RequiredListFindingsRequestListFindingsPaginateTypeDef,
    _OptionalListFindingsRequestListFindingsPaginateTypeDef,
):
    pass


_RequiredListFindingsRequestRequestTypeDef = TypedDict(
    "_RequiredListFindingsRequestRequestTypeDef",
    {
        "DetectorId": str,
    },
)
_OptionalListFindingsRequestRequestTypeDef = TypedDict(
    "_OptionalListFindingsRequestRequestTypeDef",
    {
        "FindingCriteria": FindingCriteriaTypeDef,
        "SortCriteria": SortCriteriaTypeDef,
        "MaxResults": int,
        "NextToken": str,
    },
    total=False,
)


class ListFindingsRequestRequestTypeDef(
    _RequiredListFindingsRequestRequestTypeDef, _OptionalListFindingsRequestRequestTypeDef
):
    pass


_RequiredUpdateFilterRequestRequestTypeDef = TypedDict(
    "_RequiredUpdateFilterRequestRequestTypeDef",
    {
        "DetectorId": str,
        "FilterName": str,
    },
)
_OptionalUpdateFilterRequestRequestTypeDef = TypedDict(
    "_OptionalUpdateFilterRequestRequestTypeDef",
    {
        "Description": str,
        "Action": FilterActionType,
        "Rank": int,
        "FindingCriteria": FindingCriteriaTypeDef,
    },
    total=False,
)


class UpdateFilterRequestRequestTypeDef(
    _RequiredUpdateFilterRequestRequestTypeDef, _OptionalUpdateFilterRequestRequestTypeDef
):
    pass


CoverageFilterCriteriaTypeDef = TypedDict(
    "CoverageFilterCriteriaTypeDef",
    {
        "FilterCriterion": Sequence[CoverageFilterCriterionTypeDef],
    },
    total=False,
)

DataSourcesFreeTrialTypeDef = TypedDict(
    "DataSourcesFreeTrialTypeDef",
    {
        "CloudTrail": DataSourceFreeTrialTypeDef,
        "DnsLogs": DataSourceFreeTrialTypeDef,
        "FlowLogs": DataSourceFreeTrialTypeDef,
        "S3Logs": DataSourceFreeTrialTypeDef,
        "Kubernetes": KubernetesDataSourceFreeTrialTypeDef,
        "MalwareProtection": MalwareProtectionDataSourceFreeTrialTypeDef,
    },
    total=False,
)

MalwareProtectionConfigurationResultTypeDef = TypedDict(
    "MalwareProtectionConfigurationResultTypeDef",
    {
        "ScanEc2InstanceWithFindings": ScanEc2InstanceWithFindingsResultTypeDef,
        "ServiceRole": str,
    },
    total=False,
)

FilterCriteriaTypeDef = TypedDict(
    "FilterCriteriaTypeDef",
    {
        "FilterCriterion": Sequence[FilterCriterionTypeDef],
    },
    total=False,
)

EcsTaskDetailsTypeDef = TypedDict(
    "EcsTaskDetailsTypeDef",
    {
        "Arn": str,
        "DefinitionArn": str,
        "Version": str,
        "TaskCreatedAt": datetime,
        "StartedAt": datetime,
        "StartedBy": str,
        "Tags": List[TagTypeDef],
        "Volumes": List[VolumeTypeDef],
        "Containers": List[ContainerTypeDef],
        "Group": str,
    },
    total=False,
)

KubernetesWorkloadDetailsTypeDef = TypedDict(
    "KubernetesWorkloadDetailsTypeDef",
    {
        "Name": str,
        "Type": str,
        "Uid": str,
        "Namespace": str,
        "HostNetwork": bool,
        "Containers": List[ContainerTypeDef],
        "Volumes": List[VolumeTypeDef],
    },
    total=False,
)

RuntimeContextTypeDef = TypedDict(
    "RuntimeContextTypeDef",
    {
        "ModifyingProcess": ProcessDetailsTypeDef,
        "ModifiedAt": datetime,
        "ScriptPath": str,
        "LibraryPath": str,
        "LdPreloadValue": str,
        "SocketPath": str,
        "RuncBinaryPath": str,
        "ReleaseAgentPath": str,
        "MountSource": str,
        "MountTarget": str,
        "FileSystemType": str,
        "Flags": List[str],
        "ModuleName": str,
        "ModuleFilePath": str,
        "ModuleSha256": str,
        "ShellHistoryFilePath": str,
        "TargetProcess": ProcessDetailsTypeDef,
        "AddressFamily": str,
        "IanaProtocolNumber": int,
        "MemoryRegions": List[str],
    },
    total=False,
)

DataSourceConfigurationsTypeDef = TypedDict(
    "DataSourceConfigurationsTypeDef",
    {
        "S3Logs": S3LogsConfigurationTypeDef,
        "Kubernetes": KubernetesConfigurationTypeDef,
        "MalwareProtection": MalwareProtectionConfigurationTypeDef,
    },
    total=False,
)

InstanceDetailsTypeDef = TypedDict(
    "InstanceDetailsTypeDef",
    {
        "AvailabilityZone": str,
        "IamInstanceProfile": IamInstanceProfileTypeDef,
        "ImageDescription": str,
        "ImageId": str,
        "InstanceId": str,
        "InstanceState": str,
        "InstanceType": str,
        "OutpostArn": str,
        "LaunchTime": str,
        "NetworkInterfaces": List[NetworkInterfaceTypeDef],
        "Platform": str,
        "ProductCodes": List[ProductCodeTypeDef],
        "Tags": List[TagTypeDef],
    },
    total=False,
)

OrganizationMalwareProtectionConfigurationResultTypeDef = TypedDict(
    "OrganizationMalwareProtectionConfigurationResultTypeDef",
    {
        "ScanEc2InstanceWithFindings": OrganizationScanEc2InstanceWithFindingsResultTypeDef,
    },
    total=False,
)

OrganizationMalwareProtectionConfigurationTypeDef = TypedDict(
    "OrganizationMalwareProtectionConfigurationTypeDef",
    {
        "ScanEc2InstanceWithFindings": OrganizationScanEc2InstanceWithFindingsTypeDef,
    },
    total=False,
)

AwsApiCallActionTypeDef = TypedDict(
    "AwsApiCallActionTypeDef",
    {
        "Api": str,
        "CallerType": str,
        "DomainDetails": DomainDetailsTypeDef,
        "ErrorCode": str,
        "UserAgent": str,
        "RemoteIpDetails": RemoteIpDetailsTypeDef,
        "ServiceName": str,
        "RemoteAccountDetails": RemoteAccountDetailsTypeDef,
        "AffectedResources": Dict[str, str],
    },
    total=False,
)

KubernetesApiCallActionTypeDef = TypedDict(
    "KubernetesApiCallActionTypeDef",
    {
        "RequestUri": str,
        "Verb": str,
        "SourceIps": List[str],
        "UserAgent": str,
        "RemoteIpDetails": RemoteIpDetailsTypeDef,
        "StatusCode": int,
        "Parameters": str,
    },
    total=False,
)

NetworkConnectionActionTypeDef = TypedDict(
    "NetworkConnectionActionTypeDef",
    {
        "Blocked": bool,
        "ConnectionDirection": str,
        "LocalPortDetails": LocalPortDetailsTypeDef,
        "Protocol": str,
        "LocalIpDetails": LocalIpDetailsTypeDef,
        "RemoteIpDetails": RemoteIpDetailsTypeDef,
        "RemotePortDetails": RemotePortDetailsTypeDef,
    },
    total=False,
)

PortProbeDetailTypeDef = TypedDict(
    "PortProbeDetailTypeDef",
    {
        "LocalPortDetails": LocalPortDetailsTypeDef,
        "LocalIpDetails": LocalIpDetailsTypeDef,
        "RemoteIpDetails": RemoteIpDetailsTypeDef,
    },
    total=False,
)

RdsLoginAttemptActionTypeDef = TypedDict(
    "RdsLoginAttemptActionTypeDef",
    {
        "RemoteIpDetails": RemoteIpDetailsTypeDef,
        "LoginAttributes": List[LoginAttributeTypeDef],
    },
    total=False,
)

ScanResourceCriteriaTypeDef = TypedDict(
    "ScanResourceCriteriaTypeDef",
    {
        "Include": Dict[Literal["EC2_INSTANCE_TAG"], ScanConditionTypeDef],
        "Exclude": Dict[Literal["EC2_INSTANCE_TAG"], ScanConditionTypeDef],
    },
    total=False,
)

ThreatDetectedByNameTypeDef = TypedDict(
    "ThreatDetectedByNameTypeDef",
    {
        "ItemCount": int,
        "UniqueThreatNameCount": int,
        "Shortened": bool,
        "ThreatNames": List[ScanThreatNameTypeDef],
    },
    total=False,
)

DescribeMalwareScansResponseTypeDef = TypedDict(
    "DescribeMalwareScansResponseTypeDef",
    {
        "Scans": List[ScanTypeDef],
        "NextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

UsageStatisticsTypeDef = TypedDict(
    "UsageStatisticsTypeDef",
    {
        "SumByAccount": List[UsageAccountResultTypeDef],
        "SumByDataSource": List[UsageDataSourceResultTypeDef],
        "SumByResource": List[UsageResourceResultTypeDef],
        "TopResources": List[UsageResourceResultTypeDef],
        "SumByFeature": List[UsageFeatureResultTypeDef],
    },
    total=False,
)

CoverageResourceTypeDef = TypedDict(
    "CoverageResourceTypeDef",
    {
        "ResourceId": str,
        "DetectorId": str,
        "AccountId": str,
        "ResourceDetails": CoverageResourceDetailsTypeDef,
        "CoverageStatus": CoverageStatusType,
        "Issue": str,
        "UpdatedAt": datetime,
    },
    total=False,
)

PublicAccessTypeDef = TypedDict(
    "PublicAccessTypeDef",
    {
        "PermissionConfiguration": PermissionConfigurationTypeDef,
        "EffectivePermission": str,
    },
    total=False,
)

_RequiredGetCoverageStatisticsRequestRequestTypeDef = TypedDict(
    "_RequiredGetCoverageStatisticsRequestRequestTypeDef",
    {
        "DetectorId": str,
        "StatisticsType": Sequence[CoverageStatisticsTypeType],
    },
)
_OptionalGetCoverageStatisticsRequestRequestTypeDef = TypedDict(
    "_OptionalGetCoverageStatisticsRequestRequestTypeDef",
    {
        "FilterCriteria": CoverageFilterCriteriaTypeDef,
    },
    total=False,
)


class GetCoverageStatisticsRequestRequestTypeDef(
    _RequiredGetCoverageStatisticsRequestRequestTypeDef,
    _OptionalGetCoverageStatisticsRequestRequestTypeDef,
):
    pass


_RequiredListCoverageRequestListCoveragePaginateTypeDef = TypedDict(
    "_RequiredListCoverageRequestListCoveragePaginateTypeDef",
    {
        "DetectorId": str,
    },
)
_OptionalListCoverageRequestListCoveragePaginateTypeDef = TypedDict(
    "_OptionalListCoverageRequestListCoveragePaginateTypeDef",
    {
        "FilterCriteria": CoverageFilterCriteriaTypeDef,
        "SortCriteria": CoverageSortCriteriaTypeDef,
        "PaginationConfig": PaginatorConfigTypeDef,
    },
    total=False,
)


class ListCoverageRequestListCoveragePaginateTypeDef(
    _RequiredListCoverageRequestListCoveragePaginateTypeDef,
    _OptionalListCoverageRequestListCoveragePaginateTypeDef,
):
    pass


_RequiredListCoverageRequestRequestTypeDef = TypedDict(
    "_RequiredListCoverageRequestRequestTypeDef",
    {
        "DetectorId": str,
    },
)
_OptionalListCoverageRequestRequestTypeDef = TypedDict(
    "_OptionalListCoverageRequestRequestTypeDef",
    {
        "NextToken": str,
        "MaxResults": int,
        "FilterCriteria": CoverageFilterCriteriaTypeDef,
        "SortCriteria": CoverageSortCriteriaTypeDef,
    },
    total=False,
)


class ListCoverageRequestRequestTypeDef(
    _RequiredListCoverageRequestRequestTypeDef, _OptionalListCoverageRequestRequestTypeDef
):
    pass


AccountFreeTrialInfoTypeDef = TypedDict(
    "AccountFreeTrialInfoTypeDef",
    {
        "AccountId": str,
        "DataSources": DataSourcesFreeTrialTypeDef,
        "Features": List[FreeTrialFeatureConfigurationResultTypeDef],
    },
    total=False,
)

_RequiredDataSourceConfigurationsResultTypeDef = TypedDict(
    "_RequiredDataSourceConfigurationsResultTypeDef",
    {
        "CloudTrail": CloudTrailConfigurationResultTypeDef,
        "DNSLogs": DNSLogsConfigurationResultTypeDef,
        "FlowLogs": FlowLogsConfigurationResultTypeDef,
        "S3Logs": S3LogsConfigurationResultTypeDef,
    },
)
_OptionalDataSourceConfigurationsResultTypeDef = TypedDict(
    "_OptionalDataSourceConfigurationsResultTypeDef",
    {
        "Kubernetes": KubernetesConfigurationResultTypeDef,
        "MalwareProtection": MalwareProtectionConfigurationResultTypeDef,
    },
    total=False,
)


class DataSourceConfigurationsResultTypeDef(
    _RequiredDataSourceConfigurationsResultTypeDef, _OptionalDataSourceConfigurationsResultTypeDef
):
    pass


UnprocessedDataSourcesResultTypeDef = TypedDict(
    "UnprocessedDataSourcesResultTypeDef",
    {
        "MalwareProtection": MalwareProtectionConfigurationResultTypeDef,
    },
    total=False,
)

_RequiredDescribeMalwareScansRequestDescribeMalwareScansPaginateTypeDef = TypedDict(
    "_RequiredDescribeMalwareScansRequestDescribeMalwareScansPaginateTypeDef",
    {
        "DetectorId": str,
    },
)
_OptionalDescribeMalwareScansRequestDescribeMalwareScansPaginateTypeDef = TypedDict(
    "_OptionalDescribeMalwareScansRequestDescribeMalwareScansPaginateTypeDef",
    {
        "FilterCriteria": FilterCriteriaTypeDef,
        "SortCriteria": SortCriteriaTypeDef,
        "PaginationConfig": PaginatorConfigTypeDef,
    },
    total=False,
)


class DescribeMalwareScansRequestDescribeMalwareScansPaginateTypeDef(
    _RequiredDescribeMalwareScansRequestDescribeMalwareScansPaginateTypeDef,
    _OptionalDescribeMalwareScansRequestDescribeMalwareScansPaginateTypeDef,
):
    pass


_RequiredDescribeMalwareScansRequestRequestTypeDef = TypedDict(
    "_RequiredDescribeMalwareScansRequestRequestTypeDef",
    {
        "DetectorId": str,
    },
)
_OptionalDescribeMalwareScansRequestRequestTypeDef = TypedDict(
    "_OptionalDescribeMalwareScansRequestRequestTypeDef",
    {
        "NextToken": str,
        "MaxResults": int,
        "FilterCriteria": FilterCriteriaTypeDef,
        "SortCriteria": SortCriteriaTypeDef,
    },
    total=False,
)


class DescribeMalwareScansRequestRequestTypeDef(
    _RequiredDescribeMalwareScansRequestRequestTypeDef,
    _OptionalDescribeMalwareScansRequestRequestTypeDef,
):
    pass


EcsClusterDetailsTypeDef = TypedDict(
    "EcsClusterDetailsTypeDef",
    {
        "Name": str,
        "Arn": str,
        "Status": str,
        "ActiveServicesCount": int,
        "RegisteredContainerInstancesCount": int,
        "RunningTasksCount": int,
        "Tags": List[TagTypeDef],
        "TaskDetails": EcsTaskDetailsTypeDef,
    },
    total=False,
)

KubernetesDetailsTypeDef = TypedDict(
    "KubernetesDetailsTypeDef",
    {
        "KubernetesUserDetails": KubernetesUserDetailsTypeDef,
        "KubernetesWorkloadDetails": KubernetesWorkloadDetailsTypeDef,
    },
    total=False,
)

RuntimeDetailsTypeDef = TypedDict(
    "RuntimeDetailsTypeDef",
    {
        "Process": ProcessDetailsTypeDef,
        "Context": RuntimeContextTypeDef,
    },
    total=False,
)

_RequiredCreateDetectorRequestRequestTypeDef = TypedDict(
    "_RequiredCreateDetectorRequestRequestTypeDef",
    {
        "Enable": bool,
    },
)
_OptionalCreateDetectorRequestRequestTypeDef = TypedDict(
    "_OptionalCreateDetectorRequestRequestTypeDef",
    {
        "ClientToken": str,
        "FindingPublishingFrequency": FindingPublishingFrequencyType,
        "DataSources": DataSourceConfigurationsTypeDef,
        "Tags": Mapping[str, str],
        "Features": Sequence[DetectorFeatureConfigurationTypeDef],
    },
    total=False,
)


class CreateDetectorRequestRequestTypeDef(
    _RequiredCreateDetectorRequestRequestTypeDef, _OptionalCreateDetectorRequestRequestTypeDef
):
    pass


_RequiredUpdateDetectorRequestRequestTypeDef = TypedDict(
    "_RequiredUpdateDetectorRequestRequestTypeDef",
    {
        "DetectorId": str,
    },
)
_OptionalUpdateDetectorRequestRequestTypeDef = TypedDict(
    "_OptionalUpdateDetectorRequestRequestTypeDef",
    {
        "Enable": bool,
        "FindingPublishingFrequency": FindingPublishingFrequencyType,
        "DataSources": DataSourceConfigurationsTypeDef,
        "Features": Sequence[DetectorFeatureConfigurationTypeDef],
    },
    total=False,
)


class UpdateDetectorRequestRequestTypeDef(
    _RequiredUpdateDetectorRequestRequestTypeDef, _OptionalUpdateDetectorRequestRequestTypeDef
):
    pass


_RequiredUpdateMemberDetectorsRequestRequestTypeDef = TypedDict(
    "_RequiredUpdateMemberDetectorsRequestRequestTypeDef",
    {
        "DetectorId": str,
        "AccountIds": Sequence[str],
    },
)
_OptionalUpdateMemberDetectorsRequestRequestTypeDef = TypedDict(
    "_OptionalUpdateMemberDetectorsRequestRequestTypeDef",
    {
        "DataSources": DataSourceConfigurationsTypeDef,
        "Features": Sequence[MemberFeaturesConfigurationTypeDef],
    },
    total=False,
)


class UpdateMemberDetectorsRequestRequestTypeDef(
    _RequiredUpdateMemberDetectorsRequestRequestTypeDef,
    _OptionalUpdateMemberDetectorsRequestRequestTypeDef,
):
    pass


_RequiredOrganizationDataSourceConfigurationsResultTypeDef = TypedDict(
    "_RequiredOrganizationDataSourceConfigurationsResultTypeDef",
    {
        "S3Logs": OrganizationS3LogsConfigurationResultTypeDef,
    },
)
_OptionalOrganizationDataSourceConfigurationsResultTypeDef = TypedDict(
    "_OptionalOrganizationDataSourceConfigurationsResultTypeDef",
    {
        "Kubernetes": OrganizationKubernetesConfigurationResultTypeDef,
        "MalwareProtection": OrganizationMalwareProtectionConfigurationResultTypeDef,
    },
    total=False,
)


class OrganizationDataSourceConfigurationsResultTypeDef(
    _RequiredOrganizationDataSourceConfigurationsResultTypeDef,
    _OptionalOrganizationDataSourceConfigurationsResultTypeDef,
):
    pass


OrganizationDataSourceConfigurationsTypeDef = TypedDict(
    "OrganizationDataSourceConfigurationsTypeDef",
    {
        "S3Logs": OrganizationS3LogsConfigurationTypeDef,
        "Kubernetes": OrganizationKubernetesConfigurationTypeDef,
        "MalwareProtection": OrganizationMalwareProtectionConfigurationTypeDef,
    },
    total=False,
)

PortProbeActionTypeDef = TypedDict(
    "PortProbeActionTypeDef",
    {
        "Blocked": bool,
        "PortProbeDetails": List[PortProbeDetailTypeDef],
    },
    total=False,
)

GetMalwareScanSettingsResponseTypeDef = TypedDict(
    "GetMalwareScanSettingsResponseTypeDef",
    {
        "ScanResourceCriteria": ScanResourceCriteriaTypeDef,
        "EbsSnapshotPreservation": EbsSnapshotPreservationType,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

_RequiredUpdateMalwareScanSettingsRequestRequestTypeDef = TypedDict(
    "_RequiredUpdateMalwareScanSettingsRequestRequestTypeDef",
    {
        "DetectorId": str,
    },
)
_OptionalUpdateMalwareScanSettingsRequestRequestTypeDef = TypedDict(
    "_OptionalUpdateMalwareScanSettingsRequestRequestTypeDef",
    {
        "ScanResourceCriteria": ScanResourceCriteriaTypeDef,
        "EbsSnapshotPreservation": EbsSnapshotPreservationType,
    },
    total=False,
)


class UpdateMalwareScanSettingsRequestRequestTypeDef(
    _RequiredUpdateMalwareScanSettingsRequestRequestTypeDef,
    _OptionalUpdateMalwareScanSettingsRequestRequestTypeDef,
):
    pass


ScanDetectionsTypeDef = TypedDict(
    "ScanDetectionsTypeDef",
    {
        "ScannedItemCount": ScannedItemCountTypeDef,
        "ThreatsDetectedItemCount": ThreatsDetectedItemCountTypeDef,
        "HighestSeverityThreatDetails": HighestSeverityThreatDetailsTypeDef,
        "ThreatDetectedByName": ThreatDetectedByNameTypeDef,
    },
    total=False,
)

GetUsageStatisticsResponseTypeDef = TypedDict(
    "GetUsageStatisticsResponseTypeDef",
    {
        "UsageStatistics": UsageStatisticsTypeDef,
        "NextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ListCoverageResponseTypeDef = TypedDict(
    "ListCoverageResponseTypeDef",
    {
        "Resources": List[CoverageResourceTypeDef],
        "NextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

S3BucketDetailTypeDef = TypedDict(
    "S3BucketDetailTypeDef",
    {
        "Arn": str,
        "Name": str,
        "Type": str,
        "CreatedAt": datetime,
        "Owner": OwnerTypeDef,
        "Tags": List[TagTypeDef],
        "DefaultServerSideEncryption": DefaultServerSideEncryptionTypeDef,
        "PublicAccess": PublicAccessTypeDef,
    },
    total=False,
)

GetRemainingFreeTrialDaysResponseTypeDef = TypedDict(
    "GetRemainingFreeTrialDaysResponseTypeDef",
    {
        "Accounts": List[AccountFreeTrialInfoTypeDef],
        "UnprocessedAccounts": List[UnprocessedAccountTypeDef],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

GetDetectorResponseTypeDef = TypedDict(
    "GetDetectorResponseTypeDef",
    {
        "CreatedAt": str,
        "FindingPublishingFrequency": FindingPublishingFrequencyType,
        "ServiceRole": str,
        "Status": DetectorStatusType,
        "UpdatedAt": str,
        "DataSources": DataSourceConfigurationsResultTypeDef,
        "Tags": Dict[str, str],
        "Features": List[DetectorFeatureConfigurationResultTypeDef],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

_RequiredMemberDataSourceConfigurationTypeDef = TypedDict(
    "_RequiredMemberDataSourceConfigurationTypeDef",
    {
        "AccountId": str,
    },
)
_OptionalMemberDataSourceConfigurationTypeDef = TypedDict(
    "_OptionalMemberDataSourceConfigurationTypeDef",
    {
        "DataSources": DataSourceConfigurationsResultTypeDef,
        "Features": List[MemberFeaturesConfigurationResultTypeDef],
    },
    total=False,
)


class MemberDataSourceConfigurationTypeDef(
    _RequiredMemberDataSourceConfigurationTypeDef, _OptionalMemberDataSourceConfigurationTypeDef
):
    pass


CreateDetectorResponseTypeDef = TypedDict(
    "CreateDetectorResponseTypeDef",
    {
        "DetectorId": str,
        "UnprocessedDataSources": UnprocessedDataSourcesResultTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

DescribeOrganizationConfigurationResponseTypeDef = TypedDict(
    "DescribeOrganizationConfigurationResponseTypeDef",
    {
        "AutoEnable": bool,
        "MemberAccountLimitReached": bool,
        "DataSources": OrganizationDataSourceConfigurationsResultTypeDef,
        "Features": List[OrganizationFeatureConfigurationResultTypeDef],
        "NextToken": str,
        "AutoEnableOrganizationMembers": AutoEnableMembersType,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

_RequiredUpdateOrganizationConfigurationRequestRequestTypeDef = TypedDict(
    "_RequiredUpdateOrganizationConfigurationRequestRequestTypeDef",
    {
        "DetectorId": str,
    },
)
_OptionalUpdateOrganizationConfigurationRequestRequestTypeDef = TypedDict(
    "_OptionalUpdateOrganizationConfigurationRequestRequestTypeDef",
    {
        "AutoEnable": bool,
        "DataSources": OrganizationDataSourceConfigurationsTypeDef,
        "Features": Sequence[OrganizationFeatureConfigurationTypeDef],
        "AutoEnableOrganizationMembers": AutoEnableMembersType,
    },
    total=False,
)


class UpdateOrganizationConfigurationRequestRequestTypeDef(
    _RequiredUpdateOrganizationConfigurationRequestRequestTypeDef,
    _OptionalUpdateOrganizationConfigurationRequestRequestTypeDef,
):
    pass


ActionTypeDef = TypedDict(
    "ActionTypeDef",
    {
        "ActionType": str,
        "AwsApiCallAction": AwsApiCallActionTypeDef,
        "DnsRequestAction": DnsRequestActionTypeDef,
        "NetworkConnectionAction": NetworkConnectionActionTypeDef,
        "PortProbeAction": PortProbeActionTypeDef,
        "KubernetesApiCallAction": KubernetesApiCallActionTypeDef,
        "RdsLoginAttemptAction": RdsLoginAttemptActionTypeDef,
    },
    total=False,
)

EbsVolumeScanDetailsTypeDef = TypedDict(
    "EbsVolumeScanDetailsTypeDef",
    {
        "ScanId": str,
        "ScanStartedAt": datetime,
        "ScanCompletedAt": datetime,
        "TriggerFindingId": str,
        "Sources": List[str],
        "ScanDetections": ScanDetectionsTypeDef,
    },
    total=False,
)

ResourceTypeDef = TypedDict(
    "ResourceTypeDef",
    {
        "AccessKeyDetails": AccessKeyDetailsTypeDef,
        "S3BucketDetails": List[S3BucketDetailTypeDef],
        "InstanceDetails": InstanceDetailsTypeDef,
        "EksClusterDetails": EksClusterDetailsTypeDef,
        "KubernetesDetails": KubernetesDetailsTypeDef,
        "ResourceType": str,
        "EbsVolumeDetails": EbsVolumeDetailsTypeDef,
        "EcsClusterDetails": EcsClusterDetailsTypeDef,
        "ContainerDetails": ContainerTypeDef,
        "RdsDbInstanceDetails": RdsDbInstanceDetailsTypeDef,
        "RdsDbUserDetails": RdsDbUserDetailsTypeDef,
    },
    total=False,
)

GetMemberDetectorsResponseTypeDef = TypedDict(
    "GetMemberDetectorsResponseTypeDef",
    {
        "MemberDataSourceConfigurations": List[MemberDataSourceConfigurationTypeDef],
        "UnprocessedAccounts": List[UnprocessedAccountTypeDef],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ServiceTypeDef = TypedDict(
    "ServiceTypeDef",
    {
        "Action": ActionTypeDef,
        "Evidence": EvidenceTypeDef,
        "Archived": bool,
        "Count": int,
        "DetectorId": str,
        "EventFirstSeen": str,
        "EventLastSeen": str,
        "ResourceRole": str,
        "ServiceName": str,
        "UserFeedback": str,
        "AdditionalInfo": ServiceAdditionalInfoTypeDef,
        "FeatureName": str,
        "EbsVolumeScanDetails": EbsVolumeScanDetailsTypeDef,
        "RuntimeDetails": RuntimeDetailsTypeDef,
    },
    total=False,
)

_RequiredFindingTypeDef = TypedDict(
    "_RequiredFindingTypeDef",
    {
        "AccountId": str,
        "Arn": str,
        "CreatedAt": str,
        "Id": str,
        "Region": str,
        "Resource": ResourceTypeDef,
        "SchemaVersion": str,
        "Severity": float,
        "Type": str,
        "UpdatedAt": str,
    },
)
_OptionalFindingTypeDef = TypedDict(
    "_OptionalFindingTypeDef",
    {
        "Confidence": float,
        "Description": str,
        "Partition": str,
        "Service": ServiceTypeDef,
        "Title": str,
    },
    total=False,
)


class FindingTypeDef(_RequiredFindingTypeDef, _OptionalFindingTypeDef):
    pass


GetFindingsResponseTypeDef = TypedDict(
    "GetFindingsResponseTypeDef",
    {
        "Findings": List[FindingTypeDef],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
