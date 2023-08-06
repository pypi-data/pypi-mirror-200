"""
Type annotations for sagemaker-geospatial service type definitions.

[Open documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_sagemaker_geospatial/type_defs/)

Usage::

    ```python
    from mypy_boto3_sagemaker_geospatial.type_defs import MultiPolygonGeometryInputTypeDef

    data: MultiPolygonGeometryInputTypeDef = {...}
    ```
"""
import sys
from datetime import datetime
from typing import Any, Dict, List, Mapping, Sequence, Union

from botocore.response import StreamingBody

from .literals import (
    AlgorithmNameGeoMosaicType,
    AlgorithmNameResamplingType,
    ComparisonOperatorType,
    DataCollectionTypeType,
    EarthObservationJobErrorTypeType,
    EarthObservationJobExportStatusType,
    EarthObservationJobStatusType,
    ExportErrorTypeType,
    GroupByType,
    OutputTypeType,
    PredefinedResolutionType,
    SortOrderType,
    TargetOptionsType,
    TemporalStatisticsType,
    VectorEnrichmentJobErrorTypeType,
    VectorEnrichmentJobExportErrorTypeType,
    VectorEnrichmentJobExportStatusType,
    VectorEnrichmentJobStatusType,
    VectorEnrichmentJobTypeType,
    ZonalStatisticsType,
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
    "MultiPolygonGeometryInputTypeDef",
    "PolygonGeometryInputTypeDef",
    "AssetValueTypeDef",
    "CloudRemovalConfigInputTypeDef",
    "OperationTypeDef",
    "DeleteEarthObservationJobInputRequestTypeDef",
    "DeleteVectorEnrichmentJobInputRequestTypeDef",
    "EarthObservationJobErrorDetailsTypeDef",
    "EoCloudCoverInputTypeDef",
    "S3DataInputTypeDef",
    "ResponseMetadataTypeDef",
    "ExportErrorDetailsOutputTypeDef",
    "ExportS3DataInputTypeDef",
    "VectorEnrichmentJobS3DataTypeDef",
    "FilterTypeDef",
    "GeoMosaicConfigInputTypeDef",
    "GeometryTypeDef",
    "GetEarthObservationJobInputRequestTypeDef",
    "OutputBandTypeDef",
    "GetRasterDataCollectionInputRequestTypeDef",
    "GetTileInputRequestTypeDef",
    "GetVectorEnrichmentJobInputRequestTypeDef",
    "VectorEnrichmentJobErrorDetailsTypeDef",
    "VectorEnrichmentJobExportErrorDetailsTypeDef",
    "PropertiesTypeDef",
    "TemporalStatisticsConfigInputTypeDef",
    "ZonalStatisticsConfigInputTypeDef",
    "LandsatCloudCoverLandInputTypeDef",
    "PaginatorConfigTypeDef",
    "ListEarthObservationJobInputRequestTypeDef",
    "ListEarthObservationJobOutputConfigTypeDef",
    "ListRasterDataCollectionsInputRequestTypeDef",
    "ListTagsForResourceRequestRequestTypeDef",
    "ListVectorEnrichmentJobInputRequestTypeDef",
    "ListVectorEnrichmentJobOutputConfigTypeDef",
    "MapMatchingConfigTypeDef",
    "UserDefinedTypeDef",
    "PlatformInputTypeDef",
    "ViewOffNadirInputTypeDef",
    "ViewSunAzimuthInputTypeDef",
    "ViewSunElevationInputTypeDef",
    "TimeRangeFilterInputTypeDef",
    "TimeRangeFilterOutputTypeDef",
    "ReverseGeocodingConfigTypeDef",
    "StopEarthObservationJobInputRequestTypeDef",
    "StopVectorEnrichmentJobInputRequestTypeDef",
    "TagResourceRequestRequestTypeDef",
    "UntagResourceRequestRequestTypeDef",
    "AreaOfInterestGeometryTypeDef",
    "CustomIndicesInputTypeDef",
    "EojDataSourceConfigInputTypeDef",
    "GetTileOutputTypeDef",
    "ListTagsForResourceResponseTypeDef",
    "ExportErrorDetailsTypeDef",
    "OutputConfigInputTypeDef",
    "ExportVectorEnrichmentJobOutputConfigTypeDef",
    "VectorEnrichmentJobDataSourceConfigInputTypeDef",
    "GetRasterDataCollectionOutputTypeDef",
    "RasterDataCollectionMetadataTypeDef",
    "ItemSourceTypeDef",
    "ListEarthObservationJobInputListEarthObservationJobsPaginateTypeDef",
    "ListRasterDataCollectionsInputListRasterDataCollectionsPaginateTypeDef",
    "ListVectorEnrichmentJobInputListVectorEnrichmentJobsPaginateTypeDef",
    "ListEarthObservationJobOutputTypeDef",
    "ListVectorEnrichmentJobOutputTypeDef",
    "OutputResolutionResamplingInputTypeDef",
    "OutputResolutionStackInputTypeDef",
    "PropertyTypeDef",
    "VectorEnrichmentJobConfigTypeDef",
    "AreaOfInterestTypeDef",
    "BandMathConfigInputTypeDef",
    "ExportEarthObservationJobInputRequestTypeDef",
    "ExportEarthObservationJobOutputTypeDef",
    "ExportVectorEnrichmentJobInputRequestTypeDef",
    "ExportVectorEnrichmentJobOutputTypeDef",
    "VectorEnrichmentJobInputConfigTypeDef",
    "ListRasterDataCollectionsOutputTypeDef",
    "SearchRasterDataCollectionOutputTypeDef",
    "ResamplingConfigInputTypeDef",
    "StackConfigInputTypeDef",
    "PropertyFilterTypeDef",
    "GetVectorEnrichmentJobOutputTypeDef",
    "StartVectorEnrichmentJobInputRequestTypeDef",
    "StartVectorEnrichmentJobOutputTypeDef",
    "JobConfigInputTypeDef",
    "PropertyFiltersTypeDef",
    "RasterDataCollectionQueryInputTypeDef",
    "RasterDataCollectionQueryOutputTypeDef",
    "RasterDataCollectionQueryWithBandFilterInputTypeDef",
    "InputConfigInputTypeDef",
    "InputConfigOutputTypeDef",
    "SearchRasterDataCollectionInputRequestTypeDef",
    "StartEarthObservationJobInputRequestTypeDef",
    "GetEarthObservationJobOutputTypeDef",
    "StartEarthObservationJobOutputTypeDef",
)

MultiPolygonGeometryInputTypeDef = TypedDict(
    "MultiPolygonGeometryInputTypeDef",
    {
        "Coordinates": List[List[List[List[float]]]],
    },
)

PolygonGeometryInputTypeDef = TypedDict(
    "PolygonGeometryInputTypeDef",
    {
        "Coordinates": List[List[List[float]]],
    },
)

AssetValueTypeDef = TypedDict(
    "AssetValueTypeDef",
    {
        "Href": str,
    },
    total=False,
)

CloudRemovalConfigInputTypeDef = TypedDict(
    "CloudRemovalConfigInputTypeDef",
    {
        "AlgorithmName": Literal["INTERPOLATION"],
        "InterpolationValue": str,
        "TargetBands": List[str],
    },
    total=False,
)

_RequiredOperationTypeDef = TypedDict(
    "_RequiredOperationTypeDef",
    {
        "Equation": str,
        "Name": str,
    },
)
_OptionalOperationTypeDef = TypedDict(
    "_OptionalOperationTypeDef",
    {
        "OutputType": OutputTypeType,
    },
    total=False,
)

class OperationTypeDef(_RequiredOperationTypeDef, _OptionalOperationTypeDef):
    pass

DeleteEarthObservationJobInputRequestTypeDef = TypedDict(
    "DeleteEarthObservationJobInputRequestTypeDef",
    {
        "Arn": str,
    },
)

DeleteVectorEnrichmentJobInputRequestTypeDef = TypedDict(
    "DeleteVectorEnrichmentJobInputRequestTypeDef",
    {
        "Arn": str,
    },
)

EarthObservationJobErrorDetailsTypeDef = TypedDict(
    "EarthObservationJobErrorDetailsTypeDef",
    {
        "Message": str,
        "Type": EarthObservationJobErrorTypeType,
    },
    total=False,
)

EoCloudCoverInputTypeDef = TypedDict(
    "EoCloudCoverInputTypeDef",
    {
        "LowerBound": float,
        "UpperBound": float,
    },
)

_RequiredS3DataInputTypeDef = TypedDict(
    "_RequiredS3DataInputTypeDef",
    {
        "MetadataProvider": Literal["PLANET_ORDER"],
        "S3Uri": str,
    },
)
_OptionalS3DataInputTypeDef = TypedDict(
    "_OptionalS3DataInputTypeDef",
    {
        "KmsKeyId": str,
    },
    total=False,
)

class S3DataInputTypeDef(_RequiredS3DataInputTypeDef, _OptionalS3DataInputTypeDef):
    pass

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

ExportErrorDetailsOutputTypeDef = TypedDict(
    "ExportErrorDetailsOutputTypeDef",
    {
        "Message": str,
        "Type": ExportErrorTypeType,
    },
    total=False,
)

_RequiredExportS3DataInputTypeDef = TypedDict(
    "_RequiredExportS3DataInputTypeDef",
    {
        "S3Uri": str,
    },
)
_OptionalExportS3DataInputTypeDef = TypedDict(
    "_OptionalExportS3DataInputTypeDef",
    {
        "KmsKeyId": str,
    },
    total=False,
)

class ExportS3DataInputTypeDef(
    _RequiredExportS3DataInputTypeDef, _OptionalExportS3DataInputTypeDef
):
    pass

_RequiredVectorEnrichmentJobS3DataTypeDef = TypedDict(
    "_RequiredVectorEnrichmentJobS3DataTypeDef",
    {
        "S3Uri": str,
    },
)
_OptionalVectorEnrichmentJobS3DataTypeDef = TypedDict(
    "_OptionalVectorEnrichmentJobS3DataTypeDef",
    {
        "KmsKeyId": str,
    },
    total=False,
)

class VectorEnrichmentJobS3DataTypeDef(
    _RequiredVectorEnrichmentJobS3DataTypeDef, _OptionalVectorEnrichmentJobS3DataTypeDef
):
    pass

_RequiredFilterTypeDef = TypedDict(
    "_RequiredFilterTypeDef",
    {
        "Name": str,
        "Type": str,
    },
)
_OptionalFilterTypeDef = TypedDict(
    "_OptionalFilterTypeDef",
    {
        "Maximum": float,
        "Minimum": float,
    },
    total=False,
)

class FilterTypeDef(_RequiredFilterTypeDef, _OptionalFilterTypeDef):
    pass

GeoMosaicConfigInputTypeDef = TypedDict(
    "GeoMosaicConfigInputTypeDef",
    {
        "AlgorithmName": AlgorithmNameGeoMosaicType,
        "TargetBands": List[str],
    },
    total=False,
)

GeometryTypeDef = TypedDict(
    "GeometryTypeDef",
    {
        "Coordinates": List[List[List[float]]],
        "Type": str,
    },
)

GetEarthObservationJobInputRequestTypeDef = TypedDict(
    "GetEarthObservationJobInputRequestTypeDef",
    {
        "Arn": str,
    },
)

OutputBandTypeDef = TypedDict(
    "OutputBandTypeDef",
    {
        "BandName": str,
        "OutputDataType": OutputTypeType,
    },
)

GetRasterDataCollectionInputRequestTypeDef = TypedDict(
    "GetRasterDataCollectionInputRequestTypeDef",
    {
        "Arn": str,
    },
)

_RequiredGetTileInputRequestTypeDef = TypedDict(
    "_RequiredGetTileInputRequestTypeDef",
    {
        "Arn": str,
        "ImageAssets": Sequence[str],
        "Target": TargetOptionsType,
        "x": int,
        "y": int,
        "z": int,
    },
)
_OptionalGetTileInputRequestTypeDef = TypedDict(
    "_OptionalGetTileInputRequestTypeDef",
    {
        "ExecutionRoleArn": str,
        "ImageMask": bool,
        "OutputDataType": OutputTypeType,
        "OutputFormat": str,
        "PropertyFilters": str,
        "TimeRangeFilter": str,
    },
    total=False,
)

class GetTileInputRequestTypeDef(
    _RequiredGetTileInputRequestTypeDef, _OptionalGetTileInputRequestTypeDef
):
    pass

GetVectorEnrichmentJobInputRequestTypeDef = TypedDict(
    "GetVectorEnrichmentJobInputRequestTypeDef",
    {
        "Arn": str,
    },
)

VectorEnrichmentJobErrorDetailsTypeDef = TypedDict(
    "VectorEnrichmentJobErrorDetailsTypeDef",
    {
        "ErrorMessage": str,
        "ErrorType": VectorEnrichmentJobErrorTypeType,
    },
    total=False,
)

VectorEnrichmentJobExportErrorDetailsTypeDef = TypedDict(
    "VectorEnrichmentJobExportErrorDetailsTypeDef",
    {
        "Message": str,
        "Type": VectorEnrichmentJobExportErrorTypeType,
    },
    total=False,
)

PropertiesTypeDef = TypedDict(
    "PropertiesTypeDef",
    {
        "EoCloudCover": float,
        "LandsatCloudCoverLand": float,
        "Platform": str,
        "ViewOffNadir": float,
        "ViewSunAzimuth": float,
        "ViewSunElevation": float,
    },
    total=False,
)

_RequiredTemporalStatisticsConfigInputTypeDef = TypedDict(
    "_RequiredTemporalStatisticsConfigInputTypeDef",
    {
        "Statistics": List[TemporalStatisticsType],
    },
)
_OptionalTemporalStatisticsConfigInputTypeDef = TypedDict(
    "_OptionalTemporalStatisticsConfigInputTypeDef",
    {
        "GroupBy": GroupByType,
        "TargetBands": List[str],
    },
    total=False,
)

class TemporalStatisticsConfigInputTypeDef(
    _RequiredTemporalStatisticsConfigInputTypeDef, _OptionalTemporalStatisticsConfigInputTypeDef
):
    pass

_RequiredZonalStatisticsConfigInputTypeDef = TypedDict(
    "_RequiredZonalStatisticsConfigInputTypeDef",
    {
        "Statistics": List[ZonalStatisticsType],
        "ZoneS3Path": str,
    },
)
_OptionalZonalStatisticsConfigInputTypeDef = TypedDict(
    "_OptionalZonalStatisticsConfigInputTypeDef",
    {
        "TargetBands": List[str],
        "ZoneS3PathKmsKeyId": str,
    },
    total=False,
)

class ZonalStatisticsConfigInputTypeDef(
    _RequiredZonalStatisticsConfigInputTypeDef, _OptionalZonalStatisticsConfigInputTypeDef
):
    pass

LandsatCloudCoverLandInputTypeDef = TypedDict(
    "LandsatCloudCoverLandInputTypeDef",
    {
        "LowerBound": float,
        "UpperBound": float,
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

ListEarthObservationJobInputRequestTypeDef = TypedDict(
    "ListEarthObservationJobInputRequestTypeDef",
    {
        "MaxResults": int,
        "NextToken": str,
        "SortBy": str,
        "SortOrder": SortOrderType,
        "StatusEquals": EarthObservationJobStatusType,
    },
    total=False,
)

_RequiredListEarthObservationJobOutputConfigTypeDef = TypedDict(
    "_RequiredListEarthObservationJobOutputConfigTypeDef",
    {
        "Arn": str,
        "CreationTime": datetime,
        "DurationInSeconds": int,
        "Name": str,
        "OperationType": str,
        "Status": EarthObservationJobStatusType,
    },
)
_OptionalListEarthObservationJobOutputConfigTypeDef = TypedDict(
    "_OptionalListEarthObservationJobOutputConfigTypeDef",
    {
        "Tags": Dict[str, str],
    },
    total=False,
)

class ListEarthObservationJobOutputConfigTypeDef(
    _RequiredListEarthObservationJobOutputConfigTypeDef,
    _OptionalListEarthObservationJobOutputConfigTypeDef,
):
    pass

ListRasterDataCollectionsInputRequestTypeDef = TypedDict(
    "ListRasterDataCollectionsInputRequestTypeDef",
    {
        "MaxResults": int,
        "NextToken": str,
    },
    total=False,
)

ListTagsForResourceRequestRequestTypeDef = TypedDict(
    "ListTagsForResourceRequestRequestTypeDef",
    {
        "ResourceArn": str,
    },
)

ListVectorEnrichmentJobInputRequestTypeDef = TypedDict(
    "ListVectorEnrichmentJobInputRequestTypeDef",
    {
        "MaxResults": int,
        "NextToken": str,
        "SortBy": str,
        "SortOrder": SortOrderType,
        "StatusEquals": str,
    },
    total=False,
)

_RequiredListVectorEnrichmentJobOutputConfigTypeDef = TypedDict(
    "_RequiredListVectorEnrichmentJobOutputConfigTypeDef",
    {
        "Arn": str,
        "CreationTime": datetime,
        "DurationInSeconds": int,
        "Name": str,
        "Status": VectorEnrichmentJobStatusType,
        "Type": VectorEnrichmentJobTypeType,
    },
)
_OptionalListVectorEnrichmentJobOutputConfigTypeDef = TypedDict(
    "_OptionalListVectorEnrichmentJobOutputConfigTypeDef",
    {
        "Tags": Dict[str, str],
    },
    total=False,
)

class ListVectorEnrichmentJobOutputConfigTypeDef(
    _RequiredListVectorEnrichmentJobOutputConfigTypeDef,
    _OptionalListVectorEnrichmentJobOutputConfigTypeDef,
):
    pass

MapMatchingConfigTypeDef = TypedDict(
    "MapMatchingConfigTypeDef",
    {
        "IdAttributeName": str,
        "TimestampAttributeName": str,
        "XAttributeName": str,
        "YAttributeName": str,
    },
)

UserDefinedTypeDef = TypedDict(
    "UserDefinedTypeDef",
    {
        "Unit": Literal["METERS"],
        "Value": float,
    },
)

_RequiredPlatformInputTypeDef = TypedDict(
    "_RequiredPlatformInputTypeDef",
    {
        "Value": str,
    },
)
_OptionalPlatformInputTypeDef = TypedDict(
    "_OptionalPlatformInputTypeDef",
    {
        "ComparisonOperator": ComparisonOperatorType,
    },
    total=False,
)

class PlatformInputTypeDef(_RequiredPlatformInputTypeDef, _OptionalPlatformInputTypeDef):
    pass

ViewOffNadirInputTypeDef = TypedDict(
    "ViewOffNadirInputTypeDef",
    {
        "LowerBound": float,
        "UpperBound": float,
    },
)

ViewSunAzimuthInputTypeDef = TypedDict(
    "ViewSunAzimuthInputTypeDef",
    {
        "LowerBound": float,
        "UpperBound": float,
    },
)

ViewSunElevationInputTypeDef = TypedDict(
    "ViewSunElevationInputTypeDef",
    {
        "LowerBound": float,
        "UpperBound": float,
    },
)

TimeRangeFilterInputTypeDef = TypedDict(
    "TimeRangeFilterInputTypeDef",
    {
        "EndTime": Union[datetime, str],
        "StartTime": Union[datetime, str],
    },
)

TimeRangeFilterOutputTypeDef = TypedDict(
    "TimeRangeFilterOutputTypeDef",
    {
        "EndTime": datetime,
        "StartTime": datetime,
    },
)

ReverseGeocodingConfigTypeDef = TypedDict(
    "ReverseGeocodingConfigTypeDef",
    {
        "XAttributeName": str,
        "YAttributeName": str,
    },
)

StopEarthObservationJobInputRequestTypeDef = TypedDict(
    "StopEarthObservationJobInputRequestTypeDef",
    {
        "Arn": str,
    },
)

StopVectorEnrichmentJobInputRequestTypeDef = TypedDict(
    "StopVectorEnrichmentJobInputRequestTypeDef",
    {
        "Arn": str,
    },
)

TagResourceRequestRequestTypeDef = TypedDict(
    "TagResourceRequestRequestTypeDef",
    {
        "ResourceArn": str,
        "Tags": Mapping[str, str],
    },
)

UntagResourceRequestRequestTypeDef = TypedDict(
    "UntagResourceRequestRequestTypeDef",
    {
        "ResourceArn": str,
        "TagKeys": Sequence[str],
    },
)

AreaOfInterestGeometryTypeDef = TypedDict(
    "AreaOfInterestGeometryTypeDef",
    {
        "MultiPolygonGeometry": MultiPolygonGeometryInputTypeDef,
        "PolygonGeometry": PolygonGeometryInputTypeDef,
    },
    total=False,
)

CustomIndicesInputTypeDef = TypedDict(
    "CustomIndicesInputTypeDef",
    {
        "Operations": List[OperationTypeDef],
    },
    total=False,
)

EojDataSourceConfigInputTypeDef = TypedDict(
    "EojDataSourceConfigInputTypeDef",
    {
        "S3Data": S3DataInputTypeDef,
    },
    total=False,
)

GetTileOutputTypeDef = TypedDict(
    "GetTileOutputTypeDef",
    {
        "BinaryFile": StreamingBody,
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

ExportErrorDetailsTypeDef = TypedDict(
    "ExportErrorDetailsTypeDef",
    {
        "ExportResults": ExportErrorDetailsOutputTypeDef,
        "ExportSourceImages": ExportErrorDetailsOutputTypeDef,
    },
    total=False,
)

OutputConfigInputTypeDef = TypedDict(
    "OutputConfigInputTypeDef",
    {
        "S3Data": ExportS3DataInputTypeDef,
    },
)

ExportVectorEnrichmentJobOutputConfigTypeDef = TypedDict(
    "ExportVectorEnrichmentJobOutputConfigTypeDef",
    {
        "S3Data": VectorEnrichmentJobS3DataTypeDef,
    },
)

VectorEnrichmentJobDataSourceConfigInputTypeDef = TypedDict(
    "VectorEnrichmentJobDataSourceConfigInputTypeDef",
    {
        "S3Data": VectorEnrichmentJobS3DataTypeDef,
    },
    total=False,
)

GetRasterDataCollectionOutputTypeDef = TypedDict(
    "GetRasterDataCollectionOutputTypeDef",
    {
        "Arn": str,
        "Description": str,
        "DescriptionPageUrl": str,
        "ImageSourceBands": List[str],
        "Name": str,
        "SupportedFilters": List[FilterTypeDef],
        "Tags": Dict[str, str],
        "Type": DataCollectionTypeType,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

_RequiredRasterDataCollectionMetadataTypeDef = TypedDict(
    "_RequiredRasterDataCollectionMetadataTypeDef",
    {
        "Arn": str,
        "Description": str,
        "Name": str,
        "SupportedFilters": List[FilterTypeDef],
        "Type": DataCollectionTypeType,
    },
)
_OptionalRasterDataCollectionMetadataTypeDef = TypedDict(
    "_OptionalRasterDataCollectionMetadataTypeDef",
    {
        "DescriptionPageUrl": str,
        "Tags": Dict[str, str],
    },
    total=False,
)

class RasterDataCollectionMetadataTypeDef(
    _RequiredRasterDataCollectionMetadataTypeDef, _OptionalRasterDataCollectionMetadataTypeDef
):
    pass

_RequiredItemSourceTypeDef = TypedDict(
    "_RequiredItemSourceTypeDef",
    {
        "DateTime": datetime,
        "Geometry": GeometryTypeDef,
        "Id": str,
    },
)
_OptionalItemSourceTypeDef = TypedDict(
    "_OptionalItemSourceTypeDef",
    {
        "Assets": Dict[str, AssetValueTypeDef],
        "Properties": PropertiesTypeDef,
    },
    total=False,
)

class ItemSourceTypeDef(_RequiredItemSourceTypeDef, _OptionalItemSourceTypeDef):
    pass

ListEarthObservationJobInputListEarthObservationJobsPaginateTypeDef = TypedDict(
    "ListEarthObservationJobInputListEarthObservationJobsPaginateTypeDef",
    {
        "SortBy": str,
        "SortOrder": SortOrderType,
        "StatusEquals": EarthObservationJobStatusType,
        "PaginationConfig": PaginatorConfigTypeDef,
    },
    total=False,
)

ListRasterDataCollectionsInputListRasterDataCollectionsPaginateTypeDef = TypedDict(
    "ListRasterDataCollectionsInputListRasterDataCollectionsPaginateTypeDef",
    {
        "PaginationConfig": PaginatorConfigTypeDef,
    },
    total=False,
)

ListVectorEnrichmentJobInputListVectorEnrichmentJobsPaginateTypeDef = TypedDict(
    "ListVectorEnrichmentJobInputListVectorEnrichmentJobsPaginateTypeDef",
    {
        "SortBy": str,
        "SortOrder": SortOrderType,
        "StatusEquals": str,
        "PaginationConfig": PaginatorConfigTypeDef,
    },
    total=False,
)

ListEarthObservationJobOutputTypeDef = TypedDict(
    "ListEarthObservationJobOutputTypeDef",
    {
        "EarthObservationJobSummaries": List[ListEarthObservationJobOutputConfigTypeDef],
        "NextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ListVectorEnrichmentJobOutputTypeDef = TypedDict(
    "ListVectorEnrichmentJobOutputTypeDef",
    {
        "NextToken": str,
        "VectorEnrichmentJobSummaries": List[ListVectorEnrichmentJobOutputConfigTypeDef],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

OutputResolutionResamplingInputTypeDef = TypedDict(
    "OutputResolutionResamplingInputTypeDef",
    {
        "UserDefined": UserDefinedTypeDef,
    },
)

OutputResolutionStackInputTypeDef = TypedDict(
    "OutputResolutionStackInputTypeDef",
    {
        "Predefined": PredefinedResolutionType,
        "UserDefined": UserDefinedTypeDef,
    },
    total=False,
)

PropertyTypeDef = TypedDict(
    "PropertyTypeDef",
    {
        "EoCloudCover": EoCloudCoverInputTypeDef,
        "LandsatCloudCoverLand": LandsatCloudCoverLandInputTypeDef,
        "Platform": PlatformInputTypeDef,
        "ViewOffNadir": ViewOffNadirInputTypeDef,
        "ViewSunAzimuth": ViewSunAzimuthInputTypeDef,
        "ViewSunElevation": ViewSunElevationInputTypeDef,
    },
    total=False,
)

VectorEnrichmentJobConfigTypeDef = TypedDict(
    "VectorEnrichmentJobConfigTypeDef",
    {
        "MapMatchingConfig": MapMatchingConfigTypeDef,
        "ReverseGeocodingConfig": ReverseGeocodingConfigTypeDef,
    },
    total=False,
)

AreaOfInterestTypeDef = TypedDict(
    "AreaOfInterestTypeDef",
    {
        "AreaOfInterestGeometry": AreaOfInterestGeometryTypeDef,
    },
    total=False,
)

BandMathConfigInputTypeDef = TypedDict(
    "BandMathConfigInputTypeDef",
    {
        "CustomIndices": CustomIndicesInputTypeDef,
        "PredefinedIndices": List[str],
    },
    total=False,
)

_RequiredExportEarthObservationJobInputRequestTypeDef = TypedDict(
    "_RequiredExportEarthObservationJobInputRequestTypeDef",
    {
        "Arn": str,
        "ExecutionRoleArn": str,
        "OutputConfig": OutputConfigInputTypeDef,
    },
)
_OptionalExportEarthObservationJobInputRequestTypeDef = TypedDict(
    "_OptionalExportEarthObservationJobInputRequestTypeDef",
    {
        "ClientToken": str,
        "ExportSourceImages": bool,
    },
    total=False,
)

class ExportEarthObservationJobInputRequestTypeDef(
    _RequiredExportEarthObservationJobInputRequestTypeDef,
    _OptionalExportEarthObservationJobInputRequestTypeDef,
):
    pass

ExportEarthObservationJobOutputTypeDef = TypedDict(
    "ExportEarthObservationJobOutputTypeDef",
    {
        "Arn": str,
        "CreationTime": datetime,
        "ExecutionRoleArn": str,
        "ExportSourceImages": bool,
        "ExportStatus": EarthObservationJobExportStatusType,
        "OutputConfig": OutputConfigInputTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

_RequiredExportVectorEnrichmentJobInputRequestTypeDef = TypedDict(
    "_RequiredExportVectorEnrichmentJobInputRequestTypeDef",
    {
        "Arn": str,
        "ExecutionRoleArn": str,
        "OutputConfig": ExportVectorEnrichmentJobOutputConfigTypeDef,
    },
)
_OptionalExportVectorEnrichmentJobInputRequestTypeDef = TypedDict(
    "_OptionalExportVectorEnrichmentJobInputRequestTypeDef",
    {
        "ClientToken": str,
    },
    total=False,
)

class ExportVectorEnrichmentJobInputRequestTypeDef(
    _RequiredExportVectorEnrichmentJobInputRequestTypeDef,
    _OptionalExportVectorEnrichmentJobInputRequestTypeDef,
):
    pass

ExportVectorEnrichmentJobOutputTypeDef = TypedDict(
    "ExportVectorEnrichmentJobOutputTypeDef",
    {
        "Arn": str,
        "CreationTime": datetime,
        "ExecutionRoleArn": str,
        "ExportStatus": VectorEnrichmentJobExportStatusType,
        "OutputConfig": ExportVectorEnrichmentJobOutputConfigTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

VectorEnrichmentJobInputConfigTypeDef = TypedDict(
    "VectorEnrichmentJobInputConfigTypeDef",
    {
        "DataSourceConfig": VectorEnrichmentJobDataSourceConfigInputTypeDef,
        "DocumentType": Literal["CSV"],
    },
)

ListRasterDataCollectionsOutputTypeDef = TypedDict(
    "ListRasterDataCollectionsOutputTypeDef",
    {
        "NextToken": str,
        "RasterDataCollectionSummaries": List[RasterDataCollectionMetadataTypeDef],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

SearchRasterDataCollectionOutputTypeDef = TypedDict(
    "SearchRasterDataCollectionOutputTypeDef",
    {
        "ApproximateResultCount": int,
        "Items": List[ItemSourceTypeDef],
        "NextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

_RequiredResamplingConfigInputTypeDef = TypedDict(
    "_RequiredResamplingConfigInputTypeDef",
    {
        "OutputResolution": OutputResolutionResamplingInputTypeDef,
    },
)
_OptionalResamplingConfigInputTypeDef = TypedDict(
    "_OptionalResamplingConfigInputTypeDef",
    {
        "AlgorithmName": AlgorithmNameResamplingType,
        "TargetBands": List[str],
    },
    total=False,
)

class ResamplingConfigInputTypeDef(
    _RequiredResamplingConfigInputTypeDef, _OptionalResamplingConfigInputTypeDef
):
    pass

StackConfigInputTypeDef = TypedDict(
    "StackConfigInputTypeDef",
    {
        "OutputResolution": OutputResolutionStackInputTypeDef,
        "TargetBands": List[str],
    },
    total=False,
)

PropertyFilterTypeDef = TypedDict(
    "PropertyFilterTypeDef",
    {
        "Property": PropertyTypeDef,
    },
)

GetVectorEnrichmentJobOutputTypeDef = TypedDict(
    "GetVectorEnrichmentJobOutputTypeDef",
    {
        "Arn": str,
        "CreationTime": datetime,
        "DurationInSeconds": int,
        "ErrorDetails": VectorEnrichmentJobErrorDetailsTypeDef,
        "ExecutionRoleArn": str,
        "ExportErrorDetails": VectorEnrichmentJobExportErrorDetailsTypeDef,
        "ExportStatus": VectorEnrichmentJobExportStatusType,
        "InputConfig": VectorEnrichmentJobInputConfigTypeDef,
        "JobConfig": VectorEnrichmentJobConfigTypeDef,
        "KmsKeyId": str,
        "Name": str,
        "Status": VectorEnrichmentJobStatusType,
        "Tags": Dict[str, str],
        "Type": VectorEnrichmentJobTypeType,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

_RequiredStartVectorEnrichmentJobInputRequestTypeDef = TypedDict(
    "_RequiredStartVectorEnrichmentJobInputRequestTypeDef",
    {
        "ExecutionRoleArn": str,
        "InputConfig": VectorEnrichmentJobInputConfigTypeDef,
        "JobConfig": VectorEnrichmentJobConfigTypeDef,
        "Name": str,
    },
)
_OptionalStartVectorEnrichmentJobInputRequestTypeDef = TypedDict(
    "_OptionalStartVectorEnrichmentJobInputRequestTypeDef",
    {
        "ClientToken": str,
        "KmsKeyId": str,
        "Tags": Mapping[str, str],
    },
    total=False,
)

class StartVectorEnrichmentJobInputRequestTypeDef(
    _RequiredStartVectorEnrichmentJobInputRequestTypeDef,
    _OptionalStartVectorEnrichmentJobInputRequestTypeDef,
):
    pass

StartVectorEnrichmentJobOutputTypeDef = TypedDict(
    "StartVectorEnrichmentJobOutputTypeDef",
    {
        "Arn": str,
        "CreationTime": datetime,
        "DurationInSeconds": int,
        "ExecutionRoleArn": str,
        "InputConfig": VectorEnrichmentJobInputConfigTypeDef,
        "JobConfig": VectorEnrichmentJobConfigTypeDef,
        "KmsKeyId": str,
        "Name": str,
        "Status": VectorEnrichmentJobStatusType,
        "Tags": Dict[str, str],
        "Type": VectorEnrichmentJobTypeType,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

JobConfigInputTypeDef = TypedDict(
    "JobConfigInputTypeDef",
    {
        "BandMathConfig": BandMathConfigInputTypeDef,
        "CloudMaskingConfig": Dict[str, Any],
        "CloudRemovalConfig": CloudRemovalConfigInputTypeDef,
        "GeoMosaicConfig": GeoMosaicConfigInputTypeDef,
        "LandCoverSegmentationConfig": Dict[str, Any],
        "ResamplingConfig": ResamplingConfigInputTypeDef,
        "StackConfig": StackConfigInputTypeDef,
        "TemporalStatisticsConfig": TemporalStatisticsConfigInputTypeDef,
        "ZonalStatisticsConfig": ZonalStatisticsConfigInputTypeDef,
    },
    total=False,
)

PropertyFiltersTypeDef = TypedDict(
    "PropertyFiltersTypeDef",
    {
        "LogicalOperator": Literal["AND"],
        "Properties": List[PropertyFilterTypeDef],
    },
    total=False,
)

_RequiredRasterDataCollectionQueryInputTypeDef = TypedDict(
    "_RequiredRasterDataCollectionQueryInputTypeDef",
    {
        "RasterDataCollectionArn": str,
        "TimeRangeFilter": TimeRangeFilterInputTypeDef,
    },
)
_OptionalRasterDataCollectionQueryInputTypeDef = TypedDict(
    "_OptionalRasterDataCollectionQueryInputTypeDef",
    {
        "AreaOfInterest": AreaOfInterestTypeDef,
        "PropertyFilters": PropertyFiltersTypeDef,
    },
    total=False,
)

class RasterDataCollectionQueryInputTypeDef(
    _RequiredRasterDataCollectionQueryInputTypeDef, _OptionalRasterDataCollectionQueryInputTypeDef
):
    pass

_RequiredRasterDataCollectionQueryOutputTypeDef = TypedDict(
    "_RequiredRasterDataCollectionQueryOutputTypeDef",
    {
        "RasterDataCollectionArn": str,
        "RasterDataCollectionName": str,
        "TimeRangeFilter": TimeRangeFilterOutputTypeDef,
    },
)
_OptionalRasterDataCollectionQueryOutputTypeDef = TypedDict(
    "_OptionalRasterDataCollectionQueryOutputTypeDef",
    {
        "AreaOfInterest": AreaOfInterestTypeDef,
        "PropertyFilters": PropertyFiltersTypeDef,
    },
    total=False,
)

class RasterDataCollectionQueryOutputTypeDef(
    _RequiredRasterDataCollectionQueryOutputTypeDef, _OptionalRasterDataCollectionQueryOutputTypeDef
):
    pass

_RequiredRasterDataCollectionQueryWithBandFilterInputTypeDef = TypedDict(
    "_RequiredRasterDataCollectionQueryWithBandFilterInputTypeDef",
    {
        "TimeRangeFilter": TimeRangeFilterInputTypeDef,
    },
)
_OptionalRasterDataCollectionQueryWithBandFilterInputTypeDef = TypedDict(
    "_OptionalRasterDataCollectionQueryWithBandFilterInputTypeDef",
    {
        "AreaOfInterest": AreaOfInterestTypeDef,
        "BandFilter": Sequence[str],
        "PropertyFilters": PropertyFiltersTypeDef,
    },
    total=False,
)

class RasterDataCollectionQueryWithBandFilterInputTypeDef(
    _RequiredRasterDataCollectionQueryWithBandFilterInputTypeDef,
    _OptionalRasterDataCollectionQueryWithBandFilterInputTypeDef,
):
    pass

InputConfigInputTypeDef = TypedDict(
    "InputConfigInputTypeDef",
    {
        "DataSourceConfig": EojDataSourceConfigInputTypeDef,
        "PreviousEarthObservationJobArn": str,
        "RasterDataCollectionQuery": RasterDataCollectionQueryInputTypeDef,
    },
    total=False,
)

InputConfigOutputTypeDef = TypedDict(
    "InputConfigOutputTypeDef",
    {
        "DataSourceConfig": EojDataSourceConfigInputTypeDef,
        "PreviousEarthObservationJobArn": str,
        "RasterDataCollectionQuery": RasterDataCollectionQueryOutputTypeDef,
    },
    total=False,
)

_RequiredSearchRasterDataCollectionInputRequestTypeDef = TypedDict(
    "_RequiredSearchRasterDataCollectionInputRequestTypeDef",
    {
        "Arn": str,
        "RasterDataCollectionQuery": RasterDataCollectionQueryWithBandFilterInputTypeDef,
    },
)
_OptionalSearchRasterDataCollectionInputRequestTypeDef = TypedDict(
    "_OptionalSearchRasterDataCollectionInputRequestTypeDef",
    {
        "NextToken": str,
    },
    total=False,
)

class SearchRasterDataCollectionInputRequestTypeDef(
    _RequiredSearchRasterDataCollectionInputRequestTypeDef,
    _OptionalSearchRasterDataCollectionInputRequestTypeDef,
):
    pass

_RequiredStartEarthObservationJobInputRequestTypeDef = TypedDict(
    "_RequiredStartEarthObservationJobInputRequestTypeDef",
    {
        "InputConfig": InputConfigInputTypeDef,
        "JobConfig": JobConfigInputTypeDef,
        "Name": str,
    },
)
_OptionalStartEarthObservationJobInputRequestTypeDef = TypedDict(
    "_OptionalStartEarthObservationJobInputRequestTypeDef",
    {
        "ClientToken": str,
        "ExecutionRoleArn": str,
        "KmsKeyId": str,
        "Tags": Mapping[str, str],
    },
    total=False,
)

class StartEarthObservationJobInputRequestTypeDef(
    _RequiredStartEarthObservationJobInputRequestTypeDef,
    _OptionalStartEarthObservationJobInputRequestTypeDef,
):
    pass

GetEarthObservationJobOutputTypeDef = TypedDict(
    "GetEarthObservationJobOutputTypeDef",
    {
        "Arn": str,
        "CreationTime": datetime,
        "DurationInSeconds": int,
        "ErrorDetails": EarthObservationJobErrorDetailsTypeDef,
        "ExecutionRoleArn": str,
        "ExportErrorDetails": ExportErrorDetailsTypeDef,
        "ExportStatus": EarthObservationJobExportStatusType,
        "InputConfig": InputConfigOutputTypeDef,
        "JobConfig": JobConfigInputTypeDef,
        "KmsKeyId": str,
        "Name": str,
        "OutputBands": List[OutputBandTypeDef],
        "Status": EarthObservationJobStatusType,
        "Tags": Dict[str, str],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

StartEarthObservationJobOutputTypeDef = TypedDict(
    "StartEarthObservationJobOutputTypeDef",
    {
        "Arn": str,
        "CreationTime": datetime,
        "DurationInSeconds": int,
        "ExecutionRoleArn": str,
        "InputConfig": InputConfigOutputTypeDef,
        "JobConfig": JobConfigInputTypeDef,
        "KmsKeyId": str,
        "Name": str,
        "Status": EarthObservationJobStatusType,
        "Tags": Dict[str, str],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
