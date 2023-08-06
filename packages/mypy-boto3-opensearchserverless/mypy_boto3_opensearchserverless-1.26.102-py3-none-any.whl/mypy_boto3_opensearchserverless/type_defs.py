"""
Type annotations for opensearchserverless service type definitions.

[Open documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_opensearchserverless/type_defs/)

Usage::

    ```python
    from mypy_boto3_opensearchserverless.type_defs import AccessPolicyDetailTypeDef

    data: AccessPolicyDetailTypeDef = {...}
    ```
"""
import sys
from typing import Any, Dict, List, Sequence

from .literals import (
    CollectionStatusType,
    CollectionTypeType,
    SecurityPolicyTypeType,
    VpcEndpointStatusType,
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
    "AccessPolicyDetailTypeDef",
    "AccessPolicyStatsTypeDef",
    "AccessPolicySummaryTypeDef",
    "CapacityLimitsTypeDef",
    "BatchGetCollectionRequestRequestTypeDef",
    "CollectionDetailTypeDef",
    "CollectionErrorDetailTypeDef",
    "ResponseMetadataTypeDef",
    "BatchGetVpcEndpointRequestRequestTypeDef",
    "VpcEndpointDetailTypeDef",
    "VpcEndpointErrorDetailTypeDef",
    "CollectionFiltersTypeDef",
    "CollectionSummaryTypeDef",
    "CreateAccessPolicyRequestRequestTypeDef",
    "CreateCollectionDetailTypeDef",
    "TagTypeDef",
    "SamlConfigOptionsTypeDef",
    "CreateSecurityPolicyRequestRequestTypeDef",
    "SecurityPolicyDetailTypeDef",
    "CreateVpcEndpointDetailTypeDef",
    "CreateVpcEndpointRequestRequestTypeDef",
    "DeleteAccessPolicyRequestRequestTypeDef",
    "DeleteCollectionDetailTypeDef",
    "DeleteCollectionRequestRequestTypeDef",
    "DeleteSecurityConfigRequestRequestTypeDef",
    "DeleteSecurityPolicyRequestRequestTypeDef",
    "DeleteVpcEndpointDetailTypeDef",
    "DeleteVpcEndpointRequestRequestTypeDef",
    "GetAccessPolicyRequestRequestTypeDef",
    "SecurityConfigStatsTypeDef",
    "SecurityPolicyStatsTypeDef",
    "GetSecurityConfigRequestRequestTypeDef",
    "GetSecurityPolicyRequestRequestTypeDef",
    "ListAccessPoliciesRequestRequestTypeDef",
    "ListSecurityConfigsRequestRequestTypeDef",
    "SecurityConfigSummaryTypeDef",
    "ListSecurityPoliciesRequestRequestTypeDef",
    "SecurityPolicySummaryTypeDef",
    "ListTagsForResourceRequestRequestTypeDef",
    "VpcEndpointFiltersTypeDef",
    "VpcEndpointSummaryTypeDef",
    "UntagResourceRequestRequestTypeDef",
    "UpdateAccessPolicyRequestRequestTypeDef",
    "UpdateCollectionDetailTypeDef",
    "UpdateCollectionRequestRequestTypeDef",
    "UpdateSecurityPolicyRequestRequestTypeDef",
    "UpdateVpcEndpointDetailTypeDef",
    "UpdateVpcEndpointRequestRequestTypeDef",
    "AccountSettingsDetailTypeDef",
    "UpdateAccountSettingsRequestRequestTypeDef",
    "BatchGetCollectionResponseTypeDef",
    "CreateAccessPolicyResponseTypeDef",
    "GetAccessPolicyResponseTypeDef",
    "ListAccessPoliciesResponseTypeDef",
    "UpdateAccessPolicyResponseTypeDef",
    "BatchGetVpcEndpointResponseTypeDef",
    "ListCollectionsRequestRequestTypeDef",
    "ListCollectionsResponseTypeDef",
    "CreateCollectionResponseTypeDef",
    "CreateCollectionRequestRequestTypeDef",
    "ListTagsForResourceResponseTypeDef",
    "TagResourceRequestRequestTypeDef",
    "CreateSecurityConfigRequestRequestTypeDef",
    "SecurityConfigDetailTypeDef",
    "UpdateSecurityConfigRequestRequestTypeDef",
    "CreateSecurityPolicyResponseTypeDef",
    "GetSecurityPolicyResponseTypeDef",
    "UpdateSecurityPolicyResponseTypeDef",
    "CreateVpcEndpointResponseTypeDef",
    "DeleteCollectionResponseTypeDef",
    "DeleteVpcEndpointResponseTypeDef",
    "GetPoliciesStatsResponseTypeDef",
    "ListSecurityConfigsResponseTypeDef",
    "ListSecurityPoliciesResponseTypeDef",
    "ListVpcEndpointsRequestRequestTypeDef",
    "ListVpcEndpointsResponseTypeDef",
    "UpdateCollectionResponseTypeDef",
    "UpdateVpcEndpointResponseTypeDef",
    "GetAccountSettingsResponseTypeDef",
    "UpdateAccountSettingsResponseTypeDef",
    "CreateSecurityConfigResponseTypeDef",
    "GetSecurityConfigResponseTypeDef",
    "UpdateSecurityConfigResponseTypeDef",
)

AccessPolicyDetailTypeDef = TypedDict(
    "AccessPolicyDetailTypeDef",
    {
        "createdDate": int,
        "description": str,
        "lastModifiedDate": int,
        "name": str,
        "policy": Dict[str, Any],
        "policyVersion": str,
        "type": Literal["data"],
    },
    total=False,
)

AccessPolicyStatsTypeDef = TypedDict(
    "AccessPolicyStatsTypeDef",
    {
        "DataPolicyCount": int,
    },
    total=False,
)

AccessPolicySummaryTypeDef = TypedDict(
    "AccessPolicySummaryTypeDef",
    {
        "createdDate": int,
        "description": str,
        "lastModifiedDate": int,
        "name": str,
        "policyVersion": str,
        "type": Literal["data"],
    },
    total=False,
)

CapacityLimitsTypeDef = TypedDict(
    "CapacityLimitsTypeDef",
    {
        "maxIndexingCapacityInOCU": int,
        "maxSearchCapacityInOCU": int,
    },
    total=False,
)

BatchGetCollectionRequestRequestTypeDef = TypedDict(
    "BatchGetCollectionRequestRequestTypeDef",
    {
        "ids": Sequence[str],
        "names": Sequence[str],
    },
    total=False,
)

CollectionDetailTypeDef = TypedDict(
    "CollectionDetailTypeDef",
    {
        "arn": str,
        "collectionEndpoint": str,
        "createdDate": int,
        "dashboardEndpoint": str,
        "description": str,
        "id": str,
        "kmsKeyArn": str,
        "lastModifiedDate": int,
        "name": str,
        "status": CollectionStatusType,
        "type": CollectionTypeType,
    },
    total=False,
)

CollectionErrorDetailTypeDef = TypedDict(
    "CollectionErrorDetailTypeDef",
    {
        "errorCode": str,
        "errorMessage": str,
        "id": str,
        "name": str,
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

BatchGetVpcEndpointRequestRequestTypeDef = TypedDict(
    "BatchGetVpcEndpointRequestRequestTypeDef",
    {
        "ids": Sequence[str],
    },
)

VpcEndpointDetailTypeDef = TypedDict(
    "VpcEndpointDetailTypeDef",
    {
        "createdDate": int,
        "id": str,
        "name": str,
        "securityGroupIds": List[str],
        "status": VpcEndpointStatusType,
        "subnetIds": List[str],
        "vpcId": str,
    },
    total=False,
)

VpcEndpointErrorDetailTypeDef = TypedDict(
    "VpcEndpointErrorDetailTypeDef",
    {
        "errorCode": str,
        "errorMessage": str,
        "id": str,
    },
    total=False,
)

CollectionFiltersTypeDef = TypedDict(
    "CollectionFiltersTypeDef",
    {
        "name": str,
        "status": CollectionStatusType,
    },
    total=False,
)

CollectionSummaryTypeDef = TypedDict(
    "CollectionSummaryTypeDef",
    {
        "arn": str,
        "id": str,
        "name": str,
        "status": CollectionStatusType,
    },
    total=False,
)

_RequiredCreateAccessPolicyRequestRequestTypeDef = TypedDict(
    "_RequiredCreateAccessPolicyRequestRequestTypeDef",
    {
        "name": str,
        "policy": str,
        "type": Literal["data"],
    },
)
_OptionalCreateAccessPolicyRequestRequestTypeDef = TypedDict(
    "_OptionalCreateAccessPolicyRequestRequestTypeDef",
    {
        "clientToken": str,
        "description": str,
    },
    total=False,
)


class CreateAccessPolicyRequestRequestTypeDef(
    _RequiredCreateAccessPolicyRequestRequestTypeDef,
    _OptionalCreateAccessPolicyRequestRequestTypeDef,
):
    pass


CreateCollectionDetailTypeDef = TypedDict(
    "CreateCollectionDetailTypeDef",
    {
        "arn": str,
        "createdDate": int,
        "description": str,
        "id": str,
        "kmsKeyArn": str,
        "lastModifiedDate": int,
        "name": str,
        "status": CollectionStatusType,
        "type": CollectionTypeType,
    },
    total=False,
)

TagTypeDef = TypedDict(
    "TagTypeDef",
    {
        "key": str,
        "value": str,
    },
)

_RequiredSamlConfigOptionsTypeDef = TypedDict(
    "_RequiredSamlConfigOptionsTypeDef",
    {
        "metadata": str,
    },
)
_OptionalSamlConfigOptionsTypeDef = TypedDict(
    "_OptionalSamlConfigOptionsTypeDef",
    {
        "groupAttribute": str,
        "sessionTimeout": int,
        "userAttribute": str,
    },
    total=False,
)


class SamlConfigOptionsTypeDef(
    _RequiredSamlConfigOptionsTypeDef, _OptionalSamlConfigOptionsTypeDef
):
    pass


_RequiredCreateSecurityPolicyRequestRequestTypeDef = TypedDict(
    "_RequiredCreateSecurityPolicyRequestRequestTypeDef",
    {
        "name": str,
        "policy": str,
        "type": SecurityPolicyTypeType,
    },
)
_OptionalCreateSecurityPolicyRequestRequestTypeDef = TypedDict(
    "_OptionalCreateSecurityPolicyRequestRequestTypeDef",
    {
        "clientToken": str,
        "description": str,
    },
    total=False,
)


class CreateSecurityPolicyRequestRequestTypeDef(
    _RequiredCreateSecurityPolicyRequestRequestTypeDef,
    _OptionalCreateSecurityPolicyRequestRequestTypeDef,
):
    pass


SecurityPolicyDetailTypeDef = TypedDict(
    "SecurityPolicyDetailTypeDef",
    {
        "createdDate": int,
        "description": str,
        "lastModifiedDate": int,
        "name": str,
        "policy": Dict[str, Any],
        "policyVersion": str,
        "type": SecurityPolicyTypeType,
    },
    total=False,
)

CreateVpcEndpointDetailTypeDef = TypedDict(
    "CreateVpcEndpointDetailTypeDef",
    {
        "id": str,
        "name": str,
        "status": VpcEndpointStatusType,
    },
    total=False,
)

_RequiredCreateVpcEndpointRequestRequestTypeDef = TypedDict(
    "_RequiredCreateVpcEndpointRequestRequestTypeDef",
    {
        "name": str,
        "subnetIds": Sequence[str],
        "vpcId": str,
    },
)
_OptionalCreateVpcEndpointRequestRequestTypeDef = TypedDict(
    "_OptionalCreateVpcEndpointRequestRequestTypeDef",
    {
        "clientToken": str,
        "securityGroupIds": Sequence[str],
    },
    total=False,
)


class CreateVpcEndpointRequestRequestTypeDef(
    _RequiredCreateVpcEndpointRequestRequestTypeDef, _OptionalCreateVpcEndpointRequestRequestTypeDef
):
    pass


_RequiredDeleteAccessPolicyRequestRequestTypeDef = TypedDict(
    "_RequiredDeleteAccessPolicyRequestRequestTypeDef",
    {
        "name": str,
        "type": Literal["data"],
    },
)
_OptionalDeleteAccessPolicyRequestRequestTypeDef = TypedDict(
    "_OptionalDeleteAccessPolicyRequestRequestTypeDef",
    {
        "clientToken": str,
    },
    total=False,
)


class DeleteAccessPolicyRequestRequestTypeDef(
    _RequiredDeleteAccessPolicyRequestRequestTypeDef,
    _OptionalDeleteAccessPolicyRequestRequestTypeDef,
):
    pass


DeleteCollectionDetailTypeDef = TypedDict(
    "DeleteCollectionDetailTypeDef",
    {
        "id": str,
        "name": str,
        "status": CollectionStatusType,
    },
    total=False,
)

_RequiredDeleteCollectionRequestRequestTypeDef = TypedDict(
    "_RequiredDeleteCollectionRequestRequestTypeDef",
    {
        "id": str,
    },
)
_OptionalDeleteCollectionRequestRequestTypeDef = TypedDict(
    "_OptionalDeleteCollectionRequestRequestTypeDef",
    {
        "clientToken": str,
    },
    total=False,
)


class DeleteCollectionRequestRequestTypeDef(
    _RequiredDeleteCollectionRequestRequestTypeDef, _OptionalDeleteCollectionRequestRequestTypeDef
):
    pass


_RequiredDeleteSecurityConfigRequestRequestTypeDef = TypedDict(
    "_RequiredDeleteSecurityConfigRequestRequestTypeDef",
    {
        "id": str,
    },
)
_OptionalDeleteSecurityConfigRequestRequestTypeDef = TypedDict(
    "_OptionalDeleteSecurityConfigRequestRequestTypeDef",
    {
        "clientToken": str,
    },
    total=False,
)


class DeleteSecurityConfigRequestRequestTypeDef(
    _RequiredDeleteSecurityConfigRequestRequestTypeDef,
    _OptionalDeleteSecurityConfigRequestRequestTypeDef,
):
    pass


_RequiredDeleteSecurityPolicyRequestRequestTypeDef = TypedDict(
    "_RequiredDeleteSecurityPolicyRequestRequestTypeDef",
    {
        "name": str,
        "type": SecurityPolicyTypeType,
    },
)
_OptionalDeleteSecurityPolicyRequestRequestTypeDef = TypedDict(
    "_OptionalDeleteSecurityPolicyRequestRequestTypeDef",
    {
        "clientToken": str,
    },
    total=False,
)


class DeleteSecurityPolicyRequestRequestTypeDef(
    _RequiredDeleteSecurityPolicyRequestRequestTypeDef,
    _OptionalDeleteSecurityPolicyRequestRequestTypeDef,
):
    pass


DeleteVpcEndpointDetailTypeDef = TypedDict(
    "DeleteVpcEndpointDetailTypeDef",
    {
        "id": str,
        "name": str,
        "status": VpcEndpointStatusType,
    },
    total=False,
)

_RequiredDeleteVpcEndpointRequestRequestTypeDef = TypedDict(
    "_RequiredDeleteVpcEndpointRequestRequestTypeDef",
    {
        "id": str,
    },
)
_OptionalDeleteVpcEndpointRequestRequestTypeDef = TypedDict(
    "_OptionalDeleteVpcEndpointRequestRequestTypeDef",
    {
        "clientToken": str,
    },
    total=False,
)


class DeleteVpcEndpointRequestRequestTypeDef(
    _RequiredDeleteVpcEndpointRequestRequestTypeDef, _OptionalDeleteVpcEndpointRequestRequestTypeDef
):
    pass


GetAccessPolicyRequestRequestTypeDef = TypedDict(
    "GetAccessPolicyRequestRequestTypeDef",
    {
        "name": str,
        "type": Literal["data"],
    },
)

SecurityConfigStatsTypeDef = TypedDict(
    "SecurityConfigStatsTypeDef",
    {
        "SamlConfigCount": int,
    },
    total=False,
)

SecurityPolicyStatsTypeDef = TypedDict(
    "SecurityPolicyStatsTypeDef",
    {
        "EncryptionPolicyCount": int,
        "NetworkPolicyCount": int,
    },
    total=False,
)

GetSecurityConfigRequestRequestTypeDef = TypedDict(
    "GetSecurityConfigRequestRequestTypeDef",
    {
        "id": str,
    },
)

GetSecurityPolicyRequestRequestTypeDef = TypedDict(
    "GetSecurityPolicyRequestRequestTypeDef",
    {
        "name": str,
        "type": SecurityPolicyTypeType,
    },
)

_RequiredListAccessPoliciesRequestRequestTypeDef = TypedDict(
    "_RequiredListAccessPoliciesRequestRequestTypeDef",
    {
        "type": Literal["data"],
    },
)
_OptionalListAccessPoliciesRequestRequestTypeDef = TypedDict(
    "_OptionalListAccessPoliciesRequestRequestTypeDef",
    {
        "maxResults": int,
        "nextToken": str,
        "resource": Sequence[str],
    },
    total=False,
)


class ListAccessPoliciesRequestRequestTypeDef(
    _RequiredListAccessPoliciesRequestRequestTypeDef,
    _OptionalListAccessPoliciesRequestRequestTypeDef,
):
    pass


_RequiredListSecurityConfigsRequestRequestTypeDef = TypedDict(
    "_RequiredListSecurityConfigsRequestRequestTypeDef",
    {
        "type": Literal["saml"],
    },
)
_OptionalListSecurityConfigsRequestRequestTypeDef = TypedDict(
    "_OptionalListSecurityConfigsRequestRequestTypeDef",
    {
        "maxResults": int,
        "nextToken": str,
    },
    total=False,
)


class ListSecurityConfigsRequestRequestTypeDef(
    _RequiredListSecurityConfigsRequestRequestTypeDef,
    _OptionalListSecurityConfigsRequestRequestTypeDef,
):
    pass


SecurityConfigSummaryTypeDef = TypedDict(
    "SecurityConfigSummaryTypeDef",
    {
        "configVersion": str,
        "createdDate": int,
        "description": str,
        "id": str,
        "lastModifiedDate": int,
        "type": Literal["saml"],
    },
    total=False,
)

_RequiredListSecurityPoliciesRequestRequestTypeDef = TypedDict(
    "_RequiredListSecurityPoliciesRequestRequestTypeDef",
    {
        "type": SecurityPolicyTypeType,
    },
)
_OptionalListSecurityPoliciesRequestRequestTypeDef = TypedDict(
    "_OptionalListSecurityPoliciesRequestRequestTypeDef",
    {
        "maxResults": int,
        "nextToken": str,
        "resource": Sequence[str],
    },
    total=False,
)


class ListSecurityPoliciesRequestRequestTypeDef(
    _RequiredListSecurityPoliciesRequestRequestTypeDef,
    _OptionalListSecurityPoliciesRequestRequestTypeDef,
):
    pass


SecurityPolicySummaryTypeDef = TypedDict(
    "SecurityPolicySummaryTypeDef",
    {
        "createdDate": int,
        "description": str,
        "lastModifiedDate": int,
        "name": str,
        "policyVersion": str,
        "type": SecurityPolicyTypeType,
    },
    total=False,
)

ListTagsForResourceRequestRequestTypeDef = TypedDict(
    "ListTagsForResourceRequestRequestTypeDef",
    {
        "resourceArn": str,
    },
)

VpcEndpointFiltersTypeDef = TypedDict(
    "VpcEndpointFiltersTypeDef",
    {
        "status": VpcEndpointStatusType,
    },
    total=False,
)

VpcEndpointSummaryTypeDef = TypedDict(
    "VpcEndpointSummaryTypeDef",
    {
        "id": str,
        "name": str,
        "status": VpcEndpointStatusType,
    },
    total=False,
)

UntagResourceRequestRequestTypeDef = TypedDict(
    "UntagResourceRequestRequestTypeDef",
    {
        "resourceArn": str,
        "tagKeys": Sequence[str],
    },
)

_RequiredUpdateAccessPolicyRequestRequestTypeDef = TypedDict(
    "_RequiredUpdateAccessPolicyRequestRequestTypeDef",
    {
        "name": str,
        "policyVersion": str,
        "type": Literal["data"],
    },
)
_OptionalUpdateAccessPolicyRequestRequestTypeDef = TypedDict(
    "_OptionalUpdateAccessPolicyRequestRequestTypeDef",
    {
        "clientToken": str,
        "description": str,
        "policy": str,
    },
    total=False,
)


class UpdateAccessPolicyRequestRequestTypeDef(
    _RequiredUpdateAccessPolicyRequestRequestTypeDef,
    _OptionalUpdateAccessPolicyRequestRequestTypeDef,
):
    pass


UpdateCollectionDetailTypeDef = TypedDict(
    "UpdateCollectionDetailTypeDef",
    {
        "arn": str,
        "createdDate": int,
        "description": str,
        "id": str,
        "lastModifiedDate": int,
        "name": str,
        "status": CollectionStatusType,
        "type": CollectionTypeType,
    },
    total=False,
)

_RequiredUpdateCollectionRequestRequestTypeDef = TypedDict(
    "_RequiredUpdateCollectionRequestRequestTypeDef",
    {
        "id": str,
    },
)
_OptionalUpdateCollectionRequestRequestTypeDef = TypedDict(
    "_OptionalUpdateCollectionRequestRequestTypeDef",
    {
        "clientToken": str,
        "description": str,
    },
    total=False,
)


class UpdateCollectionRequestRequestTypeDef(
    _RequiredUpdateCollectionRequestRequestTypeDef, _OptionalUpdateCollectionRequestRequestTypeDef
):
    pass


_RequiredUpdateSecurityPolicyRequestRequestTypeDef = TypedDict(
    "_RequiredUpdateSecurityPolicyRequestRequestTypeDef",
    {
        "name": str,
        "policyVersion": str,
        "type": SecurityPolicyTypeType,
    },
)
_OptionalUpdateSecurityPolicyRequestRequestTypeDef = TypedDict(
    "_OptionalUpdateSecurityPolicyRequestRequestTypeDef",
    {
        "clientToken": str,
        "description": str,
        "policy": str,
    },
    total=False,
)


class UpdateSecurityPolicyRequestRequestTypeDef(
    _RequiredUpdateSecurityPolicyRequestRequestTypeDef,
    _OptionalUpdateSecurityPolicyRequestRequestTypeDef,
):
    pass


UpdateVpcEndpointDetailTypeDef = TypedDict(
    "UpdateVpcEndpointDetailTypeDef",
    {
        "id": str,
        "lastModifiedDate": int,
        "name": str,
        "securityGroupIds": List[str],
        "status": VpcEndpointStatusType,
        "subnetIds": List[str],
    },
    total=False,
)

_RequiredUpdateVpcEndpointRequestRequestTypeDef = TypedDict(
    "_RequiredUpdateVpcEndpointRequestRequestTypeDef",
    {
        "id": str,
    },
)
_OptionalUpdateVpcEndpointRequestRequestTypeDef = TypedDict(
    "_OptionalUpdateVpcEndpointRequestRequestTypeDef",
    {
        "addSecurityGroupIds": Sequence[str],
        "addSubnetIds": Sequence[str],
        "clientToken": str,
        "removeSecurityGroupIds": Sequence[str],
        "removeSubnetIds": Sequence[str],
    },
    total=False,
)


class UpdateVpcEndpointRequestRequestTypeDef(
    _RequiredUpdateVpcEndpointRequestRequestTypeDef, _OptionalUpdateVpcEndpointRequestRequestTypeDef
):
    pass


AccountSettingsDetailTypeDef = TypedDict(
    "AccountSettingsDetailTypeDef",
    {
        "capacityLimits": CapacityLimitsTypeDef,
    },
    total=False,
)

UpdateAccountSettingsRequestRequestTypeDef = TypedDict(
    "UpdateAccountSettingsRequestRequestTypeDef",
    {
        "capacityLimits": CapacityLimitsTypeDef,
    },
    total=False,
)

BatchGetCollectionResponseTypeDef = TypedDict(
    "BatchGetCollectionResponseTypeDef",
    {
        "collectionDetails": List[CollectionDetailTypeDef],
        "collectionErrorDetails": List[CollectionErrorDetailTypeDef],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

CreateAccessPolicyResponseTypeDef = TypedDict(
    "CreateAccessPolicyResponseTypeDef",
    {
        "accessPolicyDetail": AccessPolicyDetailTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

GetAccessPolicyResponseTypeDef = TypedDict(
    "GetAccessPolicyResponseTypeDef",
    {
        "accessPolicyDetail": AccessPolicyDetailTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ListAccessPoliciesResponseTypeDef = TypedDict(
    "ListAccessPoliciesResponseTypeDef",
    {
        "accessPolicySummaries": List[AccessPolicySummaryTypeDef],
        "nextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

UpdateAccessPolicyResponseTypeDef = TypedDict(
    "UpdateAccessPolicyResponseTypeDef",
    {
        "accessPolicyDetail": AccessPolicyDetailTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

BatchGetVpcEndpointResponseTypeDef = TypedDict(
    "BatchGetVpcEndpointResponseTypeDef",
    {
        "vpcEndpointDetails": List[VpcEndpointDetailTypeDef],
        "vpcEndpointErrorDetails": List[VpcEndpointErrorDetailTypeDef],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ListCollectionsRequestRequestTypeDef = TypedDict(
    "ListCollectionsRequestRequestTypeDef",
    {
        "collectionFilters": CollectionFiltersTypeDef,
        "maxResults": int,
        "nextToken": str,
    },
    total=False,
)

ListCollectionsResponseTypeDef = TypedDict(
    "ListCollectionsResponseTypeDef",
    {
        "collectionSummaries": List[CollectionSummaryTypeDef],
        "nextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

CreateCollectionResponseTypeDef = TypedDict(
    "CreateCollectionResponseTypeDef",
    {
        "createCollectionDetail": CreateCollectionDetailTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

_RequiredCreateCollectionRequestRequestTypeDef = TypedDict(
    "_RequiredCreateCollectionRequestRequestTypeDef",
    {
        "name": str,
    },
)
_OptionalCreateCollectionRequestRequestTypeDef = TypedDict(
    "_OptionalCreateCollectionRequestRequestTypeDef",
    {
        "clientToken": str,
        "description": str,
        "tags": Sequence[TagTypeDef],
        "type": CollectionTypeType,
    },
    total=False,
)


class CreateCollectionRequestRequestTypeDef(
    _RequiredCreateCollectionRequestRequestTypeDef, _OptionalCreateCollectionRequestRequestTypeDef
):
    pass


ListTagsForResourceResponseTypeDef = TypedDict(
    "ListTagsForResourceResponseTypeDef",
    {
        "tags": List[TagTypeDef],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

TagResourceRequestRequestTypeDef = TypedDict(
    "TagResourceRequestRequestTypeDef",
    {
        "resourceArn": str,
        "tags": Sequence[TagTypeDef],
    },
)

_RequiredCreateSecurityConfigRequestRequestTypeDef = TypedDict(
    "_RequiredCreateSecurityConfigRequestRequestTypeDef",
    {
        "name": str,
        "type": Literal["saml"],
    },
)
_OptionalCreateSecurityConfigRequestRequestTypeDef = TypedDict(
    "_OptionalCreateSecurityConfigRequestRequestTypeDef",
    {
        "clientToken": str,
        "description": str,
        "samlOptions": SamlConfigOptionsTypeDef,
    },
    total=False,
)


class CreateSecurityConfigRequestRequestTypeDef(
    _RequiredCreateSecurityConfigRequestRequestTypeDef,
    _OptionalCreateSecurityConfigRequestRequestTypeDef,
):
    pass


SecurityConfigDetailTypeDef = TypedDict(
    "SecurityConfigDetailTypeDef",
    {
        "configVersion": str,
        "createdDate": int,
        "description": str,
        "id": str,
        "lastModifiedDate": int,
        "samlOptions": SamlConfigOptionsTypeDef,
        "type": Literal["saml"],
    },
    total=False,
)

_RequiredUpdateSecurityConfigRequestRequestTypeDef = TypedDict(
    "_RequiredUpdateSecurityConfigRequestRequestTypeDef",
    {
        "configVersion": str,
        "id": str,
    },
)
_OptionalUpdateSecurityConfigRequestRequestTypeDef = TypedDict(
    "_OptionalUpdateSecurityConfigRequestRequestTypeDef",
    {
        "clientToken": str,
        "description": str,
        "samlOptions": SamlConfigOptionsTypeDef,
    },
    total=False,
)


class UpdateSecurityConfigRequestRequestTypeDef(
    _RequiredUpdateSecurityConfigRequestRequestTypeDef,
    _OptionalUpdateSecurityConfigRequestRequestTypeDef,
):
    pass


CreateSecurityPolicyResponseTypeDef = TypedDict(
    "CreateSecurityPolicyResponseTypeDef",
    {
        "securityPolicyDetail": SecurityPolicyDetailTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

GetSecurityPolicyResponseTypeDef = TypedDict(
    "GetSecurityPolicyResponseTypeDef",
    {
        "securityPolicyDetail": SecurityPolicyDetailTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

UpdateSecurityPolicyResponseTypeDef = TypedDict(
    "UpdateSecurityPolicyResponseTypeDef",
    {
        "securityPolicyDetail": SecurityPolicyDetailTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

CreateVpcEndpointResponseTypeDef = TypedDict(
    "CreateVpcEndpointResponseTypeDef",
    {
        "createVpcEndpointDetail": CreateVpcEndpointDetailTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

DeleteCollectionResponseTypeDef = TypedDict(
    "DeleteCollectionResponseTypeDef",
    {
        "deleteCollectionDetail": DeleteCollectionDetailTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

DeleteVpcEndpointResponseTypeDef = TypedDict(
    "DeleteVpcEndpointResponseTypeDef",
    {
        "deleteVpcEndpointDetail": DeleteVpcEndpointDetailTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

GetPoliciesStatsResponseTypeDef = TypedDict(
    "GetPoliciesStatsResponseTypeDef",
    {
        "AccessPolicyStats": AccessPolicyStatsTypeDef,
        "SecurityConfigStats": SecurityConfigStatsTypeDef,
        "SecurityPolicyStats": SecurityPolicyStatsTypeDef,
        "TotalPolicyCount": int,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ListSecurityConfigsResponseTypeDef = TypedDict(
    "ListSecurityConfigsResponseTypeDef",
    {
        "nextToken": str,
        "securityConfigSummaries": List[SecurityConfigSummaryTypeDef],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ListSecurityPoliciesResponseTypeDef = TypedDict(
    "ListSecurityPoliciesResponseTypeDef",
    {
        "nextToken": str,
        "securityPolicySummaries": List[SecurityPolicySummaryTypeDef],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ListVpcEndpointsRequestRequestTypeDef = TypedDict(
    "ListVpcEndpointsRequestRequestTypeDef",
    {
        "maxResults": int,
        "nextToken": str,
        "vpcEndpointFilters": VpcEndpointFiltersTypeDef,
    },
    total=False,
)

ListVpcEndpointsResponseTypeDef = TypedDict(
    "ListVpcEndpointsResponseTypeDef",
    {
        "nextToken": str,
        "vpcEndpointSummaries": List[VpcEndpointSummaryTypeDef],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

UpdateCollectionResponseTypeDef = TypedDict(
    "UpdateCollectionResponseTypeDef",
    {
        "updateCollectionDetail": UpdateCollectionDetailTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

UpdateVpcEndpointResponseTypeDef = TypedDict(
    "UpdateVpcEndpointResponseTypeDef",
    {
        "UpdateVpcEndpointDetail": UpdateVpcEndpointDetailTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

GetAccountSettingsResponseTypeDef = TypedDict(
    "GetAccountSettingsResponseTypeDef",
    {
        "accountSettingsDetail": AccountSettingsDetailTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

UpdateAccountSettingsResponseTypeDef = TypedDict(
    "UpdateAccountSettingsResponseTypeDef",
    {
        "accountSettingsDetail": AccountSettingsDetailTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

CreateSecurityConfigResponseTypeDef = TypedDict(
    "CreateSecurityConfigResponseTypeDef",
    {
        "securityConfigDetail": SecurityConfigDetailTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

GetSecurityConfigResponseTypeDef = TypedDict(
    "GetSecurityConfigResponseTypeDef",
    {
        "securityConfigDetail": SecurityConfigDetailTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

UpdateSecurityConfigResponseTypeDef = TypedDict(
    "UpdateSecurityConfigResponseTypeDef",
    {
        "securityConfigDetail": SecurityConfigDetailTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
