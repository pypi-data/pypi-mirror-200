from typing import Dict, Literal, TypedDict, Union, List
from typing_extensions import Required


class IngestMetric(TypedDict, total=False):
    """ingest_metric."""

    org_id: Required[int]
    """
    The organization for which this metric is being sent.

    Required property
    """

    project_id: Required[int]
    """
    The project for which this metric is being sent.

    Required property
    """

    name: Required[str]
    """
    The metric name. Relay sometimes calls this an MRI and makes assumptions about its string shape, and those assumptions also exist in certain queries. The rest of the ingestion pipeline treats it as an opaque string.

    Required property
    """

    type: Required["_IngestMetricType"]
    """Required property"""

    timestamp: Required[int]
    """
    The timestamp at which this metric was being sent. Relay will round this down to the next 10-second interval.

    Required property
    """

    tags: Required[Dict[str, str]]
    """Required property"""

    value: Required[Union["NumberMetricValue", "NumbersMetricValue"]]
    """Required property"""

    retention_days: Required[int]
    """Required property"""



NumberMetricValue = Union[int, float]
"""number_metric_value."""



NumbersMetricValue = List[Union[int, float]]
"""numbers_metric_value."""



_IngestMetricType = Union[Literal["c"], Literal["d"], Literal["s"]]
"""The metric type. [c]ounter, [d]istribution, [s]et. Relay additionally defines Gauge, but that metric type is completely unsupported downstream."""
_INGESTMETRICTYPE_C: Literal["c"] = "c"
"""The values for the 'The metric type. [c]ounter, [d]istribution, [s]et. Relay additionally defines Gauge, but that metric type is completely unsupported downstream' enum"""
_INGESTMETRICTYPE_D: Literal["d"] = "d"
"""The values for the 'The metric type. [c]ounter, [d]istribution, [s]et. Relay additionally defines Gauge, but that metric type is completely unsupported downstream' enum"""
_INGESTMETRICTYPE_S: Literal["s"] = "s"
"""The values for the 'The metric type. [c]ounter, [d]istribution, [s]et. Relay additionally defines Gauge, but that metric type is completely unsupported downstream' enum"""

