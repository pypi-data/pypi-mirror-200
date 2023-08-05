from typing import Dict, TypedDict, List, Union
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

    type: Required[str]
    """
    The metric type. [c]ounter, [d]istribution, [s]et. Relay additionally defines Gauge, but that metric type is completely unsupported downstream.

    pattern: ^[cds]$

    Required property
    """

    timestamp: Required[int]
    """
    The timestamp at which this metric was being sent. Relay will round this down to the next 10-second interval.

    Required property
    """

    tags: Required[Dict[str, str]]
    """Required property"""

    value: Required[Union[int, List[Union[int, float]]]]
    """Required property"""

    width: int
    """DEAD PARAMETER -- downstream consumers do not use this, but relay sends it anyway. should remove or actually use"""

    retention_days: Required[int]
    """Required property"""

