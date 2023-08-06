"""
Type annotations for compute-optimizer service client paginators.

[Open documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_compute_optimizer/paginators/)

Usage::

    ```python
    from boto3.session import Session

    from mypy_boto3_compute_optimizer.client import ComputeOptimizerClient
    from mypy_boto3_compute_optimizer.paginator import (
        DescribeRecommendationExportJobsPaginator,
        GetEnrollmentStatusesForOrganizationPaginator,
        GetLambdaFunctionRecommendationsPaginator,
        GetRecommendationPreferencesPaginator,
        GetRecommendationSummariesPaginator,
    )

    session = Session()
    client: ComputeOptimizerClient = session.client("compute-optimizer")

    describe_recommendation_export_jobs_paginator: DescribeRecommendationExportJobsPaginator = client.get_paginator("describe_recommendation_export_jobs")
    get_enrollment_statuses_for_organization_paginator: GetEnrollmentStatusesForOrganizationPaginator = client.get_paginator("get_enrollment_statuses_for_organization")
    get_lambda_function_recommendations_paginator: GetLambdaFunctionRecommendationsPaginator = client.get_paginator("get_lambda_function_recommendations")
    get_recommendation_preferences_paginator: GetRecommendationPreferencesPaginator = client.get_paginator("get_recommendation_preferences")
    get_recommendation_summaries_paginator: GetRecommendationSummariesPaginator = client.get_paginator("get_recommendation_summaries")
    ```
"""
from typing import Generic, Iterator, Sequence, TypeVar

from botocore.paginate import PageIterator, Paginator

from .literals import ResourceTypeType
from .type_defs import (
    DescribeRecommendationExportJobsResponseTypeDef,
    EnrollmentFilterTypeDef,
    GetEnrollmentStatusesForOrganizationResponseTypeDef,
    GetLambdaFunctionRecommendationsResponseTypeDef,
    GetRecommendationPreferencesResponseTypeDef,
    GetRecommendationSummariesResponseTypeDef,
    JobFilterTypeDef,
    LambdaFunctionRecommendationFilterTypeDef,
    PaginatorConfigTypeDef,
    ScopeTypeDef,
)

__all__ = (
    "DescribeRecommendationExportJobsPaginator",
    "GetEnrollmentStatusesForOrganizationPaginator",
    "GetLambdaFunctionRecommendationsPaginator",
    "GetRecommendationPreferencesPaginator",
    "GetRecommendationSummariesPaginator",
)


_ItemTypeDef = TypeVar("_ItemTypeDef")


class _PageIterator(Generic[_ItemTypeDef], PageIterator):
    def __iter__(self) -> Iterator[_ItemTypeDef]:
        """
        Proxy method to specify iterator item type.
        """


class DescribeRecommendationExportJobsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/compute-optimizer.html#ComputeOptimizer.Paginator.DescribeRecommendationExportJobs)
    [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_compute_optimizer/paginators/#describerecommendationexportjobspaginator)
    """

    def paginate(
        self,
        *,
        jobIds: Sequence[str] = ...,
        filters: Sequence[JobFilterTypeDef] = ...,
        PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> _PageIterator[DescribeRecommendationExportJobsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/compute-optimizer.html#ComputeOptimizer.Paginator.DescribeRecommendationExportJobs.paginate)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_compute_optimizer/paginators/#describerecommendationexportjobspaginator)
        """


class GetEnrollmentStatusesForOrganizationPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/compute-optimizer.html#ComputeOptimizer.Paginator.GetEnrollmentStatusesForOrganization)
    [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_compute_optimizer/paginators/#getenrollmentstatusesfororganizationpaginator)
    """

    def paginate(
        self,
        *,
        filters: Sequence[EnrollmentFilterTypeDef] = ...,
        PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> _PageIterator[GetEnrollmentStatusesForOrganizationResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/compute-optimizer.html#ComputeOptimizer.Paginator.GetEnrollmentStatusesForOrganization.paginate)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_compute_optimizer/paginators/#getenrollmentstatusesfororganizationpaginator)
        """


class GetLambdaFunctionRecommendationsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/compute-optimizer.html#ComputeOptimizer.Paginator.GetLambdaFunctionRecommendations)
    [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_compute_optimizer/paginators/#getlambdafunctionrecommendationspaginator)
    """

    def paginate(
        self,
        *,
        functionArns: Sequence[str] = ...,
        accountIds: Sequence[str] = ...,
        filters: Sequence[LambdaFunctionRecommendationFilterTypeDef] = ...,
        PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> _PageIterator[GetLambdaFunctionRecommendationsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/compute-optimizer.html#ComputeOptimizer.Paginator.GetLambdaFunctionRecommendations.paginate)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_compute_optimizer/paginators/#getlambdafunctionrecommendationspaginator)
        """


class GetRecommendationPreferencesPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/compute-optimizer.html#ComputeOptimizer.Paginator.GetRecommendationPreferences)
    [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_compute_optimizer/paginators/#getrecommendationpreferencespaginator)
    """

    def paginate(
        self,
        *,
        resourceType: ResourceTypeType,
        scope: ScopeTypeDef = ...,
        PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> _PageIterator[GetRecommendationPreferencesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/compute-optimizer.html#ComputeOptimizer.Paginator.GetRecommendationPreferences.paginate)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_compute_optimizer/paginators/#getrecommendationpreferencespaginator)
        """


class GetRecommendationSummariesPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/compute-optimizer.html#ComputeOptimizer.Paginator.GetRecommendationSummaries)
    [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_compute_optimizer/paginators/#getrecommendationsummariespaginator)
    """

    def paginate(
        self, *, accountIds: Sequence[str] = ..., PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> _PageIterator[GetRecommendationSummariesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/compute-optimizer.html#ComputeOptimizer.Paginator.GetRecommendationSummaries.paginate)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_compute_optimizer/paginators/#getrecommendationsummariespaginator)
        """
