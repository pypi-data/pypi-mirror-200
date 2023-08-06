"""
Type annotations for opensearchserverless service client.

[Open documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_opensearchserverless/client/)

Usage::

    ```python
    from boto3.session import Session
    from mypy_boto3_opensearchserverless.client import OpenSearchServiceServerlessClient

    session = Session()
    client: OpenSearchServiceServerlessClient = session.client("opensearchserverless")
    ```
"""
import sys
from typing import Any, Dict, Mapping, Sequence, Type

from botocore.client import BaseClient, ClientMeta

from .literals import CollectionTypeType, SecurityPolicyTypeType
from .type_defs import (
    BatchGetCollectionResponseTypeDef,
    BatchGetVpcEndpointResponseTypeDef,
    CapacityLimitsTypeDef,
    CollectionFiltersTypeDef,
    CreateAccessPolicyResponseTypeDef,
    CreateCollectionResponseTypeDef,
    CreateSecurityConfigResponseTypeDef,
    CreateSecurityPolicyResponseTypeDef,
    CreateVpcEndpointResponseTypeDef,
    DeleteCollectionResponseTypeDef,
    DeleteVpcEndpointResponseTypeDef,
    GetAccessPolicyResponseTypeDef,
    GetAccountSettingsResponseTypeDef,
    GetPoliciesStatsResponseTypeDef,
    GetSecurityConfigResponseTypeDef,
    GetSecurityPolicyResponseTypeDef,
    ListAccessPoliciesResponseTypeDef,
    ListCollectionsResponseTypeDef,
    ListSecurityConfigsResponseTypeDef,
    ListSecurityPoliciesResponseTypeDef,
    ListTagsForResourceResponseTypeDef,
    ListVpcEndpointsResponseTypeDef,
    SamlConfigOptionsTypeDef,
    TagTypeDef,
    UpdateAccessPolicyResponseTypeDef,
    UpdateAccountSettingsResponseTypeDef,
    UpdateCollectionResponseTypeDef,
    UpdateSecurityConfigResponseTypeDef,
    UpdateSecurityPolicyResponseTypeDef,
    UpdateVpcEndpointResponseTypeDef,
    VpcEndpointFiltersTypeDef,
)

if sys.version_info >= (3, 9):
    from typing import Literal
else:
    from typing_extensions import Literal


__all__ = ("OpenSearchServiceServerlessClient",)


class BotocoreClientError(BaseException):
    MSG_TEMPLATE: str

    def __init__(self, error_response: Mapping[str, Any], operation_name: str) -> None:
        self.response: Dict[str, Any]
        self.operation_name: str


class Exceptions:
    ClientError: Type[BotocoreClientError]
    ConflictException: Type[BotocoreClientError]
    InternalServerException: Type[BotocoreClientError]
    OcuLimitExceededException: Type[BotocoreClientError]
    ResourceNotFoundException: Type[BotocoreClientError]
    ServiceQuotaExceededException: Type[BotocoreClientError]
    ValidationException: Type[BotocoreClientError]


class OpenSearchServiceServerlessClient(BaseClient):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/opensearchserverless.html#OpenSearchServiceServerless.Client)
    [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_opensearchserverless/client/)
    """

    meta: ClientMeta

    @property
    def exceptions(self) -> Exceptions:
        """
        OpenSearchServiceServerlessClient exceptions.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/opensearchserverless.html#OpenSearchServiceServerless.Client.exceptions)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_opensearchserverless/client/#exceptions)
        """

    def batch_get_collection(
        self, *, ids: Sequence[str] = ..., names: Sequence[str] = ...
    ) -> BatchGetCollectionResponseTypeDef:
        """
        Returns attributes for one or more collections, including the collection
        endpoint and the OpenSearch Dashboards endpoint.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/opensearchserverless.html#OpenSearchServiceServerless.Client.batch_get_collection)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_opensearchserverless/client/#batch_get_collection)
        """

    def batch_get_vpc_endpoint(self, *, ids: Sequence[str]) -> BatchGetVpcEndpointResponseTypeDef:
        """
        Returns attributes for one or more VPC endpoints associated with the current
        account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/opensearchserverless.html#OpenSearchServiceServerless.Client.batch_get_vpc_endpoint)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_opensearchserverless/client/#batch_get_vpc_endpoint)
        """

    def can_paginate(self, operation_name: str) -> bool:
        """
        Check if an operation can be paginated.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/opensearchserverless.html#OpenSearchServiceServerless.Client.can_paginate)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_opensearchserverless/client/#can_paginate)
        """

    def close(self) -> None:
        """
        Closes underlying endpoint connections.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/opensearchserverless.html#OpenSearchServiceServerless.Client.close)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_opensearchserverless/client/#close)
        """

    def create_access_policy(
        self,
        *,
        name: str,
        policy: str,
        type: Literal["data"],
        clientToken: str = ...,
        description: str = ...
    ) -> CreateAccessPolicyResponseTypeDef:
        """
        Creates a data access policy for OpenSearch Serverless.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/opensearchserverless.html#OpenSearchServiceServerless.Client.create_access_policy)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_opensearchserverless/client/#create_access_policy)
        """

    def create_collection(
        self,
        *,
        name: str,
        clientToken: str = ...,
        description: str = ...,
        tags: Sequence[TagTypeDef] = ...,
        type: CollectionTypeType = ...
    ) -> CreateCollectionResponseTypeDef:
        """
        Creates a new OpenSearch Serverless collection.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/opensearchserverless.html#OpenSearchServiceServerless.Client.create_collection)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_opensearchserverless/client/#create_collection)
        """

    def create_security_config(
        self,
        *,
        name: str,
        type: Literal["saml"],
        clientToken: str = ...,
        description: str = ...,
        samlOptions: SamlConfigOptionsTypeDef = ...
    ) -> CreateSecurityConfigResponseTypeDef:
        """
        Specifies a security configuration for OpenSearch Serverless.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/opensearchserverless.html#OpenSearchServiceServerless.Client.create_security_config)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_opensearchserverless/client/#create_security_config)
        """

    def create_security_policy(
        self,
        *,
        name: str,
        policy: str,
        type: SecurityPolicyTypeType,
        clientToken: str = ...,
        description: str = ...
    ) -> CreateSecurityPolicyResponseTypeDef:
        """
        Creates a security policy to be used by one or more OpenSearch Serverless
        collections.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/opensearchserverless.html#OpenSearchServiceServerless.Client.create_security_policy)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_opensearchserverless/client/#create_security_policy)
        """

    def create_vpc_endpoint(
        self,
        *,
        name: str,
        subnetIds: Sequence[str],
        vpcId: str,
        clientToken: str = ...,
        securityGroupIds: Sequence[str] = ...
    ) -> CreateVpcEndpointResponseTypeDef:
        """
        Creates an OpenSearch Serverless-managed interface VPC endpoint.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/opensearchserverless.html#OpenSearchServiceServerless.Client.create_vpc_endpoint)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_opensearchserverless/client/#create_vpc_endpoint)
        """

    def delete_access_policy(
        self, *, name: str, type: Literal["data"], clientToken: str = ...
    ) -> Dict[str, Any]:
        """
        Deletes an OpenSearch Serverless access policy.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/opensearchserverless.html#OpenSearchServiceServerless.Client.delete_access_policy)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_opensearchserverless/client/#delete_access_policy)
        """

    def delete_collection(
        self, *, id: str, clientToken: str = ...
    ) -> DeleteCollectionResponseTypeDef:
        """
        Deletes an OpenSearch Serverless collection.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/opensearchserverless.html#OpenSearchServiceServerless.Client.delete_collection)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_opensearchserverless/client/#delete_collection)
        """

    def delete_security_config(self, *, id: str, clientToken: str = ...) -> Dict[str, Any]:
        """
        Deletes a security configuration for OpenSearch Serverless.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/opensearchserverless.html#OpenSearchServiceServerless.Client.delete_security_config)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_opensearchserverless/client/#delete_security_config)
        """

    def delete_security_policy(
        self, *, name: str, type: SecurityPolicyTypeType, clientToken: str = ...
    ) -> Dict[str, Any]:
        """
        Deletes an OpenSearch Serverless security policy.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/opensearchserverless.html#OpenSearchServiceServerless.Client.delete_security_policy)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_opensearchserverless/client/#delete_security_policy)
        """

    def delete_vpc_endpoint(
        self, *, id: str, clientToken: str = ...
    ) -> DeleteVpcEndpointResponseTypeDef:
        """
        Deletes an OpenSearch Serverless-managed interface endpoint.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/opensearchserverless.html#OpenSearchServiceServerless.Client.delete_vpc_endpoint)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_opensearchserverless/client/#delete_vpc_endpoint)
        """

    def generate_presigned_url(
        self,
        ClientMethod: str,
        Params: Mapping[str, Any] = ...,
        ExpiresIn: int = 3600,
        HttpMethod: str = ...,
    ) -> str:
        """
        Generate a presigned url given a client, its method, and arguments.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/opensearchserverless.html#OpenSearchServiceServerless.Client.generate_presigned_url)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_opensearchserverless/client/#generate_presigned_url)
        """

    def get_access_policy(
        self, *, name: str, type: Literal["data"]
    ) -> GetAccessPolicyResponseTypeDef:
        """
        Returns an OpenSearch Serverless access policy.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/opensearchserverless.html#OpenSearchServiceServerless.Client.get_access_policy)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_opensearchserverless/client/#get_access_policy)
        """

    def get_account_settings(self) -> GetAccountSettingsResponseTypeDef:
        """
        Returns account-level settings related to OpenSearch Serverless.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/opensearchserverless.html#OpenSearchServiceServerless.Client.get_account_settings)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_opensearchserverless/client/#get_account_settings)
        """

    def get_policies_stats(self) -> GetPoliciesStatsResponseTypeDef:
        """
        Returns statistical information about your OpenSearch Serverless access
        policies, security configurations, and security policies.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/opensearchserverless.html#OpenSearchServiceServerless.Client.get_policies_stats)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_opensearchserverless/client/#get_policies_stats)
        """

    def get_security_config(self, *, id: str) -> GetSecurityConfigResponseTypeDef:
        """
        Returns information about an OpenSearch Serverless security configuration.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/opensearchserverless.html#OpenSearchServiceServerless.Client.get_security_config)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_opensearchserverless/client/#get_security_config)
        """

    def get_security_policy(
        self, *, name: str, type: SecurityPolicyTypeType
    ) -> GetSecurityPolicyResponseTypeDef:
        """
        Returns information about a configured OpenSearch Serverless security policy.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/opensearchserverless.html#OpenSearchServiceServerless.Client.get_security_policy)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_opensearchserverless/client/#get_security_policy)
        """

    def list_access_policies(
        self,
        *,
        type: Literal["data"],
        maxResults: int = ...,
        nextToken: str = ...,
        resource: Sequence[str] = ...
    ) -> ListAccessPoliciesResponseTypeDef:
        """
        Returns information about a list of OpenSearch Serverless access policies.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/opensearchserverless.html#OpenSearchServiceServerless.Client.list_access_policies)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_opensearchserverless/client/#list_access_policies)
        """

    def list_collections(
        self,
        *,
        collectionFilters: CollectionFiltersTypeDef = ...,
        maxResults: int = ...,
        nextToken: str = ...
    ) -> ListCollectionsResponseTypeDef:
        """
        Lists all OpenSearch Serverless collections.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/opensearchserverless.html#OpenSearchServiceServerless.Client.list_collections)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_opensearchserverless/client/#list_collections)
        """

    def list_security_configs(
        self, *, type: Literal["saml"], maxResults: int = ..., nextToken: str = ...
    ) -> ListSecurityConfigsResponseTypeDef:
        """
        Returns information about configured OpenSearch Serverless security
        configurations.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/opensearchserverless.html#OpenSearchServiceServerless.Client.list_security_configs)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_opensearchserverless/client/#list_security_configs)
        """

    def list_security_policies(
        self,
        *,
        type: SecurityPolicyTypeType,
        maxResults: int = ...,
        nextToken: str = ...,
        resource: Sequence[str] = ...
    ) -> ListSecurityPoliciesResponseTypeDef:
        """
        Returns information about configured OpenSearch Serverless security policies.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/opensearchserverless.html#OpenSearchServiceServerless.Client.list_security_policies)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_opensearchserverless/client/#list_security_policies)
        """

    def list_tags_for_resource(self, *, resourceArn: str) -> ListTagsForResourceResponseTypeDef:
        """
        Returns the tags for an OpenSearch Serverless resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/opensearchserverless.html#OpenSearchServiceServerless.Client.list_tags_for_resource)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_opensearchserverless/client/#list_tags_for_resource)
        """

    def list_vpc_endpoints(
        self,
        *,
        maxResults: int = ...,
        nextToken: str = ...,
        vpcEndpointFilters: VpcEndpointFiltersTypeDef = ...
    ) -> ListVpcEndpointsResponseTypeDef:
        """
        Returns the OpenSearch Serverless-managed interface VPC endpoints associated
        with the current account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/opensearchserverless.html#OpenSearchServiceServerless.Client.list_vpc_endpoints)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_opensearchserverless/client/#list_vpc_endpoints)
        """

    def tag_resource(self, *, resourceArn: str, tags: Sequence[TagTypeDef]) -> Dict[str, Any]:
        """
        Associates tags with an OpenSearch Serverless resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/opensearchserverless.html#OpenSearchServiceServerless.Client.tag_resource)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_opensearchserverless/client/#tag_resource)
        """

    def untag_resource(self, *, resourceArn: str, tagKeys: Sequence[str]) -> Dict[str, Any]:
        """
        Removes a tag or set of tags from an OpenSearch Serverless resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/opensearchserverless.html#OpenSearchServiceServerless.Client.untag_resource)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_opensearchserverless/client/#untag_resource)
        """

    def update_access_policy(
        self,
        *,
        name: str,
        policyVersion: str,
        type: Literal["data"],
        clientToken: str = ...,
        description: str = ...,
        policy: str = ...
    ) -> UpdateAccessPolicyResponseTypeDef:
        """
        Updates an OpenSearch Serverless access policy.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/opensearchserverless.html#OpenSearchServiceServerless.Client.update_access_policy)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_opensearchserverless/client/#update_access_policy)
        """

    def update_account_settings(
        self, *, capacityLimits: CapacityLimitsTypeDef = ...
    ) -> UpdateAccountSettingsResponseTypeDef:
        """
        Update the OpenSearch Serverless settings for the current Amazon Web Services
        account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/opensearchserverless.html#OpenSearchServiceServerless.Client.update_account_settings)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_opensearchserverless/client/#update_account_settings)
        """

    def update_collection(
        self, *, id: str, clientToken: str = ..., description: str = ...
    ) -> UpdateCollectionResponseTypeDef:
        """
        Updates an OpenSearch Serverless collection.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/opensearchserverless.html#OpenSearchServiceServerless.Client.update_collection)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_opensearchserverless/client/#update_collection)
        """

    def update_security_config(
        self,
        *,
        configVersion: str,
        id: str,
        clientToken: str = ...,
        description: str = ...,
        samlOptions: SamlConfigOptionsTypeDef = ...
    ) -> UpdateSecurityConfigResponseTypeDef:
        """
        Updates a security configuration for OpenSearch Serverless.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/opensearchserverless.html#OpenSearchServiceServerless.Client.update_security_config)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_opensearchserverless/client/#update_security_config)
        """

    def update_security_policy(
        self,
        *,
        name: str,
        policyVersion: str,
        type: SecurityPolicyTypeType,
        clientToken: str = ...,
        description: str = ...,
        policy: str = ...
    ) -> UpdateSecurityPolicyResponseTypeDef:
        """
        Updates an OpenSearch Serverless security policy.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/opensearchserverless.html#OpenSearchServiceServerless.Client.update_security_policy)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_opensearchserverless/client/#update_security_policy)
        """

    def update_vpc_endpoint(
        self,
        *,
        id: str,
        addSecurityGroupIds: Sequence[str] = ...,
        addSubnetIds: Sequence[str] = ...,
        clientToken: str = ...,
        removeSecurityGroupIds: Sequence[str] = ...,
        removeSubnetIds: Sequence[str] = ...
    ) -> UpdateVpcEndpointResponseTypeDef:
        """
        Updates an OpenSearch Serverless-managed interface endpoint.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/opensearchserverless.html#OpenSearchServiceServerless.Client.update_vpc_endpoint)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_opensearchserverless/client/#update_vpc_endpoint)
        """
