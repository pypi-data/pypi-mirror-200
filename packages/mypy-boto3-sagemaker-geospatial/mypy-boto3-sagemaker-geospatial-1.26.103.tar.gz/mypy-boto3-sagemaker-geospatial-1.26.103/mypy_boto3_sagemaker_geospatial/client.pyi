"""
Type annotations for sagemaker-geospatial service client.

[Open documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_sagemaker_geospatial/client/)

Usage::

    ```python
    from boto3.session import Session
    from mypy_boto3_sagemaker_geospatial.client import SageMakergeospatialcapabilitiesClient

    session = Session()
    client: SageMakergeospatialcapabilitiesClient = session.client("sagemaker-geospatial")
    ```
"""
import sys
from typing import Any, Dict, Mapping, Sequence, Type, overload

from botocore.client import BaseClient, ClientMeta

from .literals import (
    EarthObservationJobStatusType,
    OutputTypeType,
    SortOrderType,
    TargetOptionsType,
)
from .paginator import (
    ListEarthObservationJobsPaginator,
    ListRasterDataCollectionsPaginator,
    ListVectorEnrichmentJobsPaginator,
)
from .type_defs import (
    ExportEarthObservationJobOutputTypeDef,
    ExportVectorEnrichmentJobOutputConfigTypeDef,
    ExportVectorEnrichmentJobOutputTypeDef,
    GetEarthObservationJobOutputTypeDef,
    GetRasterDataCollectionOutputTypeDef,
    GetTileOutputTypeDef,
    GetVectorEnrichmentJobOutputTypeDef,
    InputConfigInputTypeDef,
    JobConfigInputTypeDef,
    ListEarthObservationJobOutputTypeDef,
    ListRasterDataCollectionsOutputTypeDef,
    ListTagsForResourceResponseTypeDef,
    ListVectorEnrichmentJobOutputTypeDef,
    OutputConfigInputTypeDef,
    RasterDataCollectionQueryWithBandFilterInputTypeDef,
    SearchRasterDataCollectionOutputTypeDef,
    StartEarthObservationJobOutputTypeDef,
    StartVectorEnrichmentJobOutputTypeDef,
    VectorEnrichmentJobConfigTypeDef,
    VectorEnrichmentJobInputConfigTypeDef,
)

if sys.version_info >= (3, 9):
    from typing import Literal
else:
    from typing_extensions import Literal

__all__ = ("SageMakergeospatialcapabilitiesClient",)

class BotocoreClientError(BaseException):
    MSG_TEMPLATE: str

    def __init__(self, error_response: Mapping[str, Any], operation_name: str) -> None:
        self.response: Dict[str, Any]
        self.operation_name: str

class Exceptions:
    AccessDeniedException: Type[BotocoreClientError]
    ClientError: Type[BotocoreClientError]
    ConflictException: Type[BotocoreClientError]
    InternalServerException: Type[BotocoreClientError]
    ResourceNotFoundException: Type[BotocoreClientError]
    ServiceQuotaExceededException: Type[BotocoreClientError]
    ThrottlingException: Type[BotocoreClientError]
    ValidationException: Type[BotocoreClientError]

class SageMakergeospatialcapabilitiesClient(BaseClient):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker-geospatial.html#SageMakergeospatialcapabilities.Client)
    [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_sagemaker_geospatial/client/)
    """

    meta: ClientMeta

    @property
    def exceptions(self) -> Exceptions:
        """
        SageMakergeospatialcapabilitiesClient exceptions.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker-geospatial.html#SageMakergeospatialcapabilities.Client.exceptions)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_sagemaker_geospatial/client/#exceptions)
        """
    def can_paginate(self, operation_name: str) -> bool:
        """
        Check if an operation can be paginated.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker-geospatial.html#SageMakergeospatialcapabilities.Client.can_paginate)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_sagemaker_geospatial/client/#can_paginate)
        """
    def close(self) -> None:
        """
        Closes underlying endpoint connections.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker-geospatial.html#SageMakergeospatialcapabilities.Client.close)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_sagemaker_geospatial/client/#close)
        """
    def delete_earth_observation_job(self, *, Arn: str) -> Dict[str, Any]:
        """
        Use this operation to delete an Earth Observation job.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker-geospatial.html#SageMakergeospatialcapabilities.Client.delete_earth_observation_job)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_sagemaker_geospatial/client/#delete_earth_observation_job)
        """
    def delete_vector_enrichment_job(self, *, Arn: str) -> Dict[str, Any]:
        """
        Use this operation to delete a Vector Enrichment job.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker-geospatial.html#SageMakergeospatialcapabilities.Client.delete_vector_enrichment_job)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_sagemaker_geospatial/client/#delete_vector_enrichment_job)
        """
    def export_earth_observation_job(
        self,
        *,
        Arn: str,
        ExecutionRoleArn: str,
        OutputConfig: OutputConfigInputTypeDef,
        ClientToken: str = ...,
        ExportSourceImages: bool = ...
    ) -> ExportEarthObservationJobOutputTypeDef:
        """
        Use this operation to export results of an Earth Observation job and optionally
        source images used as input to the EOJ to an Amazon S3 location.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker-geospatial.html#SageMakergeospatialcapabilities.Client.export_earth_observation_job)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_sagemaker_geospatial/client/#export_earth_observation_job)
        """
    def export_vector_enrichment_job(
        self,
        *,
        Arn: str,
        ExecutionRoleArn: str,
        OutputConfig: ExportVectorEnrichmentJobOutputConfigTypeDef,
        ClientToken: str = ...
    ) -> ExportVectorEnrichmentJobOutputTypeDef:
        """
        Use this operation to copy results of a Vector Enrichment job to an Amazon S3
        location.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker-geospatial.html#SageMakergeospatialcapabilities.Client.export_vector_enrichment_job)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_sagemaker_geospatial/client/#export_vector_enrichment_job)
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

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker-geospatial.html#SageMakergeospatialcapabilities.Client.generate_presigned_url)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_sagemaker_geospatial/client/#generate_presigned_url)
        """
    def get_earth_observation_job(self, *, Arn: str) -> GetEarthObservationJobOutputTypeDef:
        """
        Get the details for a previously initiated Earth Observation job.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker-geospatial.html#SageMakergeospatialcapabilities.Client.get_earth_observation_job)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_sagemaker_geospatial/client/#get_earth_observation_job)
        """
    def get_raster_data_collection(self, *, Arn: str) -> GetRasterDataCollectionOutputTypeDef:
        """
        Use this operation to get details of a specific raster data collection.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker-geospatial.html#SageMakergeospatialcapabilities.Client.get_raster_data_collection)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_sagemaker_geospatial/client/#get_raster_data_collection)
        """
    def get_tile(
        self,
        *,
        Arn: str,
        ImageAssets: Sequence[str],
        Target: TargetOptionsType,
        x: int,
        y: int,
        z: int,
        ExecutionRoleArn: str = ...,
        ImageMask: bool = ...,
        OutputDataType: OutputTypeType = ...,
        OutputFormat: str = ...,
        PropertyFilters: str = ...,
        TimeRangeFilter: str = ...
    ) -> GetTileOutputTypeDef:
        """
        Gets a web mercator tile for the given Earth Observation job.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker-geospatial.html#SageMakergeospatialcapabilities.Client.get_tile)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_sagemaker_geospatial/client/#get_tile)
        """
    def get_vector_enrichment_job(self, *, Arn: str) -> GetVectorEnrichmentJobOutputTypeDef:
        """
        Retrieves details of a Vector Enrichment Job for a given job Amazon Resource
        Name (ARN).

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker-geospatial.html#SageMakergeospatialcapabilities.Client.get_vector_enrichment_job)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_sagemaker_geospatial/client/#get_vector_enrichment_job)
        """
    def list_earth_observation_jobs(
        self,
        *,
        MaxResults: int = ...,
        NextToken: str = ...,
        SortBy: str = ...,
        SortOrder: SortOrderType = ...,
        StatusEquals: EarthObservationJobStatusType = ...
    ) -> ListEarthObservationJobOutputTypeDef:
        """
        Use this operation to get a list of the Earth Observation jobs associated with
        the calling Amazon Web Services account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker-geospatial.html#SageMakergeospatialcapabilities.Client.list_earth_observation_jobs)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_sagemaker_geospatial/client/#list_earth_observation_jobs)
        """
    def list_raster_data_collections(
        self, *, MaxResults: int = ..., NextToken: str = ...
    ) -> ListRasterDataCollectionsOutputTypeDef:
        """
        Use this operation to get raster data collections.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker-geospatial.html#SageMakergeospatialcapabilities.Client.list_raster_data_collections)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_sagemaker_geospatial/client/#list_raster_data_collections)
        """
    def list_tags_for_resource(self, *, ResourceArn: str) -> ListTagsForResourceResponseTypeDef:
        """
        Lists the tags attached to the resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker-geospatial.html#SageMakergeospatialcapabilities.Client.list_tags_for_resource)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_sagemaker_geospatial/client/#list_tags_for_resource)
        """
    def list_vector_enrichment_jobs(
        self,
        *,
        MaxResults: int = ...,
        NextToken: str = ...,
        SortBy: str = ...,
        SortOrder: SortOrderType = ...,
        StatusEquals: str = ...
    ) -> ListVectorEnrichmentJobOutputTypeDef:
        """
        Retrieves a list of vector enrichment jobs.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker-geospatial.html#SageMakergeospatialcapabilities.Client.list_vector_enrichment_jobs)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_sagemaker_geospatial/client/#list_vector_enrichment_jobs)
        """
    def search_raster_data_collection(
        self,
        *,
        Arn: str,
        RasterDataCollectionQuery: RasterDataCollectionQueryWithBandFilterInputTypeDef,
        NextToken: str = ...
    ) -> SearchRasterDataCollectionOutputTypeDef:
        """
        Allows you run image query on a specific raster data collection to get a list of
        the satellite imagery matching the selected filters.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker-geospatial.html#SageMakergeospatialcapabilities.Client.search_raster_data_collection)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_sagemaker_geospatial/client/#search_raster_data_collection)
        """
    def start_earth_observation_job(
        self,
        *,
        InputConfig: InputConfigInputTypeDef,
        JobConfig: JobConfigInputTypeDef,
        Name: str,
        ClientToken: str = ...,
        ExecutionRoleArn: str = ...,
        KmsKeyId: str = ...,
        Tags: Mapping[str, str] = ...
    ) -> StartEarthObservationJobOutputTypeDef:
        """
        Use this operation to create an Earth observation job.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker-geospatial.html#SageMakergeospatialcapabilities.Client.start_earth_observation_job)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_sagemaker_geospatial/client/#start_earth_observation_job)
        """
    def start_vector_enrichment_job(
        self,
        *,
        ExecutionRoleArn: str,
        InputConfig: VectorEnrichmentJobInputConfigTypeDef,
        JobConfig: VectorEnrichmentJobConfigTypeDef,
        Name: str,
        ClientToken: str = ...,
        KmsKeyId: str = ...,
        Tags: Mapping[str, str] = ...
    ) -> StartVectorEnrichmentJobOutputTypeDef:
        """
        Creates a Vector Enrichment job for the supplied job type.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker-geospatial.html#SageMakergeospatialcapabilities.Client.start_vector_enrichment_job)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_sagemaker_geospatial/client/#start_vector_enrichment_job)
        """
    def stop_earth_observation_job(self, *, Arn: str) -> Dict[str, Any]:
        """
        Use this operation to stop an existing earth observation job.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker-geospatial.html#SageMakergeospatialcapabilities.Client.stop_earth_observation_job)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_sagemaker_geospatial/client/#stop_earth_observation_job)
        """
    def stop_vector_enrichment_job(self, *, Arn: str) -> Dict[str, Any]:
        """
        Stops the Vector Enrichment job for a given job ARN.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker-geospatial.html#SageMakergeospatialcapabilities.Client.stop_vector_enrichment_job)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_sagemaker_geospatial/client/#stop_vector_enrichment_job)
        """
    def tag_resource(self, *, ResourceArn: str, Tags: Mapping[str, str]) -> Dict[str, Any]:
        """
        The resource you want to tag.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker-geospatial.html#SageMakergeospatialcapabilities.Client.tag_resource)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_sagemaker_geospatial/client/#tag_resource)
        """
    def untag_resource(self, *, ResourceArn: str, TagKeys: Sequence[str]) -> Dict[str, Any]:
        """
        The resource you want to untag.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker-geospatial.html#SageMakergeospatialcapabilities.Client.untag_resource)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_sagemaker_geospatial/client/#untag_resource)
        """
    @overload
    def get_paginator(
        self, operation_name: Literal["list_earth_observation_jobs"]
    ) -> ListEarthObservationJobsPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker-geospatial.html#SageMakergeospatialcapabilities.Client.get_paginator)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_sagemaker_geospatial/client/#get_paginator)
        """
    @overload
    def get_paginator(
        self, operation_name: Literal["list_raster_data_collections"]
    ) -> ListRasterDataCollectionsPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker-geospatial.html#SageMakergeospatialcapabilities.Client.get_paginator)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_sagemaker_geospatial/client/#get_paginator)
        """
    @overload
    def get_paginator(
        self, operation_name: Literal["list_vector_enrichment_jobs"]
    ) -> ListVectorEnrichmentJobsPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker-geospatial.html#SageMakergeospatialcapabilities.Client.get_paginator)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_sagemaker_geospatial/client/#get_paginator)
        """
